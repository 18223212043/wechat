

import pymysql
from .db_conf import *

class DBOper:
    def __init__(self):
        self.conn = None

    def open_conn(self):
        try:
            conn = pymysql.connect(host,user,passwd,dbname)

            self.conn = conn
            self.cursor = conn.cursor()
        except Exception as e:
            print("数据库连接失败")
    
    def close_conn(self):
        try:
            self.conn.close()

        except Exception as e:
            print("数据库关闭失败")

    def do_query(self,sql):
        if not sql or sql == "":
            print("SQL语句不合法")
            return None

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)

            result = cursor.fetchall()
            
            cursor.close()
            return result

        except Exception as e:
            print("查询出错")
            return None

    def do_update(self,sql):
        if not sql or sql == "":
            print("SQL语句不合法")

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)

            self.conn.commit()
            cursor.close()

        except Exception as e:
            print("修改出错")
