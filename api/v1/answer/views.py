from datetime import datetime
from flask import Blueprint, request, jsonify, make_response
from flask.views import MethodView
from api.v1.answer.answer import Answer
from api.v1.common.validators import does_object_exist, content_quality
from api.v1.question.views import questions

answer_blueprint = Blueprint('answer', __name__)

answers = list()


class AnswerQuestion(MethodView):
    ''' a class for answer related methods'''
    @classmethod
    def post(cls, questionId):
        ''' method for answering a question'''
        if not request.get_json():
            return make_response(jsonify({'message':'Invalid request format, provide json request'})), 400
        answer_body = request.json.get('answer')
        if not answer_body:
            return make_response(jsonify({'mesage': 'Provide an answer'})), 400
        if not does_object_exist(questions, 'questionId', int(questionId)):
            return make_response(jsonify({'message': 'The question does not exist, seems like it is deleted'})), 404
        if does_object_exist(answers, 'answer', answer_body):
            return make_response(jsonify(
                {'message': 'You cannot give the same answer twice'})), 409
        if content_quality(answer_body, content='answer'):
            return make_response(jsonify({'message': content_quality(answer_body, content='answer')})), 409
        id_count = 1
        for item in answers:
            id_count += 1
        answer = Answer(answer_body)
        answer_dict = answer.serialize_answer(
            id_count, questionId, datetime.now())
        answers.append(answer_dict)
        return make_response(jsonify({'message': 'Succesfully answerd the question'})), 201

    @classmethod
    def get(cls, questionId):
        '''fetch answers for a question'''
        answers_list = does_object_exist(answers, 'questionId', questionId)
        if not answers_list:
            return make_response(jsonify({'message': 'This question has no answers yet'})), 404
        return make_response(jsonify({'answers': answers_list})), 200

    @classmethod
    def put(cls, questionId, answerId):
        '''accept an answer as your preffered'''
        answer_list = does_object_exist(answers, 'answerId', int(answerId))
        if answer_list:
            if answer_list[0]['accepted']:
                return make_response(jsonify({'message': 'You have already accepted this answer'})), 409
            answer_list[0]['accepted'] = True
            return make_response(jsonify(
                {'message': 'Succesfully accepted this answer on {}'.format(
                    answer_list[0]['date_accepted'])}
            )), 200
        return make_response(jsonify({'message': 'The answer you are looking for does not exist'})), 404


class VoteAnswer(MethodView):
    ''' class vote'''
    @classmethod
    def get(cls, questionId, vote, answerId,):
        ''' upvote or downvote an answer'''
        answer_list = does_object_exist(answers, 'answerId', int(answerId))
        if vote == 'upvote':
            if answer_list:
                answer_list[0]['votes'] += 1
                return make_response(jsonify({'votes': answer_list[0]['votes']})), 200
            return make_response(jsonify({'message': 'The answer you are looking for does not exist'})), 404
        if vote == 'downvote':
            if answer_list:
                answer_list[0]['votes'] -= 1
                return make_response(jsonify({'votes': answer_list[0]['votes']})), 200
            return make_response(jsonify({'message': 'The answer you are looking for does not exist'})), 404
        return make_response(jsonify({'message': 'You have made an invalid choice,upvote or downvote'})), 409


answer_blueprint.add_url_rule(
    '/questions/<questionId>/answers', view_func=AnswerQuestion.as_view('answer-question'), methods=['POST', 'GET'])
answer_blueprint.add_url_rule(
    '/questions/<questionId>/answers/<answerId>', view_func=AnswerQuestion.as_view('accept-answer'), methods=['PUT', 'GET'])
answer_blueprint.add_url_rule(
    '/questions/<questionId>/answers/<answerId>/<vote>', view_func=VoteAnswer.as_view('vote-answer'), methods=['GET'])
