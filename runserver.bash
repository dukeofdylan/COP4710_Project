#!/bin/bash

pipenv run cop4710/manage.py migrate
xfce4-terminal --hold --geometry 66x16-0-0 --title=backend -e "pipenv run cop4710/manage.py runserver"
# cd frontend
# xfce4-terminal --hold --geometry 66x16-0+0 --title=frontend -e "npm start"