#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify
import json
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from flask_cors import CORS

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
cors = CORS(app, resources={"/*": {"origins": "*"}})
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return 'hi'

@app.route('/hint', methods=['POST'])
def hint():
    if request.method == 'POST':
        data = request.get_json()
        if not ('board' in data):
            return answer([], [], 'Error: no board information sent', False)
        state = data['board']
        question = data['question']
        new_answer = get_answer(state)
        best_moves = new_answer[0]
        possible_moves = new_answer[1]
        answer = new_answer[2]
        mate = new_answer[3]
        print(answer)
        return json_answer(best_moves, possible_moves, answer, mate)
    else:
        return answer([], [], 'Ошибка!', False)
# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port,debug=True)

#funcrions
def json_answer(best_moves, possible_moves, answer, mate):
    return jsonify({
        'best_moves': best_moves,
        'possible_moves': possible_moves,
        'answer': answer,
        'mate' : mate
    })

def get_answer(state):
    game = {
        'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2': (['e2-e3'], ['e1-e3', 'e3-e5'], 'Возможное ходы e2-e3, e1-e3, e3-e5', False),
        'r1bqkb1r/ppp2ppp/2n2n2/3pp3/4P3/P1N2N2/1PPP1PPP/R1BQKB1R w KQkq d6 0 5': (['e2-e3'], ['e1-e3', 'e3-e5'], 'Я бы предложила съесть пешку на d5', False),
        'r1bqkb1r/ppp2ppp/2n5/3np3/8/P1N2N2/1PPP1PPP/R1BQKB1R w KQkq - 0 6': (['e2-e3'], ['e1-e3', 'e3-e5'], 'Ты только что спрашивал, в этот раз подумай сам. Ты же хочешь научиться играть.', False),
        'r1bqkb1r/ppp2ppp/2n5/8/4Nn2/P4N2/1PPPBPPP/R1BQK2R w KQkq - 1 8': (['e2-e3'], ['e1-e3', 'e3-e5'], 'Пожалуй стоит сделать рокировку', False),
        'r1bqkb1r/ppp2ppp/2n5/8/4N3/P4N2/1PPPnPPP/R1BQ1RK1 w kq - 0 9':  (['e2-e3'], ['e1-e3', 'e3-e5'], 'кажется вам поставили шах', False),
        'r2qkb1r/ppp2ppp/2n5/8/4N1b1/P4N2/1PPPQPPP/R1B2RK1 w kq - 1 10': (['e2-e3'], ['e1-e3', 'e3-e5'], 'Если сходишь правильно, можешь поставить мат', False),
        'r2qkb1r/ppp2ppp/2n2N2/8/6b1/P4N2/1PPPQPPP/R1B2RK1 b kq - 2 10': (['e2-e3'], ['e1-e3', 'e3-e5'], 'Шах и мат! Ты победил! Поздравляю!', False)
    }
    if state in game:
        return game[state]
    else:
        return ([], [], 'answer', False) 















