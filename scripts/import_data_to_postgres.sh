#!/bin/bash
set -eux
# delete db
export PGPASSWORD=honomara
if ! (psql -U honomara -c "\d" >/dev/null 2>/dev/null) then
  sudo -u postgres psql -c "CREATE ROLE honomara WITH LOGIN ENCRYPTED PASSWORD 'honomara';"
fi
sudo -u postgres psql -c 'DROP DATABASE  IF EXISTS honomara;'
# create db
sudo -u postgres psql -c "CREATE DATABASE honomara ENCODING=UTF8 OWNER=honomara;"
# create tables
psql -U honomara -d honomara -f /vagrant/scripts/create_tables_postgres.sql
psql -U honomara -d honomara -f /vagrant/scripts/latest_dump.utf8.sql
