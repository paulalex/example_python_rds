#!/usr/bin/env bash
set -x

uwsgi --http :5000 --wsgi-file wsgi.py --ini uwsgi.ini --callable app --master --processes 1 --threads 2