import mysql.connector
import os


class MySQL:
    _conn = None
    _dns = None
    _conn_num = 0
    _dns = {
        'user': os.environ['MYSQL_DB_USER'],
        'host': os.environ['MYSQL_DB_HOST'],
        'password': os.environ['MYSQL_DB_PASS'],
        'database': os.environ['MYSQL_DB_NAME']
    }

    def __init__(self):
        if (not MySQL._conn) or MySQL._conn_num == 0:
            mysql.connector.MySQLConnection(**self.dns)
        MySQL._conn_num += 1

    def __del__(self):
        MySQL._conn_num -= 1
        if MySQL._conn_num == 0:  # need to be atomic... but...
            MySQL._conn.close()

    def query(self, stmt, *args, **kwargs):
        with MySQL._conn.cursor() as cursor:
            cursor.execute(stmt)
            data = cursor.fetchall()
        return data

    def exec(self, stmt, *args, **kwargs):
        with MySQL._conn.cursor() as cursor:
            cursor.execute(stmt)
        MySQL._conn.commit()
