'''answer.py'''
from datetime import datetime
from api.v2 import CONN


class Answer():
    '''answer class conaining answer related operations'''

    def __init__(self, answer_body, questionid, authorid, questionauthorid):
        '''constructor method to initialize an object'''
        self.answer_body = answer_body
        self.answer_date = datetime.now()
        self.questionid = questionid
        self.authorid = authorid
        self.qestionauthorid = questionauthorid

    def save_answer(self):
        ''' saves answer in the answers table'''
        cursor = CONN.cursor()
        query = 'INSERT INTO answers (description, answer_date,questionauthor_id,question_id,answerauthor_id)\
         VALUES(%s,%s,%s,%s,%s)'
        cursor.execute(query,
                       (self.answer_body, self.answer_date, self.qestionauthorid, self.questionid, self.authorid))
        CONN.commit()
        return 'done'
