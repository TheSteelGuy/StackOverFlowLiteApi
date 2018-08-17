""" 
run.py
application entry point
"""
import os

from api.v1 import create_app
try:
    config = os.environ['CONFIG_ENVIRONMENT']
    app = create_app(config)
except KeyError:
    app = create_app('development')

if __name__ == ('__main__'):
    app.run()