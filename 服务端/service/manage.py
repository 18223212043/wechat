
from models import client
from dao import db_oper

class ClientManage:
    def __init__(self):
        self.db_oper = db_oper.DBOper()

    def queryById(self,userId):
        self.db_oper.open_conn()
        #拼接SQL
        sql = "select * from client where userid = '%s'"%userId
        #执行查询
        result = self.db_oper.do_query(sql)

        #关闭连接
        self.db_oper.close_conn()
        if not result:
            print("查询结果为空")
            return None
        else:
            for x in result:
                cl = client.Client(x[0],x[1],x[2])
            return cl

    def insertClient(self,userid,username,userpassword):
        self.db_oper.open_conn()
        #拼接插入sql
        sql = "insert into client values('%s','%s','%s')"%(userid,username,userpassword)

        self.db_oper.do_update(sql)
        print("插入成功")
        self.db_oper.close_conn()
