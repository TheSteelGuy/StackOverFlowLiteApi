'''test question related user action'''
import unittest
import json
from flask_testing import TestCase
from flask import request
from api.v1 import create_app
from api.v1.answer.views import answers
from api.v1.question.views import questions
from .test_answer import Testbase


class TestAnswer2(Testbase):
    ''' test answer functionalities'''
    def ask_question(self):
        ''' help post a question for a testcase that needs it'''
        res = self.client.post(
            'api/v1/questions',
            data=json.dumps(self.question),
            content_type='application/json'
        )
        return res
    
    def test_downvote_question(self):
        '''test downvoting'''
        self.ask_question()
        answer = self.client.post(
            'api/v1/questions/1/answers',
            data=json.dumps(self.answer),
            content_type='application/json'
        )
        self.assertEqual(answer.status_code, 201)
        downvote = self.client.get('api/v1/questions/1/answers/1/downvote', content_type='application/json')
        self.assertIn('-1',str(downvote.data))

    def test_upvote_question(self):
        '''test downvoting'''
        self.ask_question()
        answer = self.client.post(
            'api/v1/questions/1/answers',
            data=json.dumps(self.answer),
            content_type='application/json'
        )
        self.assertEqual(answer.status_code, 201)
        downvote = self.client.get('api/v1/questions/1/answers/1/upvote', content_type='application/json')
        self.assertIn('1',str(downvote.data))

