#!/bin/bash
set -eux
### reset mysql
MYSQL_PWD='honomara' mysql -u root <<EOF
DROP DATABASE IF EXISTS honomara;
CREATE DATABASE IF NOT EXISTS honomara CHARACTER SET 'utf8';
CREATE USER IF NOT EXISTS honomara IDENTIFIED BY 'honomara';
GRANT ALL PRIVILEGES ON honomara.* TO  honomara;
EOF

cat /vagrant/scripts/create_tables_mysql.sql | MYSQL_PWD='honomara' mysql -u root honomara

MECABRC=/etc/mecabrc python3 /vagrant/scripts/migrate_data_to_mysql.py

cat /vagrant/scripts/add_foreign_key_const.sql | MYSQL_PWD='honomara' mysql -u root honomara

