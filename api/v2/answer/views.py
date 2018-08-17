from datetime import datetime
from flask import Blueprint, request, jsonify, make_response
from flask.views import MethodView
from api.v2.answer.answer import Answer
from api.v2.common.validators import does_object_exist, content_quality

answer_blueprint = Blueprint('answer', __name__)

class AnswerQuestion(MethodView):
    ''' a class for answer related methods'''
    @classmethod
    def post(cls, questionId):
        ''' method for answering a question'''
        answer_body = request.json.get('answer')
        if not answer_body:
            return make_response(jsonify({'mesage': 'Provide an answer'})), 400
        if not does_object_exist(column='title', table='questions', col_name='qId', param=questionId):
            return make_response(jsonify({'message': 'The question does not exist, seems like it is deleted'})), 404
        if does_object_exist(column='description', table='answers', col_name='description', param=answer_body):
            return make_response(jsonify(
                {'message': 'You cannot give the same answer twice'})), 409
        if content_quality(answer_body, content='answer'):
            return make_response(jsonify({'message': content_quality(answer_body, content='answer')})), 409
        ans = Answer(answer_body, questionId)
        ans.save_answer()
        return make_response(jsonify({'message': 'Succesfully answerd the question'})), 201


answer_blueprint.add_url_rule(
    '/questions/<questionId>/answers', view_func=AnswerQuestion.as_view('answer-question'), methods=['POST', 'GET'])
