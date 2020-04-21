#!/bin/bash
set -eux
# delete db
sudo -u postgres psql -c 'DROP DATABASE  IF EXISTS honomara;'
# create db
sudo -u postgres psql -c "CREATE DATABASE honomara ENCODING=UTF8 OWNER=honomara;"
export PGPASSWORD=honomara
# create tables
psql -U honomara -d honomara -f /vagrant/sql/create.sql

# import datas to postgres
[ -f /vagrant/sql/latest_dump.utf8.sql ] || echo "execute ./get_pg_dump.sh on host"
psql -U honomara -d honomara -f /vagrant/sql/latest_dump.utf8.sql
