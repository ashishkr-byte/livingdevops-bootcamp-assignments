#!/usr/bin/env bash
set -e

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Starts Flask app with Gunicorn on port 8000
gunicorn --workers 2 --bind 0.0.0.0:8000 app:app
