
from .manage import *


def msg_parse(data):
    data_arr = data.split("\n")
    cm =ClientManage()
    if data_arr[0] == "register":
        return do_register(data_arr[1],cm)
    if data_arr[0] == "login":
        return do_login()

# 处理注册请求
def do_register(arr,cm):
    # 得到请求中的用户名
    main_arr = arr.split(",")
    # 在数据库中查找用户名
    cherck_id = cm.queryById(main_arr[0])
    if not cherck_id:
        cm.insertClient(main_arr[0],main_arr[1],main_arr[2])
        return "register_True"
    else:
        print("帐号已存在")
        return "register_False"

# 处理登录请求
def do_login():
    pass

#　处理查找好友请求
def find_fridend():
    pass

# 处理添加好友请求
def add_fridend():
    pass

# 处理发送消息请求
def send_msg():
    pass

# 处理退出请求
def login_out():
    pass
