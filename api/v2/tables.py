''' module  that contains table definitions for both test db and api db'''
def create():
    tables_queries = (
        'CREATE TABLE IF NOT EXISTS users (\
                user_id SERIAL PRIMARY KEY,\
                username VARCHAR(40),\
                email VARCHAR(64),\
                confirmed_user BOOLEAN DEFAULT false,\
                password VARCHAR(164)\
                )',
    
        'CREATE TABLE IF NOT EXISTS questions (\
                question_id SERIAL PRIMARY KEY,\
                title VARCHAR(255),\
                body TEXT,\
                post_date TIMESTAMP,\
                author_id INTEGER REFERENCES users (user_id) ON DELETE CASCADE\
                )',
        'CREATE TABLE IF NOT EXISTS answers (\
                answer_id SERIAL PRIMARY KEY,\
                description VARCHAR (250),\
                votes INTEGER DEFAULT 0,\
                accepted BOOLEAN DEFAULT false,\
                answer_date VARCHAR (100),\
                questionauthor_id INTEGER REFERENCES users (user_id) ON DELETE CASCADE,\
                question_id INTEGER REFERENCES questions (question_id) ON DELETE CASCADE,\
                answerauthor_id INTEGER REFERENCES users (user_id) ON DELETE CASCADE\
                )',
        'CREATE TABLE IF NOT EXISTS comments (\
                comment_id SERIAL PRIMARY KEY,\
                comment TEXT,\
                comment_date TIMESTAMP,\
                answer_id INTEGER REFERENCES answers (answer_id) ON DELETE CASCADE,\
                commentor_id INTEGER REFERENCES users (user_id) ON DELETE CASCADE\
                )',
      
        'CREATE TABLE IF NOT EXISTS tokens (\
                token_id SERIAL PRIMARY KEY,\
                token VARCHAR(155)\
                )'
    
    )
        
    return tables_queries
