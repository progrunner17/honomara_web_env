#!/bin/bash
set -eux
source env.sh
mysqldump -u root honomara > mysql_backup.sql

