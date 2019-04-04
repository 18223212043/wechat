
from dao import db_oper

class UserManage(object):
    def __init__(self):
        self.db_oper = db_oper.DBOper()

    def query_user_by_username(self,username):
        self.db_oper.open_conn()
        #拼接SQL
        sql = "select id,username,password,sex,nickname,signature from user where username = '%s'"%username
        #执行查询
        result = self.db_oper.do_query(sql)

        #关闭连接
        self.db_oper.close_conn()
        if not result:
            print("查询结果为空")
            return None
        else:
            return result

    def query_id_by_username(self,username):
        self.db_oper.open_conn()

        sql = "select id from user where username='%s'"%username
        result = self.db_oper.do_query(sql)

        self.db_oper.close_conn()

        return result

    def insert_user(self,username,password,sex,nickname):
        self.db_oper.open_conn()
        #拼接插入sql
        sql = "insert into user(username,password,sex,nickname,register_date,register_time) values('%s','%s',%s,'%s',curdate(),curtime())"%(username,password,sex,nickname)

        self.db_oper.do_update(sql)

        self.db_oper.close_conn()


    def update_nickname(self,id,nickname):
        self.db_oper.open_conn()
        #拼接更新nickname的sql
        sql = 'update user set nickname=%s where id=%s'%(nickname,id)

        result = self.db_oper.do_update(sql)
        return result

    def update_signature(self,id,signature):
        self.db_oper.open_conn()
        #拼接更新nickname的sql
        sql = 'update user set signature=%s where id=%s'%(signature,id)

        result = self.db_oper.do_update(sql)
        return result

    def query_user_by_id(self,id):
        self.db_oper.open_conn()

        sql = 'select id,username,nickname,signature from user where id=%s'%id

        result = self.db_oper.do_query(sql)

        return result

    def query_users_by_content(self,content):
        self.db_oper.open_conn()

        sql = "select id,username,nickname from user where username='%s' UNION \
               select id,username,nickname from user where nickname like '%s' "%(content,'%'+content+'%')

        result = self.db_oper.do_query(sql)

        return result

class GroupManage(object):
    def __init__(self):
        self.db_oper = db_oper.DBOper()

    def insert_first_group(self,user_id):
        self.db_oper.open_conn()

        sql = 'insert into friend_group(groupname,user_id) values("我的朋友",%d)'%user_id

        self.db_oper.do_update(sql)

    def query_group_by_userid(self,user_id):
        self.db_oper.open_conn()

        sql = 'select id,groupname from friend_group where user_id = %s'%user_id

        result = self.db_oper.do_query(sql)

        return result

    def query_id(self,user_id):
        self.db_oper.open_conn()

        sql = 'select id from friend_group where groupname="我的朋友" and user_id=%s'%user_id

        result = self.db_oper.do_query(sql)

        return result

class FriendManage(object):
    def __init__(self):
        self.db_oper = db_oper.DBOper()

    def query_friend_count_by_groupid(self,groupid):
        self.db_oper.open_conn()

        sql = 'select count(user_id) from friend where group_id=%d'%groupid

        result = self.db_oper.do_query(sql)

        return result

    def query_friend_by_groupid(self,groupid):
        self.db_oper.open_conn()

        sql = 'select user_id from friend where group_id = %s'%groupid

        result = self.db_oper.do_query(sql)

        return result

    def insert_friend(self,initiator_group_id,accepter_id,accepter_group_id, initiator_id):
        self.db_oper.open_conn()

        sql1 = 'insert into friend(group_id,user_id) values(%d,%s)'%(initiator_group_id,accepter_id)

        sql2 = 'insert into friend(group_id,user_id) values(%d,%s)'%(accepter_group_id,initiator_id)

        result = self.db_oper.do_double_update(sql1,sql2)

        return result


class MessageManage(object):
    def __init__(self):
        self.db_oper = db_oper.DBOper()

    def insert_msg_record(self,from_id,to_id,content,send_time):
        self.db_oper.open_conn()

        sql = 'insert into message(from_user,to_user,content,send_datetime) values(%s,%s,"%s","%s")'%(
            from_id,to_id,content,send_time
        )

        result = self.db_oper.do_update(sql)

        return result

    def query_record_by_id(self,myid,friend_id):
        self.db_oper.open_conn()

        sql = 'select from_user,to_user,content,send_datetime from message where from_user = %s ' \
              'and to_user = %s UNION select from_user,to_user,content,send_datetime from message ' \
              'where from_user = %s and to_user =%s order by send_datetime ASC' %(myid,friend_id,friend_id,myid)

        result = self.db_oper.do_query(sql)

        return result

class AddFriendRecordManage(object):
    def __init__(self):
        self.db_oper = db_oper.DBOper()

    def insert_record(self,myid,add_id,add_datetime):
        self.db_oper.open_conn()

        sql = 'insert into addfriendrecord(from_user,to_user,add_datetime) values("%s","%s","%s")'%(myid,add_id,add_datetime)

        result = self.db_oper.do_update(sql)

        return result

    def query_record_id(self,myid,add_id,add_datetime):
        self.db_oper.open_conn()

        sql = 'select id from addfriendrecord where from_user="%s" and to_user="%s" and add_datetime="%s"'%(myid,add_id,add_datetime)

        result = self.db_oper.do_query(sql)

        return result

    def update_isAdd1(self,record_id):
        self.db_oper.open_conn()

        sql = 'update addfriendrecord set is_add=1 where id=%s'%record_id

        result = self.db_oper.do_update(sql)

        return result

    def update_isAdd2(self,record_id):
        self.db_oper.open_conn()

        sql = 'update addfriendrecord set is_add=2 where id=%s'%record_id

        result = self.db_oper.do_update(sql)

        return result

    def query_is_friend(self,myid,add_id):
        self.db_oper.open_conn()

        sql = 'select friend.user_id from user,friend_group,friend where user.id = %s and user.id \
            = friend_group.user_id and friend_group.id = friend.group_id and friend.user_id = %s'%(myid,add_id)

        result = self.db_oper.do_query(sql)

        return result