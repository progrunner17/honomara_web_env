#!/bin/sh
set -eu 

echo "mysql-server-5.7 mysql-server/root_password password honomara" |sudo debconf-set-selections -
echo "mysql-server-5.7 mysql-server/root_password_again password honomara" |sudo debconf-set-selections -
sudo apt install  mysql-server-5.7 mysql-client-5.7 -y
if ! (type pip3 > /dev/null 2>&1); then
./setup_pip3.sh
fi
sudo pip3 install mysql-connector-python
