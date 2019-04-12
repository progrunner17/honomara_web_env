#!/bin/sh 
set -eu

#install postgresql
sudo apt install  postgresql-9.5 postgresql-server-dev-9.5 -y

# enable password login for postgresql
sudo sed -i 's/^local\s*all\s*all\s*peer/local\tall\tall\tmd5/g'\
  /etc/postgresql/9.5/main/pg_hba.conf
sudo systemctl restart postgresql

# import data of honomara
sudo -u postgres psql -c "CREATE ROLE honomara WITH LOGIN PASSWORD 'honomara';"
sudo -u postgres psql -c "CREATE DATABASE honomara ENCODING=UTF8 OWNER=honomara;"
SQL_DIR=/home/vagrant/host_data/sql
export PGPASSWORD=honomara
psql -U honomara -d honomara -f ${SQL_DIR}/create.sql
psql -U honomara -d honomara -f ${SQL_DIR}/person_data.sql
psql -U honomara -d honomara -f ${SQL_DIR}/after_data.sql
psql -U honomara -d honomara -f ${SQL_DIR}/training_data.sql
psql -U honomara -d honomara -f ${SQL_DIR}/participants_data.sql
psql -U honomara -d honomara -f ${SQL_DIR}/race_data.sql
psql -U honomara -d honomara -f ${SQL_DIR}/distance_data.sql
psql -U honomara -d honomara -f ${SQL_DIR}/result_data.sql
