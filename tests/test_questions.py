'''test question related user action'''
import unittest
import json
from flask_testing import TestCase
from flask import request
from api import create_app
from api.question.views import questions


class Testbase(TestCase):
    '''test super class'''

    def create_app(self):
        self.app = create_app('testing')
        return self.app

    def setUp(self):
        self.client = self.app.test_client()
        self.question = {
            'title': 'what is AJAX',
            'body':'i am a newbie in js...'

        }

    def tearDown(self):
        '''make the questions list empty after each test case'''
        del questions[:]

class TestQuestion(Testbase):
    '''tests question related actions'''
    def help_ask_question(self):
        ''' help post a question for a testcase that needs it'''
        res = self.client.post(
            'api/v1/questions',
            data=json.dumps(self.question),
            content_type='application/json')
        return res

    def test_ask_question(self):
        '''test if question can be asked'''
        quiz = self.help_ask_question()
        self.assertEqual(quiz.status_code,201)
    
    def test_fetch_questions(self):
        '''test if rides can be fetched'''
        self.client.post(
            '/api/v1/questions',
            data=json.dumps(self.question),
            content_type='application/json'
        )
        questions = self.client.get(
            'api/v1/questions',
            content_type='application/json'
        )
        res = json.loads(questions.data.decode())
        self.assertEqual(len(res),1)

    def test_fetch_a_question(self):
        '''tests single question retrival'''
        self.client.post(
            '/api/v1/questions',
            data=json.dumps(self.question),
            content_type='application/json'
        )
        question = self.client.get(
            'api/v1/questions/1',
            content_type='application/json'
        )
        self.assertEqual(question.status_code, 200)
        res = json.loads(question.data.decode())
        self.asserTrue(res['title']=='what is AJAX')

    def test_ask_question_with_no_title(self):
        '''tests to see wether posting question with no title is possible'''
        quiz=self.client.post(
            '/api/v1/questions',
            data=json.dumps({'title':'','body':'is james alive?'}),
            content_type='application/json'
        )
        res = json.loads(quiz.data.decode())
        self.assertEqual(res['message'],'Provide question title, or check for spelling errors')

    def test_ask_question_with_no_body(self):
        '''tests to see wether posting question with no body is possible'''
        quiz=self.client.post(
            '/api/v1/questions',
            data=json.dumps({'title':'is james alive?','body':''}),
            content_type='application/json'
        )
        res = json.loads(quiz.data.decode())
        self.assertTrue(res['message'] =='Provide question description')


if __name__ == '__main__':
    unittest.main()
