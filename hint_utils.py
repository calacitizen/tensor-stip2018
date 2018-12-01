# -*- coding: utf-8 -*-

from numpy import argmax
from nltk.tokenize import RegexpTokenizer
from pymorphy2 import MorphAnalyzer
from sklearn.feature_extraction.text import CountVectorizer as Vectorizer
from sklearn.metrics.pairwise import cosine_similarity
import chess
import chess.uci
from config import STOCKFISH_PATH
from json import dumps

PIECES = [
    'пешка', 'конь', 'слон',
    'ладья', 'ферзь', 'король'
]

RULE_TERMS = [
    'мат', 'пат', 'шах',
    'рокировка'
]

PIECES_DIC = {
    'король': 6,
    'ферзь': 5,
    'ладья': 4,
    'слон': 3,
    'конь': 2,
    'пешка': 1
}

class ChessBoard:

    def __init__(self, movetime=10):
        self.__engine = chess.uci.popen_engine(STOCKFISH_PATH)
        self.__info_handler = chess.uci.InfoHandler()
        self.__engine.info_handlers.append(self.__info_handler)
        self.__movetime = movetime

    def get_moves(self, fen, filt=None, reverse=False):
        board = chess.Board(fen=fen)
        self.__engine.position(board)
        moves = []
        for move in board.legal_moves:
            self.__engine.go(movetime=self.__movetime, searchmoves=[move])
            score, mate = self.__info_handler.info["score"][1]
            piece_type = board.piece_type_at(move.from_square)
            if filt is not None:
                if 'piece' in filt and len(filt['piece']) > 0:
                    if piece_type not in filt['piece']:
                        continue
            moves.append({
                "full_move": move.uci(),
                "mate": False if mate is None else (True if mate > 0 else False),
                "move": board.san(move),
                "score": round((0 if (score is None and mate is not None and mate < 0) else 999 \
                    if (score is None and mate is not None and mate > 0) else score) / 100.0, 2)
            })
        moves.sort(key=lambda x: -x['score'], reverse=reverse)
        moves.sort(key=lambda x: not x['mate'], reverse=reverse)
        return moves


class Preprocess:

    def __init__(self):
        self.__morph = MorphAnalyzer()
        self.__tokenizer = RegexpTokenizer(r'\w+')
        self.__vectorizer = Vectorizer()

    def __tokenize(self, sentence):
        data = {
            'token': None,
            'args': {
                'piece': [],
                'term': []
            }
        }
        words = [self.__morph.parse(word)[0].normal_form for word in self.__tokenizer.tokenize(sentence)]
        for piece in PIECES:
            if piece in words:

                words.remove(piece)
                if piece not in data['args']['piece']:
                    data['args']['piece'].append(PIECES_DIC[piece])
        for term in RULE_TERMS:
            if term in words:
                words.remove(term)
                if term not in data['args']['term']:
                    data['args']['term'].append(term)
        if len(words) > 0:
            data['token'] = ' '.join(words)
        return data

    def fit(self, documents):
        tokens = []
        for doc in documents:
            token = self.__tokenize(doc)['token']
            if token is not None:
                tokens.append(token)
        self.__data = self.__vectorizer.fit_transform(tokens)

    def transform(self, query):
        data = self.__tokenize(query)
        if data['token'] is not None:
            query_token = self.__vectorizer.transform([data['token']])
            result = cosine_similarity(self.__data, query_token)
            data['score'] = max(result)
            data['index'] = argmax(result)
        return data


class Generator:

    @staticmethod
    def how_piece_goes(args):
        if args is None:
            return HintService.to_dict(answer='О какой фигуре речь?')
        if len(args['piece']) == 0:
            return HintService.to_dict(answer='О какой фигуре речь?')
        result = ''
        for piece in args['piece']:
            if piece == 1:
                result += 'Пешка ходит со взятием \
по диагонали на одно поле вперёд-вправо или вперёд-\
влево, а без взятия — по вертикали на одно поле вперёд. \
Если пешка в данной партии ещё не делала ходов, она может \
сделать ход без взятия на два поля вперёд. '
            elif piece == 4:
                result += 'Ладья ходит на любое расстояние \
по вертикали или горизонтали.'
            elif piece == 2:
                result += 'Конь ходит на поле, находящееся \
на расстоянии 2 по вертикали и 1 по горизонтали или 1 по \
вертикали и 2 по горизонтали от текущего положения.'
            elif piece == 5:
                result += 'Ферзь ходит на любое расстояние \
по вертикали, горизонтали или диагонали.'
            elif piece == 3:
                result += 'Слон ходит на любое \
расстояние по диагонали.'
            elif piece == 6:
                result += 'Король ходит на расстояние 1 \
по вертикали, горизонтали или диагонали.'
            else:
                result += 'А что за новая фигура такая?'
        return HintService.to_dict(answer=result)

    @staticmethod
    def __piece(char, case):
        pieces = {
            't': {
                'K' : 'королем',
                'Q' : 'ферзем',
                'R' : 'ладьей',
                'B' : 'слоном',
                'N' : 'конем'
            },
            'v' : {
                'K' : 'короля',
                'Q' : 'ферзя',
                'R' : 'ладью',
                'B' : 'слона',
                'N' : 'коня'
            }
        }
        pawn = {
            't' : 'пешкой',
            'v' : 'пешку'}
        if case in pieces:
            if char in pieces[case]:
                return pieces[case][char]
            else:
                return pawn[case]
        else:
            return ''

    @staticmethod
    def get_move(args, move_type='best'):
        if args is None:
            return HintService.to_dict(answer='Кажется, кто-то спрятал от меня шахматную доску?')
        cb = ChessBoard()
        moves = cb.get_moves(args['fen'], args)
        if len(moves) == 0:
            return HintService.to_dict(answer='Доступных ходов нет.')
        if move_type == 'best':
            #  moves[0]['move'] = 'O-O'
            main_move = moves[0]['move']
            #  moves[0]['full_move'] = 'e2e4'
            answer = ''
            if 'O-O-O' in main_move:
                answer = 'Можно сделать рокировку с левой ладьей.'
            elif 'O-O' in main_move:
                answer = 'Можно сделать рокировку с правой ладьей.'
            elif '=' in main_move:
                answer = 'Предлагаю превратить пешку на ' + main_move[:2] + ' в ' + Generator.__piece(main_move[3], 'v') + '.'
            elif 'x' in main_move:
                #if Generator.__piece(main_move[0], 't') == 'пешкой':
                    answer = 'Предлагаю ' + Generator.__piece(main_move[0], 't') + ' на ' + moves[0]['full_move'][:2] +  ' съесть ' + \
                             Generator.__piece(Generator.__who_on(args['fen'], moves[0]['full_move'][2:4]),
                                               'v') + ' на ' + moves[0]['full_move'][2:4] + '.'
            if '+' in main_move:
                if len(answer)> 0 and answer[-1] == '.':
                    answer[-1] = ' '
                    answer += 'и поставить шах.'
                else:
                    answer = 'Можно поставить шах, сходив'
                    p = Generator.__piece(main_move[0], 't')
                    if p == 'пешкой':
                        answer += ' ' + p + ' на ' + main_move[:2] + '.'
                    else:
                        answer += ' ' + p + ' на ' + main_move[1:3] + '.'
            if '#' in main_move:
                if len(answer)> 0 and answer[-1] == '.':
                    answer[-1] = ' '
                    answer += 'и поставить мат.'
                else:
                    answer = 'Есть возможность поставить мат, сходив'
                    p = Generator.__piece(main_move[0], 't')
                    if p == 'пешкой':
                        answer += ' ' + p + ' на ' + main_move[:2] + '.'
                    else:
                        answer += ' ' + p + ' на ' + main_move[1:3] + '.'
            if len(answer) == 0:
                return HintService.to_dict(answer='Лучше всего сходить ' + Generator.__piece(main_move[0], 't') + ' ' + moves[0]['full_move']+ '.', best=[moves[0]], mate=False)
            return HintService.to_dict(answer=answer, best=moves, mate=False)
        else:
            return HintService.to_dict(answer='Вот возможные ходы.', possible=moves)

    @staticmethod
    def __who_on(fen, cell):
        a = ord('a')
        board = fen.split('/')
        for j in range(0, 8):
            for i in range(0, 9):
                board[j] = board[j].replace(str(i), '.' * i)
        value = board[7 - (int(cell[1]) - 1)][ord(cell[0]) - a].upper()
        if value != '.':
            return value
        else:
            return 'пустую клетку'

    @staticmethod
    def whats(args):
        if args is None:
            return HintService.to_dict(answer='Так о чем Вы хотите узнать?')
        empty = True
        for k in args:
            empty = empty and len(args[k]) == 0
        if empty:
            return HintService.to_dict(answer='Так о чем Вы хотите узнать?')
        if len(args['piece']) > 0:
            return HintService.to_dict(answer='Это фигура в шахматах.')
        elif len(args['term']) > 0:
            if args['term'][0] == 'мат':
                return HintService.to_dict(answer='Мат – это шах, от которого нет защиты, это конец партии.')
            elif args['term'][0] == 'пат':
                return HintService.to_dict(answer='Пат – это положение в шахматной партии, в котором сторона, имеющая право хода, не может им воспользоваться, так как все фигуры лишены возможности двигаться. Король в этот момент не находится под шахом.')
            elif args['term'][0] == 'шах':
                return HintService.to_dict(answer='Шах – это нападение на короля любой фигуры или пешки.')
            elif args['term'][0] == 'рокировка':
                return HintService.to_dict(answer='Рокировка – это ход в шахматах, при котором король перепрыгивает через одно поле вправо, или влево, а ладья закрывает его, вставая на соседнее поле. Рокировку могут делать и белые и черные. Рокировка бывает короткая и длинная. Короткая делается в сторону королевского фланга, длинная в сторону ферзевого фланга.')
            else:
                return HintService.to_dict(answer='Этого я не знаю.')
        else:
            return HintService.to_dict(answer='Этого я не знаю.')

    @staticmethod
    def whats_on(args):
        if args is None:
            return HintService.to_dict(answer='А какие координаты у фигуры?')
        if len(args['square']) == 0:
            return HintService.to_dict(answer='А какие координаты у фигуры?')
        # TODO: check piece
        return HintService.to_dict(answer='В разработке.')

    @staticmethod
    def secret_check(args):
        board = chess.Board(fen=args['fen'])
        if board.is_check():
            return HintService.to_dict(answer='Кажется, вам поставили шах.')
        elif board.is_stalemate():
            return HintService.to_dict(answer='Мат!')
        elif board.is_stalemate():
            return HintService.to_dict(answer='Это пат.')
        elif board.is_insufficient_material():
            return HintService.to_dict(answer='Ничья.')
        return HintService.to_dict()


class HintService:

    def __init__(self, knowledge, threshold=0.8):
        self.__preproc = Preprocess()
        self.__preproc.fit(knowledge['question'])
        self.__answer = knowledge['answer']
        self.__threshold = threshold

    @staticmethod
    def to_dict(answer='', best=[], possible=[], mate=False):
        return dumps({
            'answer': answer,
            'best_moves': best,
            'possible_moves': possible,
            'mate': mate
        })

    def ask(self, fen, question):
        if question == '':
            return HintService.__generate_answer('secret', {'fen': fen})
        answer = self.__preproc.transform(question)
        answer['args']['fen'] = fen
        # TODO: check fen
        if answer['token'] is None:
            return HintService.__generate_answer('no_token', answer['args'])
        if answer['score'] > self.__threshold:
            return HintService.__generate_answer(self.__answer[answer['index']], answer['args'])
        return HintService.__generate_answer('no_answer', answer['args'])

    @staticmethod
    def __generate_answer(answer, args):
        if answer == 'secret':
            return Generator.secret_check(args)
        elif answer == 'no_token':
            return HintService.to_dict(answer='Что Вы имеете в виду?')
        elif answer == 'no_answer':
            return HintService.to_dict(answer='Я не знаю, как ответить на Ваш вопрос.')
        elif answer == 'how_piece_goes':
            return Generator.how_piece_goes(args)
        elif answer == 'best_move':
            return Generator.get_move(args)
        elif answer == 'whats':
            return Generator.whats(args)
        elif answer == 'available_moves':
            return Generator.get_move(args, move_type='possible')
        elif answer == 'whats_on':
            return Generator.whats_on(args)
        else:
            return HintService.to_dict(answer='Я не ожидала такого вопроса.')
