'''comment.py'''
from datetime import datetime


class Comment():
    ''' comment related operations'''

    def __init__(self, comment):
        ''' constructor method to give a comment its attributes'''
        self.comment = comment
        self.comment_date = datetime.now()

    def serialize_comment(self, id_count):
        ''' takes a comment object and returns its __dict__ representation'''
        return dict(
            comment=self.comment,
            comment_date=self.comment_date,
            commentId=id_count
        )
