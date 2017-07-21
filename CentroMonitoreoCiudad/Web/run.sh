#!/usr/bin/env bash
if [ -z ${FLASK_APP+x} ]; then
  export FLASK_APP=app.py;
fi
flask run --host=0.0.0.0
