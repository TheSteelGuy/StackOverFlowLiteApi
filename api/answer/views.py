from flask import Blueprint
from flask.views import MethodView
from api.models.answer import Answer

answer_blueprint = Blueprint('answer', __name__)

answers = list()


class AnswerQuestion(MethodView):
    ''' a class for answering a question'''

    def post(self):
        ''' method for answering a question'''
        pass
    
answer_blueprint.add_url_rule(
    '/questions/<questionId>/answers',view_func=AnswerQuestion.as_view('answer-question'),methods=['POST'])

