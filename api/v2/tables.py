''' module  that contains table definitions for both test db and api db'''
def create():
    tables_query = (
        'CREATE TABLE IF NOT EXISTS users (\
                userId SERIAL PRIMARY KEY,\
                username VARCHAR(40),\
                email VARCHAR(64),\
                confirmed_user BOOLEAN DEFAULT false,\
                password VARCHAR(164)\
                )',
    
        'CREATE TABLE IF NOT EXISTS questions (\
                qid SERIAL PRIMARY KEY,\
                title VARCHAR(255),\
                body VARCHAR(400),\
                authorId INTEGER REFERENCES users (userId) ON DELETE CASCADE\
                )',
    
        'CREATE TABLE IF NOT EXISTS answers (\
                aId SERIAL PRIMARY KEY,\
                desc VARCHAR(400),\
                answer_date TIMESTAMP,\
                votes INTEGER,\
                accepted BOOLEAN default false,\
                questionId INTEGER REFERENCES questions (qId) ON DELETE CASCADE\
                )',

        'CREATE TABLE IF NOT EXISTS comments (\
                cId SERIAL PRIMARY KEY,\
                desc VARCHAR(400),\
                comment_date TIMESTAMP,\
                answerId INTEGER REFERENCES questions (aId) ON DELETE CASCADE\
                )',
      
        'CREATE TABLE IF NOT EXISTS tokens (\
                tId SERIAL PRIMARY KEY,\
                token VARCHAR(400)\
                )'
    )
        
    return tables_query

