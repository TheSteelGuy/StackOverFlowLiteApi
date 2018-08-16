'''test comment related user action'''
import unittest
import json
from flask_testing import TestCase
from flask import request
from api.v1 import create_app
from api.v1.comment.views import comments
from api.v1.question.views import questions
from api.v1.answer.views import answers


class Testbase(TestCase):
    '''test super class'''

    def create_app(self):
        self.app = create_app('testing')
        return self.app

    def setUp(self):
        self.client = self.app.test_client()
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

    def tearDown(self):
        '''empty lists'''
        del comments[:]
        del questions[:]
        del answers[:]


class TestComment(Testbase):
    '''tests comment related actions'''

    def ask_question(self):
        ''' help post a question for a testcase that needs it'''
        res = self.client.post(
            'api/v1/questions',
            data=json.dumps(self.question),
            content_type='application/json'
        )
        return res

    def answer_question(self):
        '''help answer question'''
        answer = self.client.post(
            'api/v1/questions/1/answers',
            data=json.dumps(self.answer),
            content_type='application/json'
        )
        return answer

    def comment_(self):
        '''comment on an answer'''
        comment = self.client.post(
            'api/v1/questions/1/answers/1/comments',
            data=json.dumps(self.comment),
            content_type='application/json'
        )
        return comment

    def test_comment_possibility(self):
        '''tests commenting functionality'''
        self.ask_question()
        self.answer_question()
        assert 'Succesfully added a comment' in str(self.comment_().data)


if __name__ == '__main__':
    unittest.main()
