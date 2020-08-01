#!/usr/bin/env bash
set -eu

sudo apt-add-repository -y ppa:ondrej/php
#sudo apt update
echo "mysql-server-5.7 mysql-server/root_password password honomara"       |sudo debconf-set-selections -
echo "mysql-server-5.7 mysql-server/root_password_again password honomara" |sudo debconf-set-selections -

sudo apt install -y python3-pip \
  postgresql-9.5 postgresql-server-dev-9.5 \
  mysql-server-5.7 mysql-client-5.7 \
  apache2 libapache2-mod-php7.3 \
  php7.3 php7.3-cli php7.3-common php7.3-pgsql php7.3-mysql \
  language-pack-ja mecab libmecab-dev mecab-ipadic-utf8 swig

sudo -H python3 -m pip install --upgrade pip
sudo -H python3 -m pip install --upgrade psycopg2
sudo -H python3 -m pip install --upgrade mysql-connector-python
sudo -H python3 -m pip install --upgrade mecab-python3
sudo -H python3 -m pip install --upgrade flask flask-sqlalchemy flask-wtf flask-bootstrap flask-login flask-bcrypt

# configure postgresql (enable password login for psql command)
sudo perl -i.bak -pe 's/^(local\s+all\s+all\s+)peer/$1md5/' /etc/postgresql/9.5/main/pg_hba.conf

sudo chmod a+rw /var/www/html

# configure apache cgi
sudo a2enmod cgi
[ -L /usr/lib/cgi-bin  ] || sudo rmdir /usr/lib/cgi-bin
mkdir -p /vagrant/app
sudo ln -s /vagrant/app /usr/lib/cgi-bin
sudo chmod 755 /usr/lib/cgi-bin

# configure apache rewrite
sudo sed -i -E 's/(AllowOverride\s+)None/\1All/g' /etc/apache2/apache2.conf
sudo sed -i -E 's/(AllowOverride\s+)None/\1All/g' /etc/apache2/conf-enabled/serve-cgi-bin.conf
sudo a2enmod rewrite

cat > /var/www/html/.htaccess <<EOF
RewriteEngine On
RewriteRule ^cgi-bin\$ /cgi-bin/index.cgi [L,QSA]
EOF
chmod 604 /var/www/html/.htaccess

# restart daemons
sudo systemctl restart postgresql
sudo systemctl restart apache2
