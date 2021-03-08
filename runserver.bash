#!/bin/bash

cd backend
pipenv run python3 manage.py migrate
pipenv run python3 manage.py runserver &
cd ../frontend
npm start &
cd ..