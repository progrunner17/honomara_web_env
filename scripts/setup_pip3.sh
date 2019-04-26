#!/bin/bash
set -eu

pushd $(dirname $0)

sudo apt install python3-pip -y
sudo pip3 install --upgrade pip

popd 
