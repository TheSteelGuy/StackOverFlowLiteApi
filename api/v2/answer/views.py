from datetime import datetime
from flask import Blueprint, request, jsonify, make_response
from flask.views import MethodView
from api.v2.answer.answer import Answer
from api.v2.common.validators import does_object_exist, content_quality, token_required
from api.v2.common.SQL import select_all, accept_answer, update_answer, upvote_answer, prevent_own_answer_accept_vote

answer_blueprint = Blueprint('answer', __name__)


class AnswerQuestion(MethodView): 
    ''' a class for answer related methods'''
    @classmethod
    @token_required
    def post(cls, questionId, user_id):
        ''' method for answering a question'''
        answer_body = request.json.get('answer')
        if not answer_body:
            return make_response(jsonify({'message': 'Provide an answer'})), 400
        quiz_author = does_object_exist(
            column='author_id', table='questions', col_name='question_id', param=questionId)
        if not quiz_author:
            return make_response(jsonify(
                {'message': 'The question does not exist'})), 404
        if does_object_exist(column='description', table='answers', col_name='description', param=answer_body):
            return make_response(jsonify(
                {'message': 'You cannot give the same answer twice'})), 409
        if content_quality(answer_body, content='answer'):
            return make_response(jsonify({'message': content_quality(answer_body, content='answer')})), 409
        ans = Answer(answer_body, questionId, user_id,
                     quiz_author['author_id'])
        answer = ans.save_answer()
        return make_response(jsonify({'message': 'Succesfully answerd the question','answer':answer})), 201


class UpdateAcceptAnswer(MethodView):
    '''accept or update answer class'''
    @classmethod
    @token_required
    def put(cls, questionId, answerId, user_id):
        '''accept an answer as your preffered or update answer'''
        record = select_all('answers', 'answer_id', answerId)
        if record[0]['question_id'] != int(questionId):
            return make_response(jsonify({'message': 'The answer you are looking for does not exist'})), 404
        if record[0]['questionauthor_id'] != user_id and record[0]['answerauthor_id'] != user_id:
            return make_response(jsonify(
                {'message':'You cannot accept this answer since the question does not belong to you'})), 401
        my_answer = prevent_own_answer_accept_vote(int(answerId), user_id)
        action = request.json.get('action')
        if record[0]['questionauthor_id'] == user_id and action == 'accept':
            if my_answer:
                return make_response(jsonify({'message' : 'You cannot accept your own answer'})), 409
            return make_response(jsonify(
                        {'message': accept_answer(answerId)})), 200
        action = request.json.get('action')
        if record[0]['answerauthor_id'] == user_id and action == 'comment':
            answer_body = request.json.get('answer')
            if not answer_body:
                return make_response(jsonify({'mesage': 'Provide an answer'})), 400
            if content_quality(answer_body, content='answer'):
                return make_response(jsonify({'message': content_quality(answer_body, content='answer')})), 409
            update = update_answer(answerId, answer_body)
            return make_response(jsonify({'message': 'Answer updated in success', 'update' : update })), 200
        else:
            return make_response(jsonify({'message' : 'You cannot accept this answer since the question does not belong to you'})), 409 


class VoteAnswer(MethodView):
    ''' class vote'''
    @classmethod
    @token_required
    def get(cls, questionId, vote, answerId, user_id):
        ''' upvote or downvote an answer'''
        question_list = select_all('questions', 'question_id', questionId)
        answer_list = select_all('answers', 'answer_id', answerId)
        if prevent_own_answer_accept_vote(int(answerId), user_id):
            return make_response(jsonify({'message' : 'You cant vote your answer!'})), 409
        if vote == 'upvote':
            count = 1
            if not answer_list:
                return make_response(jsonify({'message': 'The answer you are looking for does not exist'})), 404
            if not question_list:
                return make_response(jsonify({'message': 'The question you are looking for does not exist'})), 404
            return make_response(jsonify(upvote_answer(str(answerId), count))), 200
        if vote == 'downvote':
            count = -1
            if not answer_list:
                return make_response(jsonify({'message': 'The answer you are looking for does not exist'})), 404
            if not question_list:
                return make_response(jsonify({'message': 'The question you are looking for does not exist'})), 404
            return make_response(jsonify(upvote_answer(str(answerId), count))), 200
        return make_response(jsonify({'message': 'You have made an invalid choice,upvote or downvote'})), 409


answer_blueprint.add_url_rule(
    '/questions/<questionId>/answers/<answerId>/<vote>', view_func=VoteAnswer.as_view('vote-answer'), methods=['GET'])
answer_blueprint.add_url_rule(
    '/questions/<questionId>/answers', view_func=AnswerQuestion.as_view('answer-question'), methods=['POST', 'GET'])
answer_blueprint.add_url_rule(
    '/questions/<questionId>/answers/<answerId>',
    view_func=UpdateAcceptAnswer.as_view('accept-update-answer'), methods=['PUT'])
