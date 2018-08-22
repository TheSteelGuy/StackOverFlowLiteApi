'''test question related user action'''
import unittest
import json
from api.v2.common.base_tests import Testbase


"""class TestComment(Testbase):
    '''tests comment related actions'''

    def ask_question(self):
        ''' help post a question for a testcase that needs it'''
        res = self.client.post(
            'api/v2/questions',
            data=json.dumps(self.question),
            content_type='application/json'
        )
        return res



    def test_comment_possibility(self):
        '''tests commenting functionality'''
        self.ask_question()
        self.answer_question()
        assert 'Succesfully added a comment' in str(self.comment_().data)


if __name__ == '__main__':
    unittest.main()"""
