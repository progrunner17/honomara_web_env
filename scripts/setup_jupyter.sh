#!/bin/bash
set -eu

pushd $(dirname $0)

if ! (type pip3 > /dev/null 2>&1); then
./setup_pip3.sh
fi
sudo pip3 install jupyter 
sudo pip3 install bash_kernel 
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
