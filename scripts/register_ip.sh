#!/bin/bash
set -eu

source env.sh # set the variables in the following command
curl -X POST\
  -d "account=${XREA_ACCOUNT}" -d "server_name=${XREA_SERVER}" \
  -d "api_secret_key=${XREA_API_KEY}" \
  -d "param[addr]=$(curl -s ifconfig.me)" \
  https://api.xrea.com/v1/tool/ssh_ip_allow

