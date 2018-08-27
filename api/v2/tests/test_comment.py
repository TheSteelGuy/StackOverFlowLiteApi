'''test question related user action'''
import unittest
import json
from api.v2.common.base_tests import Testbase


class TestComment(Testbase):
    '''tests comment related actions'''
    def test_comment_possibility(self):
        '''tests commenting functionality'''
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
            'api/v2/questions/1/answers',
            data=json.dumps(self.answer),
            headers={
                'Authorization': 'Bearer ' + json.loads(r.data.decode())['auth_token']
            },
            content_type='application/json')
        comment = self.client.post(
            'api/v2/questions/1/answers/1/comments',
            data=json.dumps(self.comment),
            headers={
                'Authorization': 'Bearer ' + json.loads(r.data.decode())['auth_token']
            },
            content_type='application/json'  
        )
        assert 'Succesfully added a comment' in str(comment.data)


if __name__ == '__main__':
    unittest.main()
