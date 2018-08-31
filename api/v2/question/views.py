'''question views '''
from flask import make_response, jsonify, request, Blueprint
from flask.views import MethodView

from api.v2.question.question import Question
from api.v2.common.validators import does_object_exist, question_quality, does_list_exist
from api.v2.common.validators import token_required, content_quality
from api.v2.common.SQL import select_no_condition, select_all, delete_, prevent_unauthorized_deletes
from api.v2.common.SQL import fetch_question, fetch_questions, fetch_user_question

question_blueprint = Blueprint('question', __name__)


class Questions(MethodView):
    ''' a class for asking question and fetching questions'''
    @classmethod
    @token_required
    def post(cls, user_id):
        ''' method for asking a question'''
        quiz_title = request.json.get('title')
        quiz_body = request.json.get('body')
        if not quiz_title:
            return make_response(jsonify({'message': 'Provide question title'})), 400
        if not quiz_body:
            return make_response(jsonify({'message': 'Provide question description'})), 409
        if does_object_exist(column='title', table='questions', col_name='title', param=quiz_title):
            return make_response(jsonify(
                {'message': 'Similar question exist'})), 409
        if does_object_exist(column='body', table='questions', col_name='body', param=quiz_body):
            return make_response(jsonify(
                {'message': 'Similar question exist'})), 409

        quality_check = question_quality(string1=quiz_title, string2=quiz_body)
        if quality_check:
            return make_response(jsonify({'message': quality_check})), 409
        question = Question(quiz_title, quiz_body, user_id)
        question.save_question()
        return make_response(jsonify({'message': 'Succesfully asked a question'})), 201

    @classmethod
    def get(cls):
        ''' a method  for fetching all questions'''
        if not fetch_questions():
            return make_response(jsonify({'message': 'There are no questions available'})), 404
        return make_response(jsonify({'questions': fetch_questions()})), 200


class FetchQuestion(MethodView):
    ''' a class for fetching a single question'''
    @classmethod
    def get(cls, questionId):
        ''' a method for fetching a single question'''
        join = fetch_question()
        if join:
            question = does_list_exist(join, 'question_id', int(questionId))
            if not question:
                return make_response(jsonify(
                    {'message': 'The question does not exist'})), 404
            return make_response(jsonify({'question': question})), 200
        return make_response(jsonify({'message': 'The question does not exist'})), 404

    @classmethod
    @token_required
    def delete(cls, user_id, questionId):
        '''deletes question from database'''
        if not does_object_exist(column='question_id', table='questions', col_name='question_id', param=questionId):
            return make_response(jsonify(
                {'message': 'Question does not exist'})), 409
        if prevent_unauthorized_deletes(questionId) != user_id:
            return make_response(jsonify(
                {'message': 'You are not authorised to delete this question{},{}'.format(user_id, prevent_unauthorized_deletes(questionId))})), 401
        delete_(questionId)
        return make_response(jsonify(
            {'message': "Succefully deleted this question"})), 200


class UserQuestion(MethodView):
    '''user questions related actions'''
    @classmethod
    @token_required
    def get(cls, user_id):
        '''get all question belongin t a specific user'''
        records = fetch_user_question(user_id)
        if not records:
            return make_response(jsonify({'message': 'You have no questions yet'})), 404
        return make_response(jsonify({'questions': records})), 200


question_blueprint.add_url_rule(
    '/questions/<questionId>', view_func=FetchQuestion.as_view('fetch-question'), methods=['GET', 'DELETE'])
question_blueprint.add_url_rule(
    '/questions', view_func=Questions.as_view('questions'), methods=['POST', 'GET'])
question_blueprint.add_url_rule(
    'user/questions', view_func=UserQuestion.as_view('user-questions'), methods=['GET'])
