#!/bin/sh 
set -eu

#install postgresql
sudo apt install  postgresql-9.5 postgresql-server-dev-9.5 -y

# enable password login for postgresql
sudo sed -i 's/^local\s*all\s*all\s*peer/local\tall\tall\tmd5/g'\
  /etc/postgresql/9.5/main/pg_hba.conf
sudo systemctl restart postgresql


if ! (python3 -c 'import psycopg2'); then
  if ! (type pip3 > /dev/null 2>&1); then
  ./setup_pip3.sh
  fi
  sudo pip3 install psycopg2
  sudo -u postgres psql -c "CREATE ROLE honomara WITH LOGIN PASSWORD 'honomara';"
  sudo -u postgres psql -c "CREATE DATABASE honomara ENCODING=UTF8 OWNER=honomara;"
fi
