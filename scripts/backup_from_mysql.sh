#!/bin/bash
set -eux

mysqldump -u honomara --password=honomara honomara > mysql_backup.sql

