# -*- coding: utf-8 -*-

#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify
from json import loads, dumps
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from flask_cors import CORS
from hint_utils import HintService
from pandas import read_csv
import chess
import chess.uci

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

last_board = None
last_hint = None
@app.route('/hint', methods=['POST'])
def hint():
    global last_board
    global last_hint
    if request.method == 'POST':
        data = request.get_json()
        if (last_hint != None) and (last_board != None) and (len(last_hint['best_moves']) != 0) and (last_hint['answer'] == ''):
            last_best = last_hint['best_moves'][0]
            current_board = chess.BaseBoard(data['board'].split()[0])
            if ' b ' in data['board']:
                if current_board.piece_at(chess.SQUARE_NAMES.index(last_best['full_move'][2:4])) == last_board.piece_at(chess.SQUARE_NAMES.index(last_best['full_move'][:2])):
                    return jsonify({
                        'answer' : 'Молодец, хороший ход.',
                        'best_moves' : [],
                        "possible_moves":[],
                        "mate":False
                        })
        if not 'board' in data:
            return {}
        csv = read_csv("data/dataset.tsv", sep='\t')
        hint = HintService(knowledge=csv)
        json = hint.ask(data['board'], data['question'])
        last_board = chess.BaseBoard(data['board'].split()[0])
        last_hint = loads(json)
        return json
    else:
        return {}

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
    app.run(host='0.0.0.0', port=port, debug=True)


