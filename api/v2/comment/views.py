'''comment related views '''
from flask import make_response, jsonify, request, Blueprint
from flask.views import MethodView
from api.v2.comment.comment import Comment
from api.v2.common.validators import does_object_exist, content_quality, token_required



comment_blueprint = Blueprint('comment', __name__)


class MyComment(MethodView):
    ''' a class for  comment on an answer'''
    @classmethod
    @token_required
    def post(cls, questionId, answerId, user_id):
        ''' method for asking a question'''
        if not does_object_exist(column='title', table='questions', col_name='question_id', param=questionId):
            return make_response(jsonify({'message':'Question does not exist'})), 404
        if not does_object_exist(column='description', table='answers', col_name='answer_id', param=answerId):
            return make_response(jsonify({'message':'Answer does not exist'})), 404
        comment_body = request.json.get('comment')
        if not comment_body:
            return make_response(jsonify({'message': 'Provide comment description'})), 400
        if does_object_exist(column='comment', table='comments', col_name='comment', param=comment_body):
            return make_response(jsonify(
                {'message': 'You have already made this comment'})), 409
        if content_quality(comment_body, content='comment'):
            return make_response(jsonify({'message': quality_check})), 409
        comment = Comment(comment_body, answerId, user_id)
        comment.save_comment()
        return make_response(jsonify({'message': 'Succesfully added a comment'})), 201


comment_blueprint.add_url_rule(
    '/questions/<questionId>/answers/<answerId>/comments', view_func=MyComment.as_view('comments'), methods=['POST'])
