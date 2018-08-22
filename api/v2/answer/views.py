from datetime import datetime
from flask import Blueprint, request, jsonify, make_response
from flask.views import MethodView
from api.v2.answer.answer import Answer
from api.v2.common.validators import does_object_exist, content_quality, token_required
from api.v2.common.SQL import select_all, accept_answer, update_answer

answer_blueprint = Blueprint('answer', __name__)


class AnswerQuestion(MethodView):
    ''' a class for answer related methods'''
    @classmethod
    @token_required
    def post(cls, questionId, user_id):
        ''' method for answering a question'''
        answer_body = request.json.get('answer')
        if not answer_body:
            return make_response(jsonify({'mesage': 'Provide an answer'})), 400
        quiz_author = does_object_exist(column='authorId', table='questions', col_name='qId', param=questionId)
        if not quiz_author:
            return make_response(jsonify(
                {'message': 'The question does not exist, seems like it is deleted'})), 404
        if does_object_exist(column='description', table='answers', col_name='description', param=answer_body):
            return make_response(jsonify(
                {'message': 'You cannot give the same answer twice'})), 409
        if content_quality(answer_body, content='answer'):
            return make_response(jsonify({'message': content_quality(answer_body, content='answer')})), 409
        ans = Answer(answer_body, questionId, user_id, quiz_author['authorid'])
        ans.save_answer()
        return make_response(jsonify({'message': 'Succesfully answerd the question'})), 201

class UpdateAcceptAnswer(MethodView):
    '''accept or update answer class'''
    @classmethod
    @token_required
    def put(cls, questionId, answerId, user_id):
        '''accept an answer as your preffered or update answer'''
        try:
            record = select_all('answers', 'aid', answerId)
            if record[0]['questionid'] != int(questionId):
                return make_response(jsonify({'message': 'The answer you are looking for does not exist'})), 404
            if record[0]['questionauthorid'] == user_id:
                return make_response(jsonify(
                    {'message':accept_answer(answerId)})), 200
            if record[0]['answerauthorid'] == user_id:
                answer_body = request.json.get('answer')
                if not answer_body:
                    return make_response(jsonify({'mesage': 'Provide an answer'})), 400
                if content_quality(answer_body, content='answer'):
                    return make_response(jsonify({'message': content_quality(answer_body, content='answer')})), 409
                update_answer(answerId, answer_body)
                return make_response(jsonify({'message': 'Answer updated in success'})), 200
        except TypeError:
            return make_response(jsonify({'message': 'The answer you are looking for does not exist'})), 404
       
answer_blueprint.add_url_rule(
    '/questions/<questionId>/answers', view_func=AnswerQuestion.as_view('answer-question'), methods=['POST', 'GET'])
answer_blueprint.add_url_rule(
    '/questions/<questionId>/answers/<answerId>',
    view_func=UpdateAcceptAnswer.as_view('accept-update-answer'), methods=['PUT'])
   
