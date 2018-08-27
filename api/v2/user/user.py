'''user class'''
import re
from datetime import datetime, timedelta
import jwt
from werkzeug.security import generate_password_hash
from flask import current_app
from api.v2 import CONN


class User():
    ''' class user'''

    def __init__(self, username, email, password, confirm_pwd):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.confirm_pwd = confirm_pwd

    def save_user(self):
        ''' saves user in the table'''
        cursor = CONN.cursor()
        query = 'INSERT INTO users (username, email, password) VALUES(%s,%s,%s)'
        cursor.execute(query, (self.username, self.email, self.password_hash))
        CONN.commit()
        return 'done'

    @classmethod
    def validate_email(cls, email):
        ''' check email pattern'''
        return bool(re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email))

    @classmethod
    def pass_strength(cls, password):
        '''check passphrase strength'''
        if len(password.strip()) < 1:
            return 'Password cannot be empty, please provide a password'
        if len(password) < 4:
            return 'Password should be more than 5 characters long'
        if password.isdigit():
            return 'You should not use numbers only as password'
        if password.isalpha():
            return 'You should not use letters only as password, or easy to guess password such as your name'
        

    @staticmethod
    def generate_token(user_id):
        '''method which generates token for users'''
        try:
            paylod = {
                'exp': datetime.utcnow() + timedelta(minutes=1200),
                'iat': datetime.utcnow(),
                'sub': user_id

            }
            encoded_token = jwt.encode(
                paylod, current_app.config['SECRET_KEY']
            )
            return encoded_token

        except Exception as e:
            string = 'An exception of type {0} occurred. Arguments:\n{1!r}'
            message = string.format(type(e).__name__, e.args)
            return message

    @staticmethod
    def decode_token(token_auth):
        '''decodes the token'''
        try:
            paylod = jwt.decode(
                token_auth, current_app.config['SECRET_KEY'])
            token_blacklisted = BlacklistToken.verify_token(token_auth)
            if token_blacklisted:
                return 'You have already logged out'
            return paylod['sub']
        except jwt.ExpiredSignatureError:
            return 'Token expired, you need to login'
        except jwt.InvalidTokenError:
            return 'The token is invslid'


class BlacklistToken():
    '''blacklist token'''

    def __init__(self, token):
        '''contructor for token'''
        self.token = token

    @staticmethod
    def verify_token(auth_token):
        '''
        Checks if the token exist in the database,
        that is wether it is blacklisted or not.
        '''
        query = 'SELECT token FROM tokens WHERE token =%s'
        cursor = CONN.cursor()
        cursor.execute(query, (str(auth_token),))
        blacklisted_token = cursor.fetchone()
        if blacklisted_token:
            return True
        return False

    def save_token(self, token):
        ''' saves user in the table'''
        cursor = CONN.cursor()
        query = 'INSERT INTO tokens (token) VALUES (%s)'
        cursor.execute(query, (token,))
        CONN.commit()
