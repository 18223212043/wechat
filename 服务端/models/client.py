


class Client:
    def __init__(self,userid,username,password):
        self.userid = userid
        self.username = username
        self.password = password

    def __str__(self):
        ret = "帐号：%s,昵称：%s"%(self.userid,self.username)