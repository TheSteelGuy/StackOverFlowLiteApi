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
