from flask import Flask, render_template, request, session, flash, json, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newlywed.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = 'newweds'

class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Answer1 = db.Column(db.String(255))
    Answer2 = db.Column(db.String(255))
    Answer3 = db.Column(db.String(255))
    Answer4 = db.Column(db.String(255))
    Answer5 = db.Column(db.String(255))
    Answer6 = db.Column(db.String(255))
    Answer7 = db.Column(db.String(255))
    Answer8 = db.Column(db.String(255))
    Answer9= db.Column(db.String(255))
    Answer10 = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
class Guesses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Guess1 = db.Column(db.String(255))
    Guess2 = db.Column(db.String(255))
    Guess3 = db.Column(db.String(255))
    Guess4 = db.Column(db.String(255))
    Guess5 = db.Column(db.String(255))
    Guess6 = db.Column(db.String(255))
    Guess7 = db.Column(db.String(255))
    Guess8 = db.Column(db.String(255))
    Guess9 = db.Column(db.String(255))
    Guess10 = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('main.html')

@app.route('/on_answers', methods=['POST'])
def on_answers():
    new_answers = Answers(Answer1=request.form['question1'],Answer2=request.form['question2'],Answer3=request.form['question3'],Answer4=request.form['question4'],Answer5=request.form['question5'],Answer6=request.form['question6'],Answer7=request.form['question7'],Answer8=request.form['question8'],Answer9=request.form['question9'],Answer10=request.form['question10'])
    db.session.add(new_answers)
    db.session.commit()
    if new_answers:
        return redirect('/guesses')
    else:
        return redirect('/game')

@app.route('/guesses')
def guesses():
    return render_template('game.html')

@app.route('/on_guesses', methods=['POST'])
def on_guesses():
    new_guesses = Guesses(Guess1=request.form['question1'],Guess2=request.form['question2'],Guess3=request.form['question3'],Guess4=request.form['question4'],Guess5=request.form['question5'],Guess6=request.form['question6'],Guess7=request.form['question7'],Guess8=request.form['question8'],Guess9=request.form['question9'],Guess10=request.form['question10'])
    db.session.add(new_guesses)
    db.session.commit()
    if new_guesses:
        return redirect('/results')
    else:
        return redirect('/guesses')

@app.route('/results')
def results():
    corrects = Answers.query.all()
    maybes = Guesses.query.all()
    return render_template('results.html', corrects=corrects, maybes=maybes)

@app.route('/restart')
def restart():
    answer_delete = Answers.query.get(1)
    db.session.delete(answer_delete)
    db.session.commit()

    guess_delete = Guesses.query.get(1)
    db.session.delete(guess_delete)
    db.session.commit()

    return redirect('/')
if __name__ == "__main__":
    app.run(debug=True)
