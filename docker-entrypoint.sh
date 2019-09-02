#!/bin/bash

. env/bin/activate
pip install --upgrade Flask Flask-MySQLdb flask-swagger mysql-connector
pip install --upgrade -r /src/api/requirements.txt -t lib

export FLASK_ENV=development
export FLASK_APP=/src/api/main.py
flask run --host=0.0.0.0

eval "$@"
