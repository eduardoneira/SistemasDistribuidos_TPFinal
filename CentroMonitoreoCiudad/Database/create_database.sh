#!/usr/bin/env bash

sudo -i -u postgres psql -c "CREATE DATABASE cmcdatabase"
sudo -i -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE cmcdatabase to postgres"

pip3 install --user psycopg2

python3 create_database.py