#!/bin/sh
set -eu

# import data of honomara
sudo -u postgres psql -c "CREATE ROLE honomara WITH LOGIN PASSWORD 'honomara';"
sudo -u postgres psql -c "CREATE DATABASE honomara ENCODING=UTF8 OWNER=honomara;"
SQL_DIR=../sql
export PGPASSWORD=honomara
psql -U honomara -d honomara -f ${SQL_DIR}/create.sql
psql -U honomara -d honomara -f ${SQL_DIR}/person_data.sql
psql -U honomara -d honomara -f ${SQL_DIR}/after_data.sql
psql -U honomara -d honomara -f ${SQL_DIR}/training_data.sql
psql -U honomara -d honomara -f ${SQL_DIR}/participants_data.sql
psql -U honomara -d honomara -f ${SQL_DIR}/race_data.sql
psql -U honomara -d honomara -f ${SQL_DIR}/distance_data.sql
psql -U honomara -d honomara -f ${SQL_DIR}/result_data.sql