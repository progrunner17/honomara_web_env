#!/bin/bash

pushd $(dirname $0)

curl -sS https://getcomposer.org/installer |php
sudo mv composer.phar /usr/local/bin/composer

popd
