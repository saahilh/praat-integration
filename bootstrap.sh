#!/bin/sh
export FLASK_APP=./backend/server.py
pipenv run flask --debug run -h 0.0.0.0