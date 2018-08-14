'''question views '''
from flask import make_response, jsonify, request, Blueprint
from flask.views import MethodView
from api.v1.question.question import Question
from api.v1.common.validators import does_object_exist, question_quality


question_blueprint = Blueprint('question', __name__)

questions = list()


class AskQuestion(MethodView):
    ''' a class for asking question and fetching all rides'''
    @classmethod
    def post(cls):
        ''' method for asking a question'''
        quiz_title = request.json.get('title')
        quiz_body = request.json.get('body')
        if not quiz_title:
            return make_response(jsonify({'message': 'Provide question title, or check for spelling errors'})), 400
        if not quiz_body:
            return make_response(jsonify({'message': 'Provide question description'})), 409
        if does_object_exist(questions, 'title', quiz_title):
            return make_response(jsonify(
                {'message': 'You have asked this question before'})), 409
        quality_check = question_quality(string1=quiz_title, string2=quiz_body)
        if quality_check:
            return make_response(jsonify({'message': quality_check})), 409
        id_count = 1
        for item in questions:
            id_count += 1
        question = Question(quiz_title, quiz_body)
        quiz_dict = question.serialize_question(id_count)
        questions.append(quiz_dict)
        return make_response(jsonify({'message': 'Succesfully asked a question'})), 201

    @classmethod
    def get(cls):
        ''' a method  for fetching all questions'''
        if not questions:
            return make_response(jsonify({'message': 'There are no questions available'})), 404
        return make_response(jsonify({'questions': questions})), 200

    @classmethod
    def delete(cls, questionId):
        '''delete question'''
        quiz = does_object_exist(questions, 'questionId', int(questionId))
        if quiz:
            questions.remove(quiz[0])
            return make_response(jsonify(
                {'message': 'Question deleted succefully'}
            )), 200
        return make_response(jsonify(
            {'message': 'You must have deleted the question already, it doesnt exist'}
        )), 404


class FetchQuestion(MethodView):
    ''' a class for fetching a single question'''
    @classmethod
    def get(cls, questionId):
        ''' a method for fetching a single question'''
        question = does_object_exist(questions, 'questionId', int(questionId))
        if question:
            return make_response(jsonify({'question': question[0]})), 200
        return make_response(jsonify({'message': 'The question does not exist, seems like it is deleted'}))


question_blueprint.add_url_rule(
    '/questions', view_func=AskQuestion.as_view('ask-question'), methods=['POST'])
question_blueprint.add_url_rule(
    '/questions', view_func=AskQuestion.as_view('fetch-questions'), methods=['GET'])
question_blueprint.add_url_rule(
    '/questions/<questionId>', view_func=FetchQuestion.as_view('fetch-question'), methods=['GET'])
question_blueprint.add_url_rule(
    '/questions/<questionId>/delete', view_func=AskQuestion.as_view('delete-question'), methods=['DELETE'])
