#!/bin/bash

echo "Please, do not run me. I am only here for projects that do not have project.json and Pipfile.lock"
exit

PROJECT_NAME=rsomaker
sudo apt update && sudo apt upgrade


## Django
pip3 install pipenv
pipenv install django
pipenv run django-admin startproject cop4710
cd backend
pipenv run python3 manage.py startapp $PROJECT_NAME
pipenv run python3 manage.py migrate
cd ..


## Node
# sudo apt install nodejs npm
# npx create-react-app frontend
# cd frontend
# npm install bootstrap reactstrap axios
# mkdir src/components
# touch src/components/.gitkeep
# cd ..
