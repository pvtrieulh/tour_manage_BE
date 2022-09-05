#!/usr/bin/env bash
source ~/app/production/venv/bin/activate
cd ~/app/production/tetviet/src/tetviet/
python manage.py push_notification
deactivate
