'''test question related user action'''
import unittest
import json
from api.v2.common.base_tests import Testbase


class TestQuestion(Testbase):
    '''tests question related actions'''

    def test_ask_question(self):
        '''test if question can be asked'''
        quiz = self.help_ask_question()
        self.assertEqual(quiz.status_code, 201)

    def test_fetch_questions(self):
        '''test if rides can be fetched'''
        self.help_ask_question()
        questions = self.client.get(
            'api/v2/questions',
            content_type='application/json'
        )
        res = json.loads(questions.data.decode())
        self.assertEqual(len(res), 1)

    def test_fetch_a_question(self):
        '''tests single question retrival'''
        self.help_ask_question()
        question = self.client.get(
            'api/v2/questions/1',
            content_type='application/json'
        )
        self.assertEqual(question.status_code, 200)
        res = json.loads(question.data.decode())
        self.assertEqual(len(res), 1)

    def test_ask_question_with_no_title(self):
        '''tests to see wether posting question with no title is possible'''
        r = self.client.post(self.SIGNUP_URL, data=json.dumps(
            self.signup_user), content_type='application/json')
        data_ = json.loads(r.data.decode())
        quiz = self.client.post(
            '/api/v2/questions',
            data=json.dumps({'title': '', 'body': 'is james alive?'}),
            headers={
                'Authorization': 'Bearer ' + json.loads(r.data.decode())['auth_token']
            },
            content_type='application/json'
        )
        res = json.loads(quiz.data.decode())
        self.assertEqual(
            res['message'], 'Provide question title')

    def test_ask_question_with_no_body(self):
        '''tests to see wether posting question with no body is possible'''
        r = self.client.post(self.SIGNUP_URL, data=json.dumps(
            self.signup_user), content_type='application/json')
        data_ = json.loads(r.data.decode())
        quiz = self.client.post(
            '/api/v2/questions',
            data=json.dumps({'title': 'is james alive?', 'body': ''}),
            headers={
                'Authorization': 'Bearer ' + json.loads(r.data.decode())['auth_token']
            },
            content_type='application/json'
        )
        res = json.loads(quiz.data.decode())
        self.assertTrue(res['message'] == 'Provide question description')

    def test_delete_question(self):
        '''tests to see if deleting post possible'''
        r = self.client.post(self.SIGNUP_URL, data=json.dumps(
            self.signup_user), content_type='application/json')
        self.client.post(
            '/api/v2/questions',
            data=json.dumps(self.question),
            headers={
                'Authorization': 'Bearer ' + json.loads(r.data.decode())['auth_token']
            },
            content_type='application/json'
        )
        remove = self.client.delete(
            '/api/v2/questions/1',
            headers={
                'Authorization': 'Bearer ' + json.loads(r.data.decode())['auth_token']
            },
            content_type='application/json'
        )
        res = json.loads(remove.data.decode())
        self.assertEqual(res['message'], 'Succefully deleted this question')


if __name__ == '__main__':
    unittest.main()
