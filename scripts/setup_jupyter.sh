#!/bin/sh
set -eu

if ! (type pip3 > /dev/null 2>&1); then
./setup_pip3.sh
fi
sudo pip3 install jupyter 

HOME=/home/vagrant
mkdir -p $HOME/.jupyter
cat > $HOME/.jupyter/jupyter_notebook_config.py  <<EOF
c.NotebookApp.token = ''
c.NotebookApp.password = ''
c.NotebookApp.port = 9999
c.NotebookApp.open_browser = False
c.NotebookApp.ip ='0.0.0.0'
EOF

