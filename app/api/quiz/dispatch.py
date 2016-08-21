# Import global context
from flask import request

# Import flask dependencies
from flask import Blueprint
from flask_login import login_required, login_user, current_user

# Import app-based dependencies
from ...util import utils

# Import core libraries
from ...lib.database import db
from ...lib.textteaser import TextTeaser
from ...lib.decorators import make_response
from ...lib.error_handler import FailedRequest
from ...lib.quiz_maker import extract_questions

from newspaper import Article

from .model import Quiz, Questions


# Define the blueprint: 'quiz', set its url prefix: app.url/quiz
mod_quiz = Blueprint('quiz', __name__)


@mod_quiz.route('/generate_from_text', methods=['POST'])
@make_response
def add_quiz_from_text(res):
    params = utils.get_data(
        [   
            'text', 'title'
        ], [], 
        request.values)
    
    tt = TextTeaser()

    summarized = tt.summarize(params['title'], params['text'], "Undefined", "Undefined", 20)

    return res.send(summarized)

@mod_quiz.route('/generate_from_article', methods=['POST'])
@make_response
def add_quiz(res):
    params = utils.get_data(
        [   
            'article_url'
        ], [], 
        request.values)
    
    article = Article(params['article_url'])
    article.download()
    article.parse()

    tt = TextTeaser()

    summarized = tt.summarize(article.title, article.text, "Undefined", "Undefined", 20)
    quiz_items = extract_questions(summarized, article.title)

    quiz_obj = {
        'article_url': params['article_url'],
        'article_title': article.title,
        'article_summary': ' '.join(summarized)
    }

    ### Add to the quiz database
    quiz = Quiz(quiz_obj)
    db.session.add(quiz)
    db.session.commit() 

    for qi in quiz_items:
        tmp_obj = {
            'quiz_id': quiz.id,
            'question_phrase': qi['item'], 
            'choices': ','.join(qi['choices']),
            'correct_choice': qi['correct_choice'],
            'answer': qi['answer']
        }
        db.session.add(Questions(tmp_obj))

    db.session.commit() 

    res_obj = {
        'quiz_id': quiz.id,
        'questions': quiz_items,
        'article_title': quiz.article_title,
        'article_summary': quiz.article_summary
    }

    return res.send(res_obj)


@mod_quiz.route('/<quiz_id>', methods=['GET'])
@make_response
def get_quiz(res, quiz_id):
    """ gets a certain quiz with
        all the questionaires
    """
    quiz = Quiz.query.filter_by(id=quiz_id).first()

    if not quiz:
        raise FailedRequest('Quiz not found', 404)

    questions = Questions.query.filter_by(quiz_id=quiz_id).all()

    if not questions:
        raise FailedRequest('Questions not found', 404)

    questions = list(map(lambda qs: {
            'id': qs.id,
            'item': qs.question_phrase,
            'choices': qs.choices.split(',')
        }, questions)
    )

    res_obj = {
        'quiz_id': quiz.id,
        'questions': questions,
        'article_title': quiz.article_title,
        'article_summary': quiz.article_summary
    }

    return res.send(res_obj)

@mod_quiz.route('/answer_key/<quiz_id>', methods=['GET'])
@make_response
def get_quiz_answer(res, quiz_id):
    """ gets a certain quiz with
        all the questionaires
    """
    quiz = Quiz.query.filter_by(id=quiz_id).first()

    if not quiz:
        raise FailedRequest('Quiz not found', 404)

    questions = Questions.query.filter_by(quiz_id=quiz_id).all()

    if not questions:
        raise FailedRequest('Questions not found', 404)

    questions = list(map(lambda qs: {
            'id': qs.id,
            'answer': qs.correct_choice,
            'choices': qs.choices.split(',')
        }, questions)
    )

    res_obj = {
        'quiz_id': quiz.id,
        'answers': questions,
        'article_title': quiz.article_title,
        'article_summary': quiz.article_summary
    }

    return res.send(res_obj)














