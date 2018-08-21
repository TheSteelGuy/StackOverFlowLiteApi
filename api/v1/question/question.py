'''question.py'''
from datetime import datetime

class Question():
    ''' question containing question related operations'''

    def __init__(self, title, body):
        ''' constructor method to give a question its attributes'''
        self.title = title
        self.body = body
        self.post_date = datetime.now()

    def serialize_question(self, id_count):
        ''' takes a question object returns its dict representation'''
        return dict(
            title=self.title,
            body=self.body,
            post_date=self.post_date,
            questionId=id_count
        )
