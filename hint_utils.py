# -*- coding: utf-8 -*-

from numpy import argmax
from nltk.tokenize import RegexpTokenizer
from pymorphy2 import MorphAnalyzer
from sklearn.feature_extraction.text import CountVectorizer as Vectorizer
from sklearn.metrics.pairwise import cosine_similarity

PIECES = [
    'пешка', 'ладья', 'конь',
    'ферзь', 'слон', 'король'
]

RULE_TERMS = [
    'мат', 'пат', 'ничья',
    'рокировка'
]


class Preprocess:

    def __init__(self):
        self.__morph = MorphAnalyzer()
        self.__tokenizer = RegexpTokenizer(r'\w+')
        self.__vectorizer = Vectorizer()

    def __tokenize(self, sentence):
        data = {
            'token': None,
            'args': {
                'piece': []
            }
        }
        words = [self.__morph.parse(word)[0].normal_form for word in self.__tokenizer.tokenize(sentence)]
        for piece in PIECES:
            if piece in words:
                words.remove(piece)
                if not piece in data['args']:
                    data['args']['piece'].append(piece)
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
            return 'О какой фигуре речь?'
        if len(args['piece']) == 0:
            return 'О какой фигуре речь?'
        result = ''
        for piece in args['piece']:
            if piece == PIECES[0]:
                result += 'Пешка ходит со взятием \
по диагонали на одно поле вперёд-вправо или вперёд-\
влево, а без взятия — по вертикали на одно поле вперёд. \
Если пешка в данной партии ещё не делала ходов, она может \
сделать ход без взятия на два поля вперёд. '
            elif piece == PIECES[1]:
                result += 'Ладья ходит на любое расстояние \
по вертикали или горизонтали.'
            elif piece == PIECES[2]:
                result += 'Конь ходит на поле, находящееся \
на расстоянии 2 по вертикали и 1 по горизонтали или 1 по \
вертикали и 2 по горизонтали от текущего положения.'
            elif piece == PIECES[3]:
                result += 'Ферзь ходит на любое расстояние \
по вертикали, горизонтали или диагонали.'
            elif piece == PIECES[4]:
                result += 'Слон ходит на любое \
расстояние по диагонали.'
            elif piece == PIECES[5]:
                result += 'Король ходит на расстояние 1 \
по вертикали, горизонтали или диагонали.'
            else:
                result += 'А что за новая фигура такая - ' + piece + '?'
        return result

    @staticmethod
    def best_move(args):
        if args is None:
            return 'Чем ходить будете?'
        if len(args['piece']) > 0:
            return 'Чтобы посчитать ходы для фигур %s, нужно дописать функцию!' % ' '.join(args['piece'])
        else:
            return 'Пока не умею делать этого.'

    @staticmethod
    def whats(args):
        if args is None:
            return 'Так о чем Вы хотите узнать?'
        empty = True
        for k in args:
            empty = empty and len(args[k]) == 0
        if empty:
            return 'Так о чем Вы хотите узнать?'
        if len(args['piece']) > 0:
            return 'Это фигура в шахматах.'
        else:
            return 'Этого я не знаю.'


class HintService:

    def __init__(self, knowledge, treshold=0.7, send_score=False):
        self.__preproc = Preprocess()
        self.__preproc.fit(knowledge['question'])
        self.__answer = knowledge['answer']
        self.__treshold = treshold
        self.__send_score = send_score

    def ask(self, question):
        result = ''
        answer = self.__preproc.transform(question)
        if answer['token'] is None:
            return self.__generate_answer('no_token', answer['args'])
        if self.__send_score:
            result += '[%f] ' % answer['score']
        if answer['score'] > self.__treshold:
            if self.__answer[answer['index']]:
                result += self.__generate_answer(self.__answer[answer['index']], answer['args'])
            else:
                result += self.__answer[answer['index']]
        else:
            result += self.__generate_answer('no_answer', answer['args'])
        return result

    def __generate_answer(self, answer, args):
        if answer == 'no_token':
            return 'Что Вы имеете в виду?'
        elif answer == 'no_answer':
            return 'Я не знаю, как ответить на Ваш вопрос.'
        elif answer == 'how_piece_goes':
            return Generator.how_piece_goes(args)
        elif answer == 'best_move':
            return Generator.best_move(args)
        elif answer == 'whats':
            return Generator.whats(args)
        else:
            return 'Я не ожидала такого вопроса.'
