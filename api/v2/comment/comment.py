'''comment.py'''
from datetime import datetime
from api.v2 import CONN


class Comment():
    ''' comment related operations'''

    def __init__(self, comment, answer_id , commentor_id):
        ''' constructor method to give a comment its attributes'''
        self.comment = comment
        self.comment_date = datetime.now()
        self.answer_id = answer_id
        self .commentor_id = commentor_id



    def save_comment(self):
        ''' saves a comment in the comments  table'''
        cursor = CONN.cursor()
        query = 'INSERT INTO comments (comment, comment_date,answer_id, commentor_id) VALUES(%s,%s,%s,%s)'
        cursor.execute(query, (self.comment, self.comment_date, self.commentor_id, self.answer_id))
        CONN.commit()
        return 'done'
    
