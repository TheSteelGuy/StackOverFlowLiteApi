'''manage.py'''
import psycopg2
from psycopg2.extras import RealDictCursor
from os import getenv
from api.v2.tables import create

class DBSetup():
    '''set up database actions'''
    def __init__(self):
        ''' db constructor method'''
        self.db_name = getenv('DB_NAME')
        self.db_user = getenv('DB_USER')
        self.db_password = getenv('DB_PASSWORD') 
        self.db_host = getenv('DB_HOST')
        self.connection = psycopg2.connect(database=self.db_name, user=self.db_user,host=self.db_host,password=self.db_password)



    def create_tables(self):
        '''create tables for the the application'''
        cur = self.connection.cursor()
        for create_table in create():
            try:
              cur.execute(create_table)
              print ('......creating.......')
              self.connection.commit()
              print ('table created in success')
            except Exception as e:
                string = 'An exception of type {0} occurred. Arguments:\n{1!r}'
                message = string.format(type(e).__name__, e.args)
                print(message)
        return 'tables created'
    
                
                
            

    def drop_tables(self):
        ''' removes all tables from the database'''
        drop_query = (
            'DROP TABLE IF EXISTS questions CASCADE;',
            'DROP TABLE IF EXISTS answers CASCADE;',
            'DROP TABLE IF EXISTS users CASCADE;',
            'DROP TABLE IF EXISTS comments CASCADE',
            'DROP TABLE IF EXISTS blacklist_tokens;'
        )
        try:
            cur = self.connection.cursor()
            for drop_table in drop_query:
                cur.execute(drop_table)
                print ('.....DROP.....')
            self.connection.commit()
        except Exception as e:
            string = 'An exception of type {0} occurred. Arguments:\n{1!r}'
            message = string.format(type(e).__name__, e.args)
            #rollback the ops
            print (message)
        return 'drop tables was a success'

    def cursor(self):
        '''method to allow objects execute SQL querries on the db instance'''
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        return cur
    
    def commit(self):
        '''commits changes to db'''
        self.connection.commit()

        


