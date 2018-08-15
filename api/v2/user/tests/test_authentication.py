'''test auth views'''
from unittest import TestCase
import json
from api.v2 import create_app
#from api.v2.user import User


class Testbase(TestCase):
    '''test super class'''

    def setUp(self):
        '''prepare test environment'''
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.SIGNUP_URL = 'api/v2/auth/signup'
        self.signup_user = {
            'username': 'collo',
            'email': 'myemail@gmail.com',
            'password': '12345jamesQ@',
            'confirm_pwd': '12345jamesQ@'
        }
        self.login_user = {
            'username': 'collo',
            'password': '12345jamesQ@'
        }

    def tearDown(self):
        '''drop tables for atomicity of tests'''


class SignUpTests(Testbase):

    def test_signup(self):
        signup = self.client.post(
            self.SIGNUP_URL,
            data=json.dumps(self.signup_user),
            content_type='application/json'
        )

        self.assertIn('Registration successfull', str(signup.data))

    def test_signup_more_than_once_with_same_email(self):
        '''test if a user can signup twice with the same details'''
        self.client.post(
            self.SIGNUP_URL,
            data=json.dumps(self.signup_user),
            content_type='application/json'
        )
        response = self.client.post(
            self.SIGNUP_URL,
            data=json.dumps(self.signup_user),
            content_type='application/json'
        )
        self.assertIn(
            'A user with that email address already exist', str(response.data))

    def test_logout(self):
        ''''tests_user logout'''
        r = self.client.post(self.SIGNUP_URL, data=json.dumps(
            self.signup_user), content_type='application/json')
        data_ = json.loads(r.data.decode())
        self.assertEqual(data_['message'], 'registration successfull')

        logout = self.client.post(
            'api/v2/auth/logout',
            headers={
                'Authorization': 'Bearer ' + json.loads(r.data.decode())['auth_token']
            },
            content_type='application/json'
        )
        self.assertIn('You have successfuly logged out', str(logout.data))

    def test_if_user_can_signin(self):
        '''tests if a user can log in with correct credentials'''
        self.client.post(self.SIGNUP_URL, data=json.dumps(self.signup_user), content_type='application/json'
                         )
        login = self.client.post(
            'api/v2/auth/login', data=json.dumps(self.login_user), content_type='application/json')
        self.assertIn('You have succefully logged in', str(login.data))

    def test_signup_with_unmatching_credentials(self):
        '''tests if a user can signup with wrong credentials'''
        signup_user = {
            'username': 'collo',
            'email': 'myemail@gmail.com',
            'password': '12345Ii^5',
            'confirm_pwd': '123'
        }
        r = self.client.post(self.SIGNUP_URL, data=json.dumps(
            signup_user), content_type='application/json')
        self.assertIn(
            'Ensure password and confirm password matches', str(r.data))

    def test_if_user_can_signup_with_incorrect_data_format(self):
        '''test if signup possible with some missing required details'''
        signup_user = {
            'username': 'collo',
            'password': '12345%4b',
            'confirm_pwd': '12345%4b'
        }
        r = self.client.post(self.SIGNUP_URL, data=json.dumps(
            signup_user), content_type='application/json')
        self.assertIn(
            'Ensure you have provide all required details', str(r.data))

    def test_if_user_can_confirm_email(self):
        '''tests if a user can confirm email through links sent to there accounts'''
        signup = self.client.post(self.SIGNUP_URL, data=json.dumps(
            self.signup_user), content_type='application/json')
        token = json.loads(signup.data.decode())['confirm_token']
        auth_token = json.loads(signup.data.decode())['auth_token']
        res = self.client.get('api/v1/auth/confirm/{}'.format(token),
                              headers={'Authorization': 'Bearer '+auth_token})
        self.assertIn('Your email was verified succefully', str(res.data))

    def test_if_user_can_confirm_email_with_invalid_confirmation_token(self):
        '''tests if a user can confirm email through invalid links'''
        signup = self.client.post(self.SIGNUP_URL, data=json.dumps(
            self.signup_user), content_type='application/json')
        token = json.loads(signup.data.decode())['confirm_token']
        auth_token = json.loads(signup.data.decode())['auth_token']
        res = self.client.get('api/v1/auth/confirm/ioghohiuwie.uawouhe.iuah',
                              headers={'Authorization': 'Bearer '+auth_token})
        self.assertFalse('Your email was verified succefully' in str(res.data))


if __name__ == '__main__':
    unittest.main()
