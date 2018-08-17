'''answer.py'''
from datetime import datetime
from api.v2 import CONN


class Answer():
    '''answer class conaining answer related operations'''

    def __init__(self, answer_body, questionId):
        '''constructor method to initialize an object'''
        self.answer_body = answer_body
        self.answer_date = datetime.now()
        self.questionId = questionId
        

    def save_answer(self):
        ''' saves answer in the answers table'''
        cursor = CONN.cursor()
        query = 'INSERT INTO answers (description, answer_date, questionId) VALUES(%s,%s,%s)'
        cursor.execute(query, (self.answer_body, self.answer_date, self.questionId))
        CONN.commit()
        return 'done'
