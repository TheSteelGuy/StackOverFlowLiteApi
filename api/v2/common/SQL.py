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
    query1 = 'SELECT accepted from answers WHERE answer_id=%s'
    cursor.execute(query1, answerId)
    bool_ = cursor.fetchone()
    if bool_['accepted']:
        return 'You have already accepted this answer before'
    query = 'UPDATE answers SET accepted=true WHERE answer_id=%s'
    cursor.execute(query, answerId)
    CONN.commit()
    return 'Succefully, accepted, this answer as preffered to your question'


def update_answer(answerId, description):
    query = "UPDATE answers SET description='{}' WHERE answer_id=%s;".format(description)
    cursor.execute(query, answerId)
    CONN.commit()
    return True

def upvote_answer(answerId, count):
    query = "UPDATE answers SET votes=(SELECT votes+{} FROM answers WHERE answer_id=%s) RETURNING votes".format(count)
    cursor.execute(query, answerId)
    CONN.commit()
    votes = cursor.fetchone()
    return votes

def delete_(questionId):
    '''remove item from db'''
    query = "DELETE FROM questions WHERE question_id ='{}'".format(questionId)
    cursor.execute(query)
    CONN.commit()

def fetch_question_answer():
    '''inner joining users and question tables'''
    query = "SELECT u.user_id,u.username AS posted_by, q.question_id, q.title AS question_title, SUBSTRING(q.body,1,20) AS question_body,\
    q.post_date, COALESCE(a.votes,'0') as votes FROM users u, questions q, answers a WHERE \
    u.user_id=q.author_id AND a.question_id=q.question_id;"
    cursor.execute(query)
    records = cursor.fetchall()
    if not records:
        return False
    return records

def fetch_question():
    '''fetch Questions'''
    query = "SELECT u.username, q.question_id, q.title AS question_title, SUBSTRING(q.body,1,50) AS question_body,\
    q.post_date, COALESCE(a.votes,'0') as votes FROM users u, questions q, answers a WHERE \
    u.user_id=q.author_id"
    cursor.execute(query)
    records = cursor.fetchchall()
    if records:
        return records
    return False



def prevent_unauthorized_deletes(questionId):
    query = "SELECT question_id, author_id FROM questions WHERE question_id='{}';".format(questionId)
    cursor.execute(query)
    record = cursor.fetchone()
    if record:
        return record['author_id']
    return False
