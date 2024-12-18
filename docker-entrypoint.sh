#!/bin/sh

# Startup OpenSSH daemon
/usr/sbin/sshd

# Run uwsgi
#uwsgi --http :80 --wsgi-file app.py --callable app -b 32768 --master --thunder-lock --enable-threads
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
