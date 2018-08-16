'''test question related user action'''
import unittest
import json
from flask_testing import TestCase
from flask import request
from api import create_app
from api.answer.views import answers
from api.question.views import questions


class Testbase(TestCase):
    '''test answer super class'''

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

    def tearDown(self):
        '''clear list data for every test case to be atomic'''
        del answers[:]
        del questions[:]


class TestAnswer(Testbase):
    '''tests question related actions'''

    def ask_question(self):
        ''' help post a question for a testcase that needs it'''
        res = self.client.post(
            'api/v1/questions',
            data=json.dumps(self.question),
            content_type='application/json'
        )
        return res

    def test_answer_question(self):
        '''test if asking question is possible'''
        quiz = self.ask_question()
        answer = self.client.post(
            'api/v1/questions/1/answers',
            data=json.dumps(self.answer),
            content_type='application/json'
        )
        self.assertEqual(answer.status_code, 201)

    def test_answer_question_with_empty_body(self):
        quiz = self.ask_question()
        answer = self.client.post(
            'api/v1/questions/1/answers',
            data=json.dumps({'body': ''}),
            content_type='application/json'
        )

    def test_answer_question_with_empty_body(self):
        quiz = self.ask_question()
        answer = self.client.post(
            'api/v1/questions/1/answers',
            data=json.dumps({'body': ''}),
            content_type='application/json'
        )
        self.assertIn('Provide an answer', str(answer.data))

    def test_fetch_anaswers_for_a_question(self):
        '''check if answers for a question can be retrieved'''
        self.ask_question()
        self.client.post(
            '/api/v1/questions/1/answers',
            data=json.dumps(self.answer),
            content_type='application/json'
        )
        res = self.client.get('api/v1/questions/1/answers',
                              content_type='application/json')
        answer = json.loads(res.data.decode())['answers'][0]['answer']
        self.assertEqual(answer, 'ajax is an old tech which...')

    def test_accept_answer_as_preffered(self):
        '''tests accept answer'''
        self.ask_question()
        self.client.post('/api/v1/questions/1/answers',
                        data=json.dumps(self.answer), content_type='application/json')
        accept = self.client.put('/api/v1/questions/1/answers/1', content_type='application/json')
        self.assertIn('Succesfully accepted this answer', str(accept.data))


if __name__ == ('__maain__'):
    unittest.main()
