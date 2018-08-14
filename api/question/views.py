'''question views '''
from flask import request, Blueprint
from flask.views import MethodView
from api.models.question import Question

question_blueprint = Blueprint('question', __name__)

questions = list()


class AskQuestion(MethodView):
    ''' a class for asking question and fetching all questions'''

    def post(self):
        ''' method for asking a question'''
        pass

    def get(self):
        ''' a method  for fetching all questions'''
        pass


class FetchQuestion(MethodView):
    ''' a class for fetching a single question'''

    def get(self):
        ''' a method for fetching a single question'''
        pass




question_blueprint.add_url_rule(
    '/questions', view_func=AskQuestion.as_view('ask-question'), methods=['POST'])
question_blueprint.add_url_rule(
    '/questions', view_func=AskQuestion.as_view('fetch-questions'), methods=['GET'])
question_blueprint.add_url_rule(
    '/questions/<questionId>', view_func=FetchQuestion.as_view('fetch-question'), methods=['GET'])
