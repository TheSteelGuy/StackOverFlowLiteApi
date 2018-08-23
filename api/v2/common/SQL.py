'''SQL.py contains querries'''
from api.v2 import CONN

cursor = CONN.cursor()


def select_all(table, column, param):
    '''select based on a condition'''
    query = 'SELECT * FROM {} WHERE {} =%s'.format(table, column)
    cursor.execute(query, param)
    list_ = cursor.fetchall()
    if list_:
        return list_
    return False


def select_no_condition(table):
    '''select based on no condition'''
    query = 'SELECT * FROM {}'.format(table)
    cursor.execute(query)
    list_ = cursor.fetchall()
    if list_:
        return list_
    return False


def accept_answer(answerId):
    query1 = 'SELECT accepted from answers WHERE aid=%s'
    cursor.execute(query1, answerId)
    bool_ = cursor.fetchone()
    if bool_['accepted']:
        return 'You have already accepted this answer before'
    query = 'UPDATE answers SET accepted=true WHERE aid=%s'
    cursor.execute(query, answerId)
    CONN.commit()
    return 'Succefully, accepted, this answer as preffered to your question'


def update_answer(answerId, description):
    query = "UPDATE answers SET description='{}' WHERE aid=%s;".format(description)
    cursor.execute(query, answerId)
    CONN.commit()
    return True

def delete_(questionId):
    '''remove item from db'''
    query = "DELETE FROM questions WHERE qid ='{}'".format(questionId)
    cursor.execute(query)
    CONN.commit()
