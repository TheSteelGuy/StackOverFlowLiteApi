'''test question related user action'''
import unittest
import json
from api.v2.common.base_tests import Testbase

class TestAnswer2(Testbase):
    ''' test answer functionalities'''


    def test_downvote_question(self):
        '''test downvoting'''
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
            content_type='application/json'
        )
        self.assertEqual(answer.status_code, 201)
        downvote = self.client.get(
            'api/v2/questions/1/answers/1/downvote', 
            headers={
                'Authorization': 'Bearer ' + json.loads(r.data.decode())['auth_token']
            },
             content_type='application/json')
        self.assertIn('-1', str(downvote.data))

    def test_upvote_question(self):
        '''test downvoting'''
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
            headers={
                'Authorization': 'Bearer ' + json.loads(r.data.decode())['auth_token']
            },
            data=json.dumps(self.answer),
            content_type='application/json'
        )
        self.assertEqual(answer.status_code, 201)
        downvote = self.client.get(
            'api/v2/questions/1/answers/1/upvote',
            headers={
                'Authorization': 'Bearer ' + json.loads(r.data.decode())['auth_token']
            },
             content_type='application/json')
        self.assertIn('1', str(downvote.data))

if __name__ == '__main__':
    unittest.main()
