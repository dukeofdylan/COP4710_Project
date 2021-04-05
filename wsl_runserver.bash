#!/bin/bash

cd $(dirname $0)
python3 -m pipenv run project/manage.py makemigrations
python3 -m pipenv run project/manage.py migrate
python3 -m pipenv run project/manage.py runserver