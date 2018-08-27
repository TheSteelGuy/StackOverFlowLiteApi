'''test answer related user action'''
import unittest
import json
from api.v2.common.base_tests import Testbase

class TestAnswer(Testbase):
    '''tests question related actions'''
    
    def test_answer_question(self):
        '''help answer question'''
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
            
        answer = self.client.post(
            'api/v2/questions/1/answers',
            data=json.dumps(self.answer),
            headers={
                'Authorization': 'Bearer ' + json.loads(r.data.decode())['auth_token']
            },
            content_type='application/json')
        assert 'Succesfully answerd the question' in str(answer.data)
  

    def test_answer_question_with_empty_body(self):
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
        answer = self.client.post(
            'api/v2/questions/1/answers',
            data=json.dumps({'body': ''}),
            headers={
                'Authorization': 'Bearer ' + json.loads(r.data.decode())['auth_token']
            },
            content_type='application/json'
        )
        assert 'Provide an answer' in str(answer.data)



    """def test_fetch_answers_for_a_question(self):
        '''check if answers for a question can be retrieved'''
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
        self.client.post(
            '/api/v2/questions/1/answers',
            data=json.dumps(self.answer),
            headers={
                'Authorization': 'Bearer ' + json.loads(r.data.decode())['auth_token']
            },
            content_type='application/json'
        )
        res = self.client.get('api/v2/questions/1/answers',
                              content_type='application/json')
        answer = json.loads(res.data.decode())['answers'][0]['answer']
        self.assertEqual(answer, 'ajax is an old tech which...')

    def test_accept_answer_as_preffered(self):
        '''tests accept answer'''
        self.ask_question()
        self.client.post('/api/v2/questions/1/answers',
                         data=json.dumps(self.answer), content_type='application/json')
        accept = self.client.put(
            '/api/v2/questions/1/answers/1', content_type='application/json')
        self.assertIn('Succesfully accepted this answer', str(accept.data))


if __name__ == ('__maain__'):
    unittest.main()"""
