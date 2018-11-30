# -*- coding: utf-8 -*-

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
def parse_question(question, new_turn):
    skinut' ' pastebin
    answer = ''
    if question[:16].lower() == 'какой лучший ход':
        best_move = new_turn[best_moves][0]
        if 'x' in best_move:
           # answer = 'Предлагаю съесть' + 
        else:
            #answer = 'Предлагаю сходить ' + piece() + ' на ' + cell()
    return answer

def json_answer(best_moves, possible_moves, answer, mate):
    return jsonify({
        'best_moves': best_moves,
        'possible_moves': possible_moves,
        'answer': answer,
        'mate' : mate
    })

def get_answer(state):
    with open('game-temp.json') as f:
        game = json.load(f)
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
            return json_answer([], [], 'Error: no board information sent', False)
        state = data['board']
        question = data['question']
        new_answer = get_answer(state)
        mate = False
        if question != '':
            text = generate_text(question, new_answer)
        new_answer = get_answer(state)
        mate = False
        # return json_answer(new_answer['best_moves'], new_answer['possible_moves'], text, mate)
        return json_answer(new_answer['best_moves'], new_answer['possible_moves'], new_answer['answer'], mate)
    else:
        return json_answer([], [], 'Ошибка!', False)
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


