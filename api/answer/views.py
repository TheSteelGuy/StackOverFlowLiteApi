from flask import Blueprint, request, jsonify, make_response
from flask.views import MethodView
from api.models.answer import Answer
from api.common.validators import does_object_exist, content_quality
from api.question.views import questions

answer_blueprint = Blueprint('answer', __name__)

answers = list()


class AnswerQuestion(MethodView):
    ''' a class for answering a question'''

    def post(self, questionId):
        ''' method for answering a question'''
        answer_body = request.json.get('answer')
        if not answer_body:
            return make_response(jsonify({'mesage': 'Provide an answer'})), 400
        if not does_object_exist(questions,'questionId',int(questionId)):
            return make_response(jsonify({'message':'The question does not exist, seems like it is deleted'})), 404
        if does_object_exist(answers, 'answer', answer_body):
            return make_response(jsonify(
                {'message': 'You cannot give the same answer twice'})), 409
        if content_quality(answer_body, content='answer'):
            return make_response(jsonify({'message': content_quality(answer_body, content='answer')})), 409
        id_count = 1
        for item in answers:
            id_count += 1
        answer = Answer(answer_body)
        answer_dict = answer.serialize_answer(id_count)
        answers.append(answer_dict)
        return make_response(jsonify({'message': 'Succesfully answerd the question'})), 201 


answer_blueprint.add_url_rule(
    '/questions/<questionId>/answers', view_func=AnswerQuestion.as_view('answer-question'), methods=['POST'])
