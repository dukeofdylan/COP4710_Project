#!/bin/bash

sudo apt-get python3-pip
sudo add-apt-repository ppa:ubuntugis/ppa
sudo apt-get update
python3 -m pip install pipenv --user
python3 -m pipenv install
sudo apt install gdal-bin python-gdal python3-gdal