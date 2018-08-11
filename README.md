# StackOverFlowLiteApi

## Introduction
* An API for the StackOverFLow hosted  **[```here:```](https://thesteelguy.github.io/StackOverFowLite/)**). front end app.
* StackOverFLowLite a platform where people can ask questions and provide answers. .
## NB
The app purely uses python data structures hence no persistance, however another version will be available fro data persistance

## Technologies used & needed.
* **[Python2](https://www.python.org/downloads/)**).
* **[Flask](flask.pocoo.org/)**  

## Link to heroku:
https://infinite-dusk-68356.herokuapp.com/
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
    `GET /api/v1/questions/<quetionId>` 
    ```
    headers = {content_type:application/json} 
    ```
    

* #### Provide an answer to a question.
    `POST /api/v1/questions/questionId/answers`:
    ```
    headers = {content_type:application/json}

    {
        "answe": "answer description"
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
    (myenv)$ export CONFIG_ENVIROMENT=production **to run *under produnction environment**
    ```

#### **Run the app**
   ```
    (myenv)$ python run.py
   ```
#### **Run Tests**
  ```
  (myenv)$ pytest --cov=tests
  ```
