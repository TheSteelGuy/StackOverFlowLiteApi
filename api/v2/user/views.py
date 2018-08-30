'''views.py'''
import psycopg2
# third party imports
from flask import make_response, jsonify, request, Blueprint
from flask.views import MethodView
from werkzeug.security import check_password_hash
# local imports
from api.v2.user.user import User, BlacklistToken
from api.v2.common.validators import does_object_exist, check_user_input
from api.v2.common.SQL import select_all
from api.v2 import CONN
from api.v2.common.validators import token_required


auth_blueprint = Blueprint('auth', __name__)


class SignUp(MethodView):
    ''' a view class for sign up'''
    @classmethod
    def post(cls):
        ''' class method which allows user to sign up'''
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')
        confirm_pwd = request.json.get('confirm_pwd')
        check_input = check_user_input(username=username,email=email, pwd=password, confirm_pwd=confirm_pwd)
        if check_input:
            return make_response(jsonify({'message': check_input})), 409
        if not User.validate_email(email):
            return make_response(jsonify(
                {'message': 'Enter a valid email address.'}
            )), 409
        if password != confirm_pwd:
            return make_response(jsonify(
                {'message': 'Ensure password and confirm password matches.'}
            )), 409
        if User.pass_strength(password):
            return make_response(jsonify({'message': User.pass_strength(password)})), 409
        if does_object_exist(column='email', table='users', col_name='email', param=email):
            return make_response(jsonify(
                {'message': 'A user with that email already exist'}
            )), 409
        user = User(username, email, password, confirm_pwd)
        user.save_user()
        row = does_object_exist(
            column='user_id', table='users', col_name='email', param=user.email)
        token = user.generate_token(row['user_id'])
        return make_response(jsonify(
            {
                'message': 'Registration successfull', 'auth_token': token
            }
        )), 201
        return make_response(jsonify({'message': check_input})), 400


class SignIn(MethodView):
    ''' a view class for signin'''
    @classmethod
    def post(cls):
        '''a post class method which allows user to sign in'''
        email = request.json.get('email')
        password = request.json.get('password')
        if email and password:
            try:
                row = does_object_exist(
                    column='password', table='users', col_name='email', param=email)
                if check_password_hash(row['password'], password):
                    row = does_object_exist(
                        column='user_id', table='users', col_name='email', param=email)
                    token = User.generate_token(row['user_id'])
                    return make_response(jsonify(
                        {'message': 'You have succesfully logged in', 'auth_token': token})), 200
                return make_response(jsonify({'message': 'Wrong email or password'})), 401
            except TypeError:
                return make_response(jsonify({'message': 'That email address does not exist in our records'})), 404
        return make_response(jsonify({'message': 'Ensure you have provide all required details'})), 400


class Logout(MethodView):
    ''' a view class for logout '''
    @classmethod
    @token_required
    def post(cls, user_id):
        '''method to logout users'''
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split("Bearer ")[1]
        if auth_token:
            user_id = User.decode_token(auth_token)
            if not isinstance(user_id, str):
                blacklist_token = BlacklistToken(auth_token)
                blacklist_token.save_token(auth_token)
                response = {
                    'message': 'You have successfuly logged out'
                }
                return make_response(jsonify(response)), 200


auth_blueprint.add_url_rule(
    '/signup', view_func=SignUp.as_view('signup'), methods=['POST'])

auth_blueprint.add_url_rule(
    '/login', view_func=SignIn.as_view('login'), methods=['POST'])

auth_blueprint.add_url_rule(
    '/logout', view_func=Logout.as_view('logout'), methods=['POST'])
