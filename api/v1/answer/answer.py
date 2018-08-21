'''answer.py'''
from datetime import datetime


class Answer():
    '''answer class conaining answer related operations'''

    def __init__(self, answer_body):
        '''constructor method to initialize an object'''
        self.answer_body = answer_body
        self.answer_date = datetime.now()

    def serialize_answer(self, id_count, questionId, accpet_date):
        '''take user object and return __dict__ representation'''
        return dict(
            answer=self.answer_body,
            answerId=id_count,
            answer_date=self.answer_date,
            votes=0,
            accepted=False,
            date_accepted=accpet_date,
            questionId=questionId
        )
