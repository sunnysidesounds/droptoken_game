#!/usr/bin/env bash
sleep 10

set FLASK_APP="app.py"

python app.py
echo -e 'app started'