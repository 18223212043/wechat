from models import client
import os
from .aotuGetTime import *

class ClientAddr(client.Client):
    def __init__(self,userid,username,password,loginip,loginport):
        super().__init__(userid,username,password)
        self.loginip = loginip
        self.loginport = loginport
        self.logintime = get_current_time()
        # 获取日志保存路径
        self.base_dir = os.path.dirname('log')
        self.doc_login_msg()

    def __str__(self):
        ret = "帐号：%s,登录时间：%s"%(self.userid,self.logintime)
        return ret

    def doc_login_msg(self):
        try:
            filename = os.path.join(self.base_dir,self.userid+'.txt')
            f = open(filename,mode = "a")
            msg = "帐号%s:%s,在%s登录"%(self.userid,self.logintime,self.loginip)
            f.write(msg)
        except:
            print("写入文件失败")
        finally:
            f.close()