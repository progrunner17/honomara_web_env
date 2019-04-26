#!/bin/bash
set -eu 

pushd $(dirname $0)

echo "mysql-server-5.7 mysql-server/root_password password honomara" |sudo debconf-set-selections -
echo "mysql-server-5.7 mysql-server/root_password_again password honomara" |sudo debconf-set-selections -
sudo apt install  mysql-server-5.7 mysql-client-5.7 -y


if ! (pythin3 -c 'import mysql.connector'); then
  if ! (type pip3 > /dev/null 2>&1); then
  ./setup_pip3.sh
  fi
  sudo pip3 install mysql-connector-python
  echo "create db named honomara"
  mysql  -u root --password='honomara' -e "CREATE DATABASE IF NOT EXISTS honomara CHARACTER SET 'utf8';"
  echo "create user named honomara"
  mysql  -u root --password='honomara' -e "CREATE USER IF NOT EXISTS honomara IDENTIFIED BY 'honomara';"
  echo "add ownership to user honomara on db honomara"
  mysql  -u root --password='honomara' -e "GRANT ALL PRIVILEGES ON honomara.* TO  honomara;"
fi

popd
