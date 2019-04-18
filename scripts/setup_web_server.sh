#!/bin/sh
set -eu
sudo apt-add-repository -y ppa:ondrej/php
sudo apt update -y
sudo apt install -y  apache2
sudo apt install -y libapache2-mod-php7.3 php7.3 php7.3-cli php7.3-common
sudo apt install -y php7.3-pgsql
sudo apt install -y php7.3-mysql
sudo chmod a+rw /var/www/html
