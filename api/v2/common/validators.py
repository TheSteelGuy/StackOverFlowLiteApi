''' file contains common functions'''
from api.v2 import CONN

cursor = CONN.cursor()


def does_object_exist(column=None, table=None, col_name=None, param=None):
    ''' find out if a user exist before adding to db'''
    query = 'SELECT {} FROM {} WHERE {} =%s'.format(column, table, col_name)
    cursor.execute(query, (param,))
    list_ = cursor.fetchone()
    if list_:
        return list_
    return False


def question_quality(string1="", string2=""):
    '''check the quality of questions sent to the platform'''
    if len(string1.strip()) < 10:
        return 'Your question seems to be of low quality, ensure your title makes sense'
    if len(string1) > len(string2):
        return 'Ensure your description provides detail,it should not be shorter than title'
    if string1.isdigit() or string2.isdigit():
        return 'Your question cannot have a title with numbers only'
    if len(string2.split()) < 3:
        return 'Please space question body properly readership'
    if len(string1.split()) < 2:
        return 'Please space question title properly readership'


def content_quality(string_, content=None):
    if len(string_.strip()) < 10:
        return 'Your {} seems to be of low quality, ensure your it makes sense'.format(content)
    if string_.isdigit():
        return 'Your {} cannot be numbers only'.format(content)
    if len(string_.split()) < 2:
        return 'Please space your {} properly for readership'.format(content)
