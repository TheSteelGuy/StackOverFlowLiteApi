'''comment related views '''
from flask import make_response, jsonify, request, Blueprint
from flask.views import MethodView
from api.v1.comment.comment import Comment
from api.v1.common.validators import does_object_exist, content_quality
from api.v1.answer.views import questions
from api.v1.answer.views import answers


comment_blueprint = Blueprint('comment', __name__)

comments = list()


class MyComment(MethodView):
    ''' a class for  comment on an answer'''
    @classmethod
    def post(cls, questionId, answerId):
        ''' method for asking a question'''
        question = does_object_exist(questions, 'questionId', int(questionId))
        answer = does_object_exist(answers, 'answerId', int(answerId))
        if not question:
            return make_response(jsonify({'message':'Question with that id does not exist'})), 404
        if not answer:
            return make_response(jsonify({'message':'Answer with that id does not exist'})), 404
        if not request.get_json():
            return make_response(jsonify({'message':'Invalid request format, provide json request'})), 400
        comment_body = request.json.get('comment')
        if not comment_body:
            return make_response(jsonify({'message': 'Provide comment description'})), 400
        if does_object_exist(comments, 'comment', comment_body):
            return make_response(jsonify(
                {'message': 'This comment is already recorded'})), 409
        quality_check = content_quality(comment_body, content='comment')
        if quality_check:
            return make_response(jsonify({'message': quality_check})), 409
        id_count = 1
        for item in comments:
            id_count += 1
        comment = Comment(comment_body)
        comment_dict = comment.serialize_comment(id_count)
        comments.append(comment_dict)
        return make_response(jsonify({'message': 'Succesfully added a comment'})), 201


comment_blueprint.add_url_rule(
    '/questions/<questionId>/answers/<answerId>/comments', view_func=MyComment.as_view('comments'), methods=['POST'])
