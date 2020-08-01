#!/bin/bash
set -eu

pushd $(dirname $0)

sudo apt install -y python3 python3-pip

sudo -H python3 -m pip install --upgrade pip
sudo -H python3 -m pip install jupyter
sudo -H python3 -m pip install bash_kernel
sudo python3 -m bash_kernel.install

HOME=/home/vagrant
mkdir -p $HOME/.jupyter
cat > $HOME/.jupyter/jupyter_notebook_config.py  <<EOF
c.NotebookApp.token = ''
c.NotebookApp.password = ''
c.NotebookApp.port = 9999
c.NotebookApp.open_browser = False
c.NotebookApp.ip ='0.0.0.0'
EOF

popd
