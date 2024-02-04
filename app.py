from flask import Flask, render_template, request, jsonify, session
from boggle import Boggle


app = Flask(__name__)
app.config['SECRET_KEY'] = 'porsche911'

boggle_game = Boggle()

@app.route('/')
def homepage():
    """Home Page"""
    board = boggle_game.make_board()
    session['board'] = board

    return render_template('index.html', board=board)
    

@app.route('/check-word')
def check_word():
    """Checking the words"""
    word = request.args['word']
    board = session['board']
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})