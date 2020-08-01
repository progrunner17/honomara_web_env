#!/bin/sh
set -eux

source ./env.sh # create env.sh and set ENV_PGPASSWORD
mkdir -p ./dump
file="./dump/dump_data_postgres_$(date +%s).sql"
ssh -C honomara sh > $file <<-EOF
PGPASSWORD="${ENV_PGPASSWORD}" pg_dump -a honomara --inserts
EOF

file_utf8=${file%%.sql}.utf8.sql
nkf -Ew -Lu ${file}   >| ${file_utf8}
ruby -i.raw -ne '
BEGIN{del=false}
if /(EUC_JP|ai_.*_seq)/ =~ $_ then
  next
end

if /^--\s+\S/  =~ $_ then
  del=false
end

if /Data for Name:.*(ai_.*dic|update|apollo|meibo|afterbbs)/  =~ $_ then
  del=true
end

if ! del then
  print $_
end
' ${file_utf8}

if [ -e latest_dump.utf8.sql -a ! -L latest_dump.utf8.sql ] ;then
  mv ./latest_dump.utf8.sql ./latest_dump.utf8.sql.bak
fi

rm -f ./latest_dump.utf8.sql
cp ${file_utf8} ./latest_dump.utf8.sql
