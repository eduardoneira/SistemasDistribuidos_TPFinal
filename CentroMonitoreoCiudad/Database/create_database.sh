#!/usr/bin/env bash

sudo -i -u postgres psql -c "CREATE DATABASE cmc_db"
sudo -i -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE cmc_db to postgres"

pip3 install --user psycopg2

python3 create_database.py