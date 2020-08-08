#!/bin/bash
set -eux

MYSQL_PWD='honomara' mysqldump -u root honomara > mysql_backup.sql

