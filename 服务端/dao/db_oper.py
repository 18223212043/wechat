

import pymysql
from .db_conf import *

class DBOper:
    def __init__(self):
        self.conn = None

    def open_conn(self):
        try:
            conn = pymysql.connect(host,user,passwd,dbname,charset='utf8')

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
            print(e)
            print("查询出错")
            return None

    def do_update(self,sql):
        if not sql or sql == "":
            print("SQL语句不合法")

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)

            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
            return 'update_False'
        else:
            return 'update_True'
        finally:
            cursor.close()

    def do_double_update(self,sql1,sql2):
        if (not sql1 or sql1 == "") and (not sql2 or sql2 == ""):
            print("SQL语句不合法")

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql1)
            cursor.execute(sql2)

            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
            return 'update_False'
        else:
            return 'update_True'
        finally:
            cursor.close()