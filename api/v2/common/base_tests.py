'''base tests '''
import json
from flask_testing import TestCase
from api.v2 import create_app, CONN
from api.v2.answer.answer import Answer
#from api.v2.comment.comment import Comment
from api.v2.question.question import Question
from api.v2.user.user import User


class Testbase(TestCase):
    '''base test setup class'''

    def create_app(self):
        self.app = create_app('testing')
        return self.app

    def setUp(self):
        self.client = self.app.test_client()
        CONN.drop_tables()
        CONN.create_tables()
        self.SIGNUP_URL = 'api/v2/auth/signup'
        self.signup_user = {
            'username': 'collo',
            'email': 'myemail@gmail.com',
            'password': '12345@',
            'confirm_pwd': '12345@'
        }
        self.login_user = {
            'email': 'myemail@gmail.com',
            'password': '12345@'
        }
        self.question = {
            'title': 'what is AJAX',
            'body': 'i am a newbie in js in this'

        }
        self.answer = {
            'answer': 'ajax is an old tech which...'
        }
        self.comment = {
            'comment': "i hear there is fetch api to replace AJAX's xmlhttprequest.."

        }

    def generate_token(self):
        '''generate tokens for the protected endpoints'''
        signup = self.client.post(
            self.SIGNUP_URL,
            data=json.dumps(self.signup_user),
            content_type='application/json')
        token = json.loads(signup.data.decode())['auth_token']
        return token

    def help_ask_question(self):
        ''' help post a question for a testcase that needs it'''
        r = self.client.post(self.SIGNUP_URL, data=json.dumps(
            self.signup_user), content_type='application/json')
        data_ = json.loads(r.data.decode())
        res = self.client.post(
            'api/v2/questions',
            headers={
                'Authorization': 'Bearer ' + json.loads(r.data.decode())['auth_token']
            },
            data=json.dumps(self.question),
            content_type='application/json')
        return res

    def comment_(self):
        '''comment on an answer'''
        comment = self.client.post(
            'api/v2/questions/1/answers/1/comments',
            data=json.dumps(self.comment),
            content_type='application/json'
        )
        return comment

    def tearDown(self):
        '''clear tables for every test'''
        CONN.drop_tables()
