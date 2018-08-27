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
        query = 'INSERT INTO questions (title, body,post_date, author_id) VALUES(%s,%s,%s,%s)'
        cursor.execute(query, (self.title, self.body, self.post_date, self.authorId))
        CONN.commit()
        return 'done'
