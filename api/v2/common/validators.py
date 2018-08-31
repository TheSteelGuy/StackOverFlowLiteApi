''' file contains common functions'''
# third party imports
import re
from functools import wraps
from flask import request, jsonify, make_response
from api.v2 import CONN
# local imports
from api.v2.user.user import User
cursor = CONN.cursor()


def token_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        '''function that fetches token from header and decodes it'''
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return make_response(jsonify(
                {'message': 'provide a token in the authorization header, please'}
            )), 403
        auth_token = auth_header.split("Bearer ")[1]
        if auth_token:
            user_id = User.decode_token(auth_token)
            if not isinstance(user_id, str):
                user_id = user_id
            else:
                response = {
                    'message': user_id
                }
                return make_response(jsonify(response)), 401
        else:
            return False
        return func(user_id=user_id, *args, **kwargs)
    return wrapper


def does_object_exist(column=None, table=None, col_name=None, param=None):
    ''' find out if a user exist before adding to db'''
    query = 'SELECT {} FROM {} WHERE {} =%s'.format(column, table, col_name)
    cursor.execute(query, (param,))
    list_ = cursor.fetchone()
    if list_:
        return list_
    return False


def does_list_exist(list_, object_key, object_attr):
    ''' find out if an object exist'''
    object_list = list(
        filter(
            lambda object_dict: object_dict[object_key] == object_attr,
            list_))
    if object_list:
        return object_list
    return False


def question_quality(string1="", string2=""):
    '''check the quality of questions sent to the platform'''
    if len(string1.strip()) < 1:
        return 'Provide Question title'
    if string1.isdigit() or string2.isdigit():
        return 'Your question cannot have a title with numbers only'


def content_quality(string_, content=None):
    if len(string_.strip()) < 1:
        return 'Provide {} body'.format(content)
    if string_.isdigit():
        return 'Your {} cannot be numbers only'.format(content)


def check_user_input(username=None, email=None, pwd=None, confirm_pwd=None):
    ''' check user details'''
    if username is None:
        return 'Provide  username'
    if len(username.strip())<1:
        return 'Provide username'
    if len(username.strip())<4:
        return 'Username should be more than 4 characters long'
    if email is None:
        return 'Provide email'
    if pwd is None:
        return 'Provide password'
    if confirm_pwd is None:
        return 'Provide password confirmation'
