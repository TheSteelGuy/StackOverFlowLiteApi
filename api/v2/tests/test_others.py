'''test answer related user action'''
import unittest
import json
from api.v2.common.base_tests import Testbase


class TestOtherTests(Testbase):
    '''tests api non direct endpoint related'''

    def test_404_not_found(self):
        '''tests 404 not found'''
        get = self.client.get(
            'api/v2/collo'
        )
        assert 'the requested resource could not be found on this server' in str(
            get.data)

    def test_400_bad_request(self):
        '''tests 404 not found'''
        r = self.client.post(self.SIGNUP_URL, data=json.dumps(
            self.signup_user), content_type='application/json')
        res = self.client.post(
            'api/v2/questions',
            headers={
                'Authorization': 'Bearer ' + json.loads(r.data.decode())['auth_token']
            },
            data='questions are for the strong',
            content_type='application/json')

        assert 'incorrect     data input format' in str(res.data)
