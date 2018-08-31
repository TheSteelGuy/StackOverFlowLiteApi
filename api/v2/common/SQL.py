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
    query = "UPDATE answers SET description='{}' WHERE answer_id=%s;".format(
        description)
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


def fetch_user_question(id):
    '''inner joining users and question tables'''
    query = "SELECT u.username AS asked_by, q.question_id, q.title AS question_title,\
        SUBSTRING(q.body,50) AS question_body,q.post_date FROM users u, questions q WHERE u.user_id=q.author_id\
        AND u.user_id=(SELECT user_id FROM users WHERE user_id={});".format(id)
    cursor.execute(query)
    records = cursor.fetchall()
    if not records:
        return False
    return records


def fetch_questions():
    '''fetch Questions'''
    query = "SELECT u.username AS asked_by,q.question_id, q.title AS question_title, SUBSTRING(q.body,1,50)\
        AS question_body,q.post_date, COALESCE(a.votes,'0') as votes FROM users u,\
        questions q, answers a WHERE u.user_id=q.author_id"
    cursor.execute(query)
    records = cursor.fetchall()
    if records:
        return records
    return False


def fetch_question():
    query = "SELECT questions.question_id, questions.title as question_title, questions.body AS question\
        ,questions.post_date AS asked_on, COALESCE(answers.description, 'No answer') AS answer,\
        COALESCE(answers.votes,'0') AS answer_votes,COALESCE(answers.answer_date,'No date') AS answered_on\
        from questions LEFT JOIN answers ON questions.question_id=answers.question_id;"
    cur = CONN.cursor()
    cur.execute(query)
    records = cur.fetchall()
    return records


def prevent_unauthorized_deletes(questionId):
    query = "SELECT question_id, author_id FROM questions WHERE question_id='{}';".format(
        questionId)
    cursor.execute(query)
    record = cursor.fetchone()
    if record:
        return record['author_id']
    return False
