'''SQL.py contains querries'''
from api.v2 import CONN
from api.v2.common.validators import does_list_exist
cursor = CONN.cursor()


def select_all(table, column, param):
    '''select based on a condition'''
    query = "SELECT * FROM {} WHERE {}={}".format(table, column, param)
    cursor.execute(query)
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
    query1 = "SELECT accepted from answers WHERE answer_id=%s"
    cursor.execute(query1,(answerId,))
    bool_ = cursor.fetchone()
    if bool_['accepted']:
        return 'You have already accepted this answer before'
    query = 'UPDATE answers SET accepted=true WHERE answer_id=%s'
    cursor.execute(query, (answerId,))
    CONN.commit()
    return 'Succefully, accepted, this answer as preffered to your question'


def update_answer(answerId, description):
    query = "UPDATE answers SET description='{}' WHERE answer_id={} RETURNING description".format(
        description, answerId)
    cursor.execute(query)
    new_description = cursor.fetchone()
    CONN.commit()
    return new_description


def upvote_answer(answerId, count):
    query = "UPDATE answers SET votes=(SELECT votes+{} FROM answers WHERE answer_id=%s)\
     WHERE answer_id=%s RETURNING votes".format(count)
    cursor.execute(query, (answerId, answerId))
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
        AND u.user_id=(SELECT user_id FROM users WHERE user_id='{}');".format(id)
    cursor.execute(query)
    records = cursor.fetchall()
    return records

def questions_with_most_answer(id):
    '''inner joining users and question tables'''
    query = "q.question_id, q.title AS question_title,\
        SUBSTRING(q.body,50) AS question_body FROM users u, questions q WHERE u.user_id=q.author_id\
        AND u.user_id=(SELECT user_id FROM users WHERE user_id='{}');".format(id)
    cursor.execute(query)
    records = cursor.fetchall()
    return records

def fetch_user_answer(id):
    'fetch user answers'
    query1 = "SELECT question_id, answer_id,description AS myanswer FROM answers WHERE\
        answerauthor_id='{}';".format(id)
    cursor.execute(query1)
    user_answers = cursor.fetchall()
    return user_answers

def check_answer_belongs_to_question(question_id, answer_id):
    '''checks if answer is tied to question before commenting'''
    query = "SELECT q.question_id, a.answer_id FROM questions q \
            LEFT JOIN answers a on a.question_id=q.question_id WHERE q.question_id='{}'".format(question_id)
    cursor.execute(query)
    records = cursor.fetchall()
    answer_list = does_list_exist(records, 'answer_id', answer_id)
    if answer_list:
        return True
    return False

def prevent_own_answer_accept_vote(answer_id, user_id):
    '''prevents user from accepting own answer'''
    query = "SELECT a.answerauthor_id, a.answer_id FROM answers a WHERE answerauthor_id='{}';".format(user_id)
    cursor.execute(query)
    records = cursor.fetchall()
    answer_list = does_list_exist(records, 'answer_id', answer_id)
    if answer_list:
        return answer_list
    return False


def fetch_question(question_id):
    '''fetch Question'''
    query = "SELECT u.username AS asked_by,q.question_id, q.title AS question_title, q.body\
        AS question,q.post_date AS asked_on FROM questions q, users u WHERE q.author_id=u.user_id\
        AND question_id='{}';".format(question_id)
    cursor.execute(query)
    question = cursor.fetchall()
    if question:
        return question
    return False

def fetch_answers(question_id):
    '''fetch answers'''
    query = "SELECT u.username AS answerd_by, a.answer_id,a.question_id, a.description,a.votes\
        FROM answers a, users u WHERE u.user_id=a.answerauthor_id AND question_id='{}';".format(question_id)
    cursor.execute(query)
    answers = cursor.fetchall()
    if answers:
        return answers
    return False


def fetch_comments(question_id):
    '''fetch comments'''
    query = "SELECT u.username AS commented_by, c.comment_id, c.comment, a.question_id, a.answer_id\
    FROM comments c, answers a, users u WHERE u.user_id=c.commentor_id\
    AND a.answer_id=c.answer_id AND a.question_id='{}';".format(question_id)
    cursor.execute(query)
    comments = cursor.fetchall()
    return comments

def answer_comments(question_id):
    '''ensures each answer is tied to its comments'''
    answers_list = fetch_answers(question_id)
    answers = answers_list if answers_list else []
    comments = fetch_comments(question_id)
    final_list = []
    for answer in answers:
        answer_ = does_list_exist(answers, 'answer_id', answer['answer_id'])
        comments_ = does_list_exist(comments, 'answer_id', answer['answer_id'])
        answer_.append({'comments' : comments_ if comments_ else []})
        final_list.append(answer_)
    return final_list


def fetch_questions():
    query = "SELECT users.username AS asked_by,questions.question_id, questions.title AS question_title,\
        SUBSTRING(questions.body, 1,150) AS question, questions.post_date AS asked_on FROM questions\
        LEFT JOIN users ON questions.author_id=users.user_id ORDER BY questions.post_date DESC;"
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

