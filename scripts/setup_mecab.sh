#!/bin/bash
set -eu 

pushd $(dirname $0)

sudo apt install mecab libmecab-dev mecab-ipadic-utf8 swig -y
if ! (type pip3 > /dev/null 2>&1); then
./setup_pip3.sh
fi
sudo pip3 install mecab-python3

popd

