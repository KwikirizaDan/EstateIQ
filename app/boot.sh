#!/bin/bash
export FLASK_APP=app.py
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
exec gunicorn --bind 0.0.0.0:5000 wsgi:app