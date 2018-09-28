[![Build Status](https://travis-ci.org/TheSteelGuy/StackOverFlowLiteApi.svg?branch=develop)](https://travis-ci.org/TheSteelGuy/StackOverFlowLiteApi)
[![Coverage Status](https://coveralls.io/repos/github/TheSteelGuy/StackOverFlowLiteApi/badge.svg?branch=159922255-ch3-delete-functionality-persist)](https://coveralls.io/github/TheSteelGuy/StackOverFlowLiteApi?branch=159922255-ch3-delete-functionality-persist)
[![Maintainability](https://api.codeclimate.com/v1/badges/c9337d2239165a70a7db/maintainability)](https://codeclimate.com/github/TheSteelGuy/StackOverFlowLiteApi/maintainability)
# StackOverFlowLiteApi

## Introduction
* An API for the StackOverFLow hosted  **[```here```](https://thesteelguy.github.io/StackOverFowLite/)**). front end app.
* StackOverFLowLite a platform where people can ask questions and provide answers. .

## Technologies used & needed.
* **[Python](https://www.python.org/downloads/)**).
* **[Flask](flask.pocoo.org/)**  
*  Postgress
* Json web Tokens for authentication

## Setting up database
### Install Postgres:
```
$ sudo apt-get update
$ sudo apt-get install postgresql postgresql-contrib
$ psql -c "CREATE DATABASE sol;" -U postgres
```
## Link to heroku:
* https://stackoverflowlitev2.herokuapp.com/

## Current endpoints(More to follow)

* #### SIgnup.
    `POST /api/v2/auth/signup`:
    ```
    headers = {content_type:application/json}

    {
        "username":"username",
        "email":"someemail@.gmail.com",
        "password":"collo0",
        "confirm_pwd":"collo0"
    }

* #### Login.
    `POST /api/v2/auth/login`:
    ```
    headers = {content_type:application/json}

    {
        "email":"someemail@gmail.com",
        "password":"collo0"

    }

* #### Login.
    `POST /api/v2/auth/logout`:
    ```
    headers = {content_type:application/json}
    ```
  #### NB all DELETE,POST, PUT apart from signup and login endpoints require tokens

* #### Ask a question.
    `POST /api/v2/questions`:
    ```
    headers = {content_type:application/json}

    {
        "title": "title description",
        "body": "question body description"

    }
    ```
* #### Fetch all questions.
    `GET /api/v2/questions`
    ```
    headers = {content_type:application/json}
    ```


* #### Fetch a specific question.   
    `GET /api/2/questions/<questionId>`
    ```
    headers = {content_type:application/json}
    ```


* #### Provide an answer to a question.
    `POST /api/v2/questions/questionId/answers`:
    ```
    headers = {content_type:application/json}

    {
        "answer": "answer description"
    }
    ```

* #### Delete a question.
    `DELETE /api/v2/questions/questionId`:
    ```
    headers = {content_type:application/json}

    ```
* #### Accept answer as preffered.   
    `PUT /api/v2/questions/<questionId>/answers/<answerId>`
    ```
    headers = {content_type:application/json}
    ```
* #### Upvote/Downvote an answer.   
    `GET /api/v2/questions/<questionId>/answers/<answerId>/<vote>`
    ```
    headers = {content_type:application/json}

    to downvote replace vote with downvote and upvote to upvote an answer
    for example to upvote answer send: `GET /api/v1/questions/<questionId>/answers/<answerId>/upvote
    ```


* #### Comment on an answer.   
    `POST /api/v2/questions/<questionId>/answers/<answerId>/comments`
    ```
    headers = {content_type:application/json}

    {
        "comment": "comment description here"
    }
    ```


## Installation guide and usage

 #### **Clone the repo.**
    ```
    $ git clone https://github.com/TheSteelGuy/StackOverFlowLiteApi.git
    ```
 #### **Create virtual environment & Activate.**
    ```
    $ virtualenv -p python3 myenv
    $ source myenv/bin/activate
    ```
 #### **Install Dependancies.**
    ```
    (myenv)$ pip install -r requirements.txt
    ```
 #### **Enviroment variables.**
    ```
    by default if you dont pass any this the sever runs as development
    ```
### if you want to test other enviroments type:
    ```
    (myenv)$ export CONFIG_ENVIRONMENT=production **to run *under produnction environment**
    ```

#### **Run the app**
   ```
    (myenv)$ python runv2.py
   ```
#### **Run Tests**
  ```
  (myenv)$ pytest --cov=api
  ```
