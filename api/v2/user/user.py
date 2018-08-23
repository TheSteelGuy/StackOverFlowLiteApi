'''user class'''
import re
from werkzeug.security import generate_password_hash
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
            return 'You should not use numbers only as password'
        return True

