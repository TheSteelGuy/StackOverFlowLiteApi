'''answer.py'''
from datetime import datetime

class Answer():
    '''answer class conaining answer related operations'''

    def __init__(self, answer_body):
        '''constructor method to initialize an object'''
        self.answer_body = answer_body
        self.answer_date = datetime.now()

    def serialize_answer(self, id_count, questionId):
        '''take user object and return __dict__ representation'''
        return dict(
            answer=self.answer_body,
            answer_id=id_count,
            answer_date=self.answer_date,
            questionId=questionId
        )

