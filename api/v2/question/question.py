'''question.py'''
from datetime import datetime
from api.v2 import CONN

class Question():
    ''' question containing question related operations'''

    def __init__(self, title, body, authorId):
        ''' constructor method to give a question its attributes'''
        self.title = title
        self.body = body
        self.post_date = datetime.now()
        self.authorId = authorId

    def save_question(self):
        ''' saves a question in the questions table'''
        cursor = CONN.cursor()
        query = "INSERT INTO questions (title, body,post_date, author_id) VALUES(%s,%s,%s,%s)\
        RETURNING question_id, title, body, post_date,(SELECT username FROM users WHERE user_id='{}');".format(self.authorId)
        cursor.execute(query, (self.title, self.body, self.post_date, self.authorId))
        record = cursor.fetchall()
        CONN.commit()
        return record
