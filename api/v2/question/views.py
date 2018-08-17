'''question views '''
from flask import make_response, jsonify, request, Blueprint
from flask.views import MethodView
from api.v2.question.question import Question
from api.v2.common.validators import does_object_exist, question_quality
from api.v2.common.SQL import select_no_condition, select_all


question_blueprint = Blueprint('question', __name__)


class Questions(MethodView):
    ''' a class for asking question and fetching questions'''
    @classmethod
    def post(cls, user_id=1):
        ''' method for asking a question'''
        quiz_title = request.json.get('title')
        quiz_body = request.json.get('body')
        if not quiz_title:
            return make_response(jsonify({'message': 'Provide question title, or check for spelling errors'})), 400
        if not quiz_body:
            return make_response(jsonify({'message': 'Provide question description'})), 409
        if does_object_exist(column='title', table='questions', col_name='title', param=quiz_title):
            return make_response(jsonify(
                {'message': 'You have asked this question before'})), 409
        quality_check = question_quality(string1=quiz_title, string2=quiz_body)
        if quality_check:
            return make_response(jsonify({'message': quality_check})), 409
        question = Question(quiz_title, quiz_body, user_id)
        question.save_question()
        return make_response(jsonify({'message': 'Succesfully asked a question'})), 201

    @classmethod
    def get(cls):
        ''' a method  for fetching all questions'''
        if not select_no_condition('questions'):
            return make_response(jsonify({'message': 'There are no questions available'})), 404
        return make_response(jsonify({'questions': select_no_condition('questions')})), 200


class FetchQuestion(MethodView):
    ''' a class for fetching a single question'''
    @classmethod
    def get(cls, questionId):
        ''' a method for fetching a single question'''
        question = select_all('questions', 'qId', questionId)
        answers = select_all('answers', 'questionId', questionId)
        if question:
            if answers:
                return make_response(jsonify(
                    {'question': question[0],'answes':answers}
                )), 200
            return make_response(jsonify({'question':question[0], 'answers':'This  question has no answers'})), 200
        return make_response(jsonify({'message': 'The question does not exist, seems like it is deleted'}))

question_blueprint.add_url_rule(
    '/questions/<questionId>', view_func=FetchQuestion.as_view('fetch-question'), methods=['GET'])
question_blueprint.add_url_rule(
    '/questions', view_func=Questions.as_view('questions'), methods=['POST','GET'])
