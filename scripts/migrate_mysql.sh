#!/bin/bash
set -eux
### reset mysql
mysql  -u root --password='honomara' -e "DROP DATABASE honomara;"
mysql  -u root --password='honomara' -e "CREATE DATABASE IF NOT EXISTS honomara CHARACTER SET 'utf8';"
mysql  -u root --password='honomara' -e "GRANT ALL PRIVILEGES ON honomara.* TO  honomara;"

python3 migrate_mysql.py

echo finish reset!!
