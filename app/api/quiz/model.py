# Imports
from ...util import utils
from ...lib.database import db

class Quiz(db.Model):

    __tablename__ = 'quiz'

    id = db.Column(db.Integer, primary_key=True)
    article_url = db.Column(db.String(400), nullable=False)
    article_title = db.Column(db.String(400), nullable=False)
    article_summary = db.Column(db.Text, nullable=False)
    
    def __init__(self, obj):
        self.article_url = obj['article_url']
        self.article_title = obj['article_title']
        self.article_summary = obj['article_summary']


class Questions(db.Model):

    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, nullable=False)
    question_phrase = db.Column(db.Text, nullable=False)
    is_multiple_choice = db.Column(db.Boolean, nullable=False, default=True)
    choices = db.Column(db.Text, nullable=False)
    correct_choice = db.Column(db.Integer, nullable=False)
    answer = db.Column(db.String(64), nullable=False)
    
    def __init__(self, obj):
        self.quiz_id = obj['quiz_id']
        self.question_phrase = obj['question_phrase']
        self.is_multiple_choice = True
        self.choices = obj['choices']
        self.correct_choice = obj['correct_choice']
        self.answer = obj['answer']