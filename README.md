[![Build Status](https://travis-ci.org/TheSteelGuy/StackOverFlowLiteApi.svg?branch=159714040-ch2-testcases)](https://travis-ci.org/TheSteelGuy/StackOverFlowLiteApi)
[![Coverage Status](https://coveralls.io/repos/github/TheSteelGuy/StackOverFlowLiteApi/badge.svg?branch=159714040-ch2-testcases)](https://coveralls.io/github/TheSteelGuy/StackOverFlowLiteApi?branch=159714040-ch2-testcases)
[![Maintainability](https://api.codeclimate.com/v1/badges/c9337d2239165a70a7db/maintainability)](https://codeclimate.com/github/TheSteelGuy/StackOverFlowLiteApi/maintainability)
# StackOverFlowLiteApi

## Introduction
* StackOverFLowApi is An API for the StackOverFLow hosted front end up  **[```here```](https://thesteelguy.github.io/StackOverFowLite/)**).
* StackOverFLowLite a platform where people can ask questions and provide answers. .
## NB
The app purely uses python data structures hence no persistance, however another version will be available fro data persistance

## Technologies used & needed.
* **[Python2](https://www.python.org/downloads/)**).
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
    by default if you dont pass any ENV VAR, the sever runs with development configarations
    ```
### **if you want to test other enviroments type:**
    ```
    (myenv)$ export CONFIG_ENVIROMENT=production to run *under produnction environment
    ```

#### **Run the app**
   ```
    (myenv)$ python run.py
   ```
#### **Run Tests**
  ```
  (myenv)$ pytest --cov=tests
  ```
