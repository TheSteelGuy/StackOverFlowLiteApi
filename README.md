[![Build Status](https://travis-ci.org/TheSteelGuy/StackOverFlowLiteApi.svg?branch=159788421-ch3-minimum-tests)](https://travis-ci.org/TheSteelGuy/StackOverFlowLiteApi)
[![Coverage Status](https://coveralls.io/repos/github/TheSteelGuy/StackOverFlowLiteApi/badge.svg?branch=159726336-ch2-create-accept-answer-functionality)](https://coveralls.io/github/TheSteelGuy/StackOverFlowLiteApi?branch=159726336-ch2-create-accept-answer-functionality)
[![Maintainability](https://api.codeclimate.com/v1/badges/c9337d2239165a70a7db/maintainability)](https://codeclimate.com/github/TheSteelGuy/StackOverFlowLiteApi/maintainability)
# StackOverFlowLiteApi

## Introduction
* An API for the StackOverFLow hosted  **[```here:```](https://thesteelguy.github.io/StackOverFowLite/)**). front end app.
* StackOverFLowLite a platform where people can ask questions and provide answers. .
## NB
The app purely uses python data structures hence no persistance, however another version will be available fro data persistance

## Technologies used & needed.
* **[Python3](https://www.python.org/downloads/)**).
* **[Flask](flask.pocoo.org/)**  

## Link to heroku:


## Current endpoints(More to follow)

* #### Ask a question.
    `POST /api/v1/questions`: 
    ```
    headers = {content_type:application/json}

    {
        "title": "title description",
        "body": "question body description"

    }
    ```
* #### Fetch all questions.
    `GET /api/v1/questions`
    ```
    headers = {content_type:application/json}
    ```


* #### Fetch a specific question.   
    `GET /api/v1/questions/<questionId>` 
    ```
    headers = {content_type:application/json} 
    ```
    

* #### Provide an answer to a question.
    `POST /api/v1/questions/questionId/answers`:
    ```
    headers = {content_type:application/json}

    {
        "answer": "answer description"
    }
    ```

* #### Delete a question.
    `DELETE /api/v1/questions/questionId/delete`:
    ```
    headers = {content_type:application/json}

    ```
* #### Accept answer as preffered.   
    `PUT /api/v1/questions/<questionId>/answers/<answerId>` 
    ```
    headers = {content_type:application/json} 
    ```
* #### Upvote/Downvote an answer.   
    `GET /api/v1/questions/<questionId>/answers/<answerId>/<vote>` 
    ```
    headers = {content_type:application/json} 

    to downvote replace vote with downvote and upvote to upvote an answer
    for example to upvote answer send: `GET /api/v1/questions/<questionId>/answers/<answerId>/upvote
    ```


* #### Comment on an answer.   
    `POST /api/v1/questions/<questionId>/answers/<answerId>/comments` 
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
    (myenv)$ python run.py
   ```
#### **Run Tests**
  ```
  (myenv)$ pytest --cov=api
  ```
