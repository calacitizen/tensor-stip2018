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
cors = CORS(app, resources={r"/hint/*": {"origins": "*"}})
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
      "r1bqkb1r/ppp2ppp/2n2n2/3pp3/4P3/P1N2N2/1PPP1PPP/R1BQKB1R w KQkq d6 0 5": {
        "possible_moves": [], 
        "best_moves": [
          {
            "full_move": "f1b5", 
            "mate": False, 
            "move": "Bb5", 
            "score": 7.0
          }, 
          {
            "full_move": "e4d5", 
            "mate": False, 
            "move": "exd5", 
            "score": -9.0
          }, 
          {
            "full_move": "d2d4", 
            "mate": False, 
            "move": "d4", 
            "score": -27.0
          }, 
          {
            "full_move": "f1d3", 
            "mate": False, 
            "move": "Bd3", 
            "score": -35.0
          }, 
          {
            "full_move": "c3d5", 
            "mate": False, 
            "move": "Nxd5", 
            "score": -43.0
          }, 
          {
            "full_move": "d2d3", 
            "mate": False, 
            "move": "d3", 
            "score": -48.0
          }, 
          {
            "full_move": "f3g5", 
            "mate": False, 
            "move": "Ng5", 
            "score": -93.0
          }, 
          {
            "full_move": "b2b4", 
            "mate": False, 
            "move": "b4", 
            "score": -132.0
          }, 
          {
            "full_move": "d1e2", 
            "mate": False, 
            "move": "Qe2", 
            "score": -138.0
          }, 
          {
            "full_move": "h2h4", 
            "mate": False, 
            "move": "h4", 
            "score": -141.0
          }, 
          {
            "full_move": "h2h3", 
            "mate": False, 
            "move": "h3", 
            "score": -142.0
          }, 
          {
            "full_move": "f1e2", 
            "mate": False, 
            "move": "Be2", 
            "score": -143.0
          }, 
          {
            "full_move": "a3a4", 
            "mate": False, 
            "move": "a4", 
            "score": -148.0
          }, 
          {
            "full_move": "b2b3", 
            "mate": False, 
            "move": "b3", 
            "score": -170.0
          }, 
          {
            "full_move": "g2g3", 
            "mate": False, 
            "move": "g3", 
            "score": -172.0
          }, 
          {
            "full_move": "a1b1", 
            "mate": False, 
            "move": "Rb1", 
            "score": -196.0
          }, 
          {
            "full_move": "f3g1", 
            "mate": False, 
            "move": "Ng1", 
            "score": -207.0
          }, 
          {
            "full_move": "a1a2", 
            "mate": False, 
            "move": "Ra2", 
            "score": -215.0
          }, 
          {
            "full_move": "f3e5", 
            "mate": False, 
            "move": "Nxe5", 
            "score": -249.0
          }, 
          {
            "full_move": "g2g4", 
            "mate": False, 
            "move": "g4", 
            "score": -298.0
          }, 
          {
            "full_move": "f3h4", 
            "mate": False, 
            "move": "Nh4", 
            "score": -321.0
          }, 
          {
            "full_move": "h1g1", 
            "mate": False, 
            "move": "Rg1", 
            "score": -328.0
          }, 
          {
            "full_move": "c3a4", 
            "mate": False, 
            "move": "Na4", 
            "score": -331.0
          }, 
          {
            "full_move": "c3e2", 
            "mate": False, 
            "move": "Ne2", 
            "score": -335.0
          }, 
          {
            "full_move": "c3b5", 
            "mate": False, 
            "move": "Nb5", 
            "score": -337.0
          }, 
          {
            "full_move": "c3b1", 
            "mate": False, 
            "move": "Nb1", 
            "score": -419.0
          }, 
          {
            "full_move": "f1a6", 
            "mate": False, 
            "move": "Ba6", 
            "score": -423.0
          }, 
          {
            "full_move": "f1c4", 
            "mate": False, 
            "move": "Bc4", 
            "score": -425.0
          }, 
          {
            "full_move": "c3a2", 
            "mate": False, 
            "move": "Na2", 
            "score": -434.0
          }, 
          {
            "full_move": "f3d4", 
            "mate": False, 
            "move": "Nd4", 
            "score": -515.0
          }, 
          {
            "full_move": "e1e2", 
            "mate": False, 
            "move": "Ke2", 
            "score": -598.0
          }
        ], 
        "answer": "Я бы предложила съесть пешку на d5"
      }, 
      "r2qkb1r/ppp2ppp/2n5/8/4N1b1/P4N2/1PPPQPPP/R1B2RK1 w kq - 1 10": {
        "possible_moves": [], 
        "best_moves": [
          {
            "full_move": "e4d6", 
            "mate": False, 
            "move": "Nd6+", 
            "score": 750.0
          }, 
          {
            "full_move": "h2h3", 
            "mate": False, 
            "move": "h3", 
            "score": 292.0
          }, 
          {
            "full_move": "e4g5", 
            "mate": False, 
            "move": "Neg5+", 
            "score": 205.0
          }, 
          {
            "full_move": "b2b4", 
            "mate": False, 
            "move": "b4", 
            "score": 182.0
          }, 
          {
            "full_move": "d2d3", 
            "mate": False, 
            "move": "d3", 
            "score": 171.0
          }, 
          {
            "full_move": "b2b3", 
            "mate": False, 
            "move": "b3", 
            "score": 167.0
          }, 
          {
            "full_move": "d2d4", 
            "mate": False, 
            "move": "d4", 
            "score": 166.0
          }, 
          {
            "full_move": "f1e1", 
            "mate": False, 
            "move": "Re1", 
            "score": 160.0
          }, 
          {
            "full_move": "f1d1", 
            "mate": False, 
            "move": "Rd1", 
            "score": 151.0
          }, 
          {
            "full_move": "c2c3", 
            "mate": False, 
            "move": "c3", 
            "score": 151.0
          }, 
          {
            "full_move": "e4g3", 
            "mate": False, 
            "move": "Ng3+", 
            "score": 150.0
          }, 
          {
            "full_move": "a1b1", 
            "mate": False, 
            "move": "Rb1", 
            "score": 135.0
          }, 
          {
            "full_move": "a3a4", 
            "mate": False, 
            "move": "a4", 
            "score": 133.0
          }, 
          {
            "full_move": "e2e3", 
            "mate": False, 
            "move": "Qe3", 
            "score": 125.0
          }, 
          {
            "full_move": "e4c3", 
            "mate": False, 
            "move": "Nc3+", 
            "score": 123.0
          }, 
          {
            "full_move": "a1a2", 
            "mate": False, 
            "move": "Ra2", 
            "score": 121.0
          }, 
          {
            "full_move": "e2d1", 
            "mate": False, 
            "move": "Qd1", 
            "score": 86.0
          }, 
          {
            "full_move": "e2e1", 
            "mate": False, 
            "move": "Qe1", 
            "score": 85.0
          }, 
          {
            "full_move": "g1h1", 
            "mate": False, 
            "move": "Kh1", 
            "score": 85.0
          }, 
          {
            "full_move": "e2c4", 
            "mate": False, 
            "move": "Qc4", 
            "score": 71.0
          }, 
          {
            "full_move": "c2c4", 
            "mate": False, 
            "move": "c4", 
            "score": 22.0
          }, 
          {
            "full_move": "e4f6", 
            "mate": True, 
            "move": "Nf6#", 
            "score": 9.99
          }, 
          {
            "full_move": "e2b5", 
            "mate": False, 
            "move": "Qb5", 
            "score": 9.0
          }, 
          {
            "full_move": "h2h4", 
            "mate": False, 
            "move": "h4", 
            "score": 4.0
          }, 
          {
            "full_move": "e4c5", 
            "mate": False, 
            "move": "Nc5+", 
            "score": 0.0
          }, 
          {
            "full_move": "g2g3", 
            "mate": False, 
            "move": "g3", 
            "score": -54.0
          }, 
          {
            "full_move": "e2d3", 
            "mate": False, 
            "move": "Qd3", 
            "score": -189.0
          }, 
          {
            "full_move": "f3d4", 
            "mate": False, 
            "move": "Nd4", 
            "score": -745.0
          }, 
          {
            "full_move": "f3g5", 
            "mate": False, 
            "move": "Nfg5", 
            "score": -1112.0
          }, 
          {
            "full_move": "f3e5", 
            "mate": False, 
            "move": "Ne5", 
            "score": -1174.0
          }, 
          {
            "full_move": "e2a6", 
            "mate": False, 
            "move": "Qa6", 
            "score": -1176.0
          }, 
          {
            "full_move": "f3h4", 
            "mate": False, 
            "move": "Nh4", 
            "score": -1212.0
          }, 
          {
            "full_move": "f3e1", 
            "mate": False, 
            "move": "Ne1", 
            "score": -1355.0
          }
        ], 
        "answer": "Если сходишь правильно, можешь поставить мат."
      }, 
      "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2": {
        "possible_moves": [
          {
            "full_move": "g1f3", 
            "mate": False, 
            "move": "Nf3", 
            "score": 124.0
          }, 
          {
            "full_move": "b1c3", 
            "mate": False, 
            "move": "Nc3", 
            "score": 69.0
          }, 
          {
            "full_move": "g1e2", 
            "mate": False, 
            "move": "Ne2", 
            "score": 59.0
          }, 
          {
            "full_move": "g1h3", 
            "mate": False, 
            "move": "Nh3", 
            "score": -87.0
          }, 
          {
            "full_move": "b1a3", 
            "mate": False, 
            "move": "Na3", 
            "score": -122.0
          }
        ], 
        "best_moves": [], 
        "answer": "Возможное ходы e2-e3, e1-e3, e3-e5"
      }, 
      "r2qkb1r/ppp2ppp/2n2N2/8/6b1/P4N2/1PPPQPPP/R1B2RK1 b kq - 2 10": {
        "possible_moves": [], 
        "best_moves": [], 
        "answer": "Шах и мат! Ты победил! Поздравляю!"
      }, 
      "r1bqkb1r/ppp2ppp/2n5/8/4Nn2/P4N2/1PPPBPPP/R1BQK2R w KQkq - 1 8": {
        "possible_moves": [], 
        "best_moves": [
          {
            "full_move": "e1g1", 
            "mate": False, 
            "move": "O-O", 
            "score": 208.0
          }, 
          {
            "full_move": "e2f1", 
            "mate": False, 
            "move": "Bf1", 
            "score": 128.0
          }, 
          {
            "full_move": "h1g1", 
            "mate": False, 
            "move": "Rg1", 
            "score": 67.0
          }, 
          {
            "full_move": "d2d4", 
            "mate": False, 
            "move": "d4", 
            "score": 59.0
          }, 
          {
            "full_move": "e2c4", 
            "mate": False, 
            "move": "Bc4", 
            "score": 49.0
          }, 
          {
            "full_move": "e1f1", 
            "mate": False, 
            "move": "Kf1", 
            "score": 10.0
          }, 
          {
            "full_move": "h1f1", 
            "mate": True, 
            "move": "Rf1", 
            "score": 9.99
          }, 
          {
            "full_move": "g2g3", 
            "mate": False, 
            "move": "g3", 
            "score": -20.0
          }, 
          {
            "full_move": "e2b5", 
            "mate": False, 
            "move": "Bb5", 
            "score": -38.0
          }, 
          {
            "full_move": "h2h4", 
            "mate": False, 
            "move": "h4", 
            "score": -41.0
          }, 
          {
            "full_move": "h2h3", 
            "mate": False, 
            "move": "h3", 
            "score": -79.0
          }, 
          {
            "full_move": "f3g5", 
            "mate": False, 
            "move": "Nfg5", 
            "score": -86.0
          }, 
          {
            "full_move": "d2d3", 
            "mate": False, 
            "move": "d3", 
            "score": -98.0
          }, 
          {
            "full_move": "c2c3", 
            "mate": False, 
            "move": "c3", 
            "score": -124.0
          }, 
          {
            "full_move": "a1b1", 
            "mate": False, 
            "move": "Rb1", 
            "score": -126.0
          }, 
          {
            "full_move": "b2b3", 
            "mate": False, 
            "move": "b3", 
            "score": -143.0
          }, 
          {
            "full_move": "e4g3", 
            "mate": False, 
            "move": "Ng3", 
            "score": -159.0
          }, 
          {
            "full_move": "b2b4", 
            "mate": False, 
            "move": "b4", 
            "score": -163.0
          }, 
          {
            "full_move": "a1a2", 
            "mate": False, 
            "move": "Ra2", 
            "score": -177.0
          }, 
          {
            "full_move": "e4c3", 
            "mate": False, 
            "move": "Nc3", 
            "score": -189.0
          }, 
          {
            "full_move": "a3a4", 
            "mate": False, 
            "move": "a4", 
            "score": -200.0
          }, 
          {
            "full_move": "g2g4", 
            "mate": False, 
            "move": "g4", 
            "score": -200.0
          }, 
          {
            "full_move": "f3g1", 
            "mate": False, 
            "move": "Ng1", 
            "score": -238.0
          }, 
          {
            "full_move": "c2c4", 
            "mate": False, 
            "move": "c4", 
            "score": -239.0
          }, 
          {
            "full_move": "e4g5", 
            "mate": False, 
            "move": "Neg5", 
            "score": -250.0
          }, 
          {
            "full_move": "f3h4", 
            "mate": False, 
            "move": "Nh4", 
            "score": -325.0
          }, 
          {
            "full_move": "e4c5", 
            "mate": False, 
            "move": "Nc5", 
            "score": -344.0
          }, 
          {
            "full_move": "e2a6", 
            "mate": False, 
            "move": "Ba6", 
            "score": -345.0
          }, 
          {
            "full_move": "f3e5", 
            "mate": False, 
            "move": "Ne5", 
            "score": -416.0
          }, 
          {
            "full_move": "e2d3", 
            "mate": False, 
            "move": "Bd3", 
            "score": -423.0
          }, 
          {
            "full_move": "e4d6", 
            "mate": False, 
            "move": "Nd6+", 
            "score": -475.0
          }, 
          {
            "full_move": "e4f6", 
            "mate": False, 
            "move": "Nf6+", 
            "score": -510.0
          }, 
          {
            "full_move": "f3d4", 
            "mate": False, 
            "move": "Nd4", 
            "score": -594.0
          }
        ], 
        "answer": "Пожалуй стоит сделать рокировку."
      }, 
      "r1bqkb1r/ppp2ppp/2n5/8/4N3/P4N2/1PPPnPPP/R1BQ1RK1 w kq - 0 9": {
        "possible_moves": [], 
        "best_moves": [
          {
            "full_move": "d1e2", 
            "mate": False, 
            "move": "Qxe2", 
            "score": 192.0
          }, 
          {
            "full_move": "g1h1", 
            "mate": False, 
            "move": "Kh1", 
            "score": -295.0
          }
        ], 
        "answer": "Кажется вам поставили шах."
      }, 
      "r1bqkb1r/ppp2ppp/2n5/3np3/8/P1N2N2/1PPP1PPP/R1BQKB1R w KQkq - 0 6": {
        "possible_moves": [], 
        "best_moves": [
          {
            "full_move": "d1e2", 
            "mate": False, 
            "move": "Qe2", 
            "score": 76.0
          }, 
          {
            "full_move": "f1b5", 
            "mate": False, 
            "move": "Bb5", 
            "score": 75.0
          }, 
          {
            "full_move": "f1c4", 
            "mate": False, 
            "move": "Bc4", 
            "score": 37.0
          }, 
          {
            "full_move": "d2d4", 
            "mate": False, 
            "move": "d4", 
            "score": 0.0
          }, 
          {
            "full_move": "d2d3", 
            "mate": False, 
            "move": "d3", 
            "score": -12.0
          }, 
          {
            "full_move": "f3e5", 
            "mate": False, 
            "move": "Nxe5", 
            "score": -18.0
          }, 
          {
            "full_move": "f1e2", 
            "mate": False, 
            "move": "Be2", 
            "score": -38.0
          }, 
          {
            "full_move": "a1b1", 
            "mate": False, 
            "move": "Rb1", 
            "score": -72.0
          }, 
          {
            "full_move": "c3d5", 
            "mate": False, 
            "move": "Nxd5", 
            "score": -73.0
          }, 
          {
            "full_move": "h2h4", 
            "mate": False, 
            "move": "h4", 
            "score": -74.0
          }, 
          {
            "full_move": "f1d3", 
            "mate": False, 
            "move": "Bd3", 
            "score": -79.0
          }, 
          {
            "full_move": "b2b4", 
            "mate": False, 
            "move": "b4", 
            "score": -81.0
          }, 
          {
            "full_move": "h2h3", 
            "mate": False, 
            "move": "h3", 
            "score": -82.0
          }, 
          {
            "full_move": "a3a4", 
            "mate": False, 
            "move": "a4", 
            "score": -89.0
          }, 
          {
            "full_move": "f3g5", 
            "mate": False, 
            "move": "Ng5", 
            "score": -119.0
          }, 
          {
            "full_move": "b2b3", 
            "mate": False, 
            "move": "b3", 
            "score": -127.0
          }, 
          {
            "full_move": "g2g3", 
            "mate": False, 
            "move": "g3", 
            "score": -129.0
          }, 
          {
            "full_move": "h1g1", 
            "mate": False, 
            "move": "Rg1", 
            "score": -135.0
          }, 
          {
            "full_move": "a1a2", 
            "mate": False, 
            "move": "Ra2", 
            "score": -135.0
          }, 
          {
            "full_move": "c3e4", 
            "mate": False, 
            "move": "Ne4", 
            "score": -151.0
          }, 
          {
            "full_move": "c3b5", 
            "mate": False, 
            "move": "Nb5", 
            "score": -153.0
          }, 
          {
            "full_move": "f3g1", 
            "mate": False, 
            "move": "Ng1", 
            "score": -176.0
          }, 
          {
            "full_move": "c3e2", 
            "mate": False, 
            "move": "Ne2", 
            "score": -190.0
          }, 
          {
            "full_move": "c3a4", 
            "mate": False, 
            "move": "Na4", 
            "score": -199.0
          }, 
          {
            "full_move": "e1e2", 
            "mate": False, 
            "move": "Ke2", 
            "score": -299.0
          }, 
          {
            "full_move": "g2g4", 
            "mate": False, 
            "move": "g4", 
            "score": -333.0
          }, 
          {
            "full_move": "c3a2", 
            "mate": False, 
            "move": "Na2", 
            "score": -396.0
          }, 
          {
            "full_move": "c3b1", 
            "mate": False, 
            "move": "Nb1", 
            "score": -450.0
          }, 
          {
            "full_move": "f1a6", 
            "mate": False, 
            "move": "Ba6", 
            "score": -459.0
          }, 
          {
            "full_move": "f3h4", 
            "mate": False, 
            "move": "Nh4", 
            "score": -505.0
          }, 
          {
            "full_move": "f3d4", 
            "mate": False, 
            "move": "Nd4", 
            "score": -562.0
          }
        ], 
        "answer": "Ты только что спрашивал, в этот раз подумай сам. Ты же хочешь научиться играть."
      }
    }
    if state in game:
        return game[state]
    else:
        return ([], [], 'answer', False) 



@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

@app.route('/hint', methods=['POST'])
def hint():
    if request.method == 'POST':
        data = request.get_json()
        if not ('board' in data):
            return answer([], [], 'Error: no board information sent', False)
        state = data['board']
        question = data['question']
        if question != '':
            parse_question(question);
        new_answer = get_answer(state)
        mate = False
        return json_answer(new_answer['best_moves'], new_answer['possible_moves'], new_answer['answer'], mate)
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


