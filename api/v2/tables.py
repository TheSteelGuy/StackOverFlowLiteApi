''' module  that contains table definitions for both test db and api db'''
def create():
    tables_queries = (
        'CREATE TABLE IF NOT EXISTS users (\
                userId SERIAL PRIMARY KEY,\
                username VARCHAR(40),\
                email VARCHAR(64),\
                confirmed_user BOOLEAN DEFAULT false,\
                password VARCHAR(164)\
                )',
    
        'CREATE TABLE IF NOT EXISTS questions (\
                qid SERIAL PRIMARY KEY,\
                title VARCHAR(55),\
                body VARCHAR(255),\
                post_date TIMESTAMP,\
                authorId INTEGER REFERENCES users (userId) ON DELETE CASCADE\
                )',
        'CREATE TABLE IF NOT EXISTS answers (\
                aId SERIAL PRIMARY KEY,\
                description VARCHAR(250),\
                votes INT DEFAULT 0,\
                accepted BOOLEAN DEFAULT false,\
                answer_date TIMESTAMP,\
                questionId INTEGER REFERENCES questions (qId) ON DELETE CASCADE\
                )',
        'CREATE TABLE IF NOT EXISTS comments (\
                cId SERIAL PRIMARY KEY,\
                description VARCHAR(100),\
                comment_date TIMESTAMP,\
                answerId INTEGER REFERENCES answers (aId) ON DELETE CASCADE\
                )',
      
        'CREATE TABLE IF NOT EXISTS tokens (\
                tId SERIAL PRIMARY KEY,\
                token VARCHAR(155)\
                )'
    
    )
        
    return tables_queries

   