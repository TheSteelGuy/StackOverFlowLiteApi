'''test question related user action'''
import unittest
import json
from api.v2.common.base_tests import Testbase

"""
class TestAnswer2(Testbase):
    ''' test answer functionalities'''


    def test_downvote_question(self):
        '''test downvoting'''
        self.ask_question()
        answer = self.client.post(
            'api/v2/questions/1/answers',
            data=json.dumps(self.answer),
            content_type='application/json'
        )
        self.assertEqual(answer.status_code, 201)
        downvote = self.client.get(
            'api/v2/questions/1/answers/1/downvote', content_type='application/json')
        self.assertIn('-1', str(downvote.data))

    def test_upvote_question(self):
        '''test downvoting'''
        self.ask_question()
        answer = self.client.post(
            'api/v2/questions/1/answers',
            data=json.dumps(self.answer),
            content_type='application/json'
        )
        self.assertEqual(answer.status_code, 201)
        downvote = self.client.get(
            'api/v2/questions/1/answers/1/upvote', content_type='application/json')
        self.assertIn('1', str(downvote.data))"""
