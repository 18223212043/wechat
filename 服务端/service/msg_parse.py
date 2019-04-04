import json,os
from .manage import *
from .udp_send_msg import *
from datetime import datetime
from service import udp_send_msg

def msg_parse(data,c,login_user,session_addr):
    data_arr = data.split("\n")
    if data_arr[0] == "register":
        return do_register(data_arr[1:])
    if data_arr[0] == "login":
        return do_login(data_arr[1:],c,login_user)
    if data_arr[0] == 'updateNickname':
        return do_update_nickname(data_arr[1:])
    if data_arr[0] == 'updateSignature':
        return do_update_signature(data_arr[1:])
    if data_arr[0] == 'getGroup':
        return do_get_group(data_arr[1:],login_user)
    if data_arr[0] == 'getFriendByGroup':
        return do_get_friend(data_arr[1:])
    if data_arr[0] == 'sendMsg':
        return do_send_msg(data_arr[1:],session_addr)
    if data_arr[0] == 'getMsg':
        return do_get_msg(data_arr[1:])
    if data_arr[0] == 'searchUser':
        return do_search_user(data_arr[1:])
    if data_arr[0] == 'addFriend':
        return do_add_friend(data_arr[1:],login_user)
    if data_arr[0] == 'acceptAdd':
        return do_accept_add(data_arr[1:],login_user)
    if data_arr[0] == 'refuseAdd':
        return do_refuse_add(data_arr[1:], login_user)
    if data_arr[0] == 'sendMsgPort':
        return do_save_session_addr(data_arr[1:],c,session_addr)


# 处理注册请求
def do_register(arr):
    um = UserManage()
    gm = GroupManage()
    try:
        # 得到请求中的数据
        main_arr = arr[0].split(",")
        # 在数据库中通过用户名查找
        query_result = um.query_user_by_username(main_arr[0])
        if not query_result:
            um.insert_user(main_arr[0],main_arr[1],main_arr[2],main_arr[3])
            id = um.query_id_by_username(main_arr[0])[0][0]
            gm.insert_first_group(id)
            return "register_True\n"
        else:
            return "username_Exist\n"
    except Exception as e:
        print(e)
        return 'register_False'

# 处理登录请求
def do_login(arr,c,login_user):
    um = UserManage()
    main_arr = arr[0].split(',')
    query_result = um.query_user_by_username(main_arr[0])
    if query_result:
        # 获取查询到的用户信息
        user_info = query_result[0]
        # 判断用户输入的密码和数据库中查询出来的密码是否相等
        if main_arr[1] != user_info[2]:
            return 'user_Error\n'
        elif main_arr[1] == user_info[2]:
            # 密码相等则登录成功并将用户id作为键用户地址作为值存入login_user中
            login_user[user_info[0]] = (c.getpeername()[0],int(main_arr[2]))
            if user_info[5] is None:
                return 'login_True\n%d,%s,%d,%s,null' % (user_info[0], user_info[1], user_info[3], user_info[4])
            else:
                return 'login_True\n%d,%s,%d,%s,%s'%(user_info[0],user_info[1],user_info[3],user_info[4],user_info[5])
    else:
        return 'user_Error\n'

# 处理更新昵称请求
def do_update_nickname(arr):
    um = UserManage()
    main_arr = arr[0].split(',')
    update_result = um.update_nickname(main_arr[0],main_arr[1])
    return update_result

# 更新个性签名请求
def do_update_signature(arr):
    um = UserManage()
    main_arr = arr[0].split(',')
    update_result = um.update_signature(main_arr[0], main_arr[1])
    return update_result

# 处理获取分组请求
def do_get_group(arr,login_user):
    gm = GroupManage()
    fm = FriendManage()
    main_arr = arr[0].split(',')
    # 通过用户id查询到相关的分组
    query_group_result = gm.query_group_by_userid(main_arr[0])
    msg = 'groupInfo'
    for group in query_group_result:
        # 获取分组中好友的总数量
        friend_count = fm.query_friend_count_by_groupid(group[0])
        # 获取分组中所有好友的id
        group_friend_id = fm.query_friend_by_groupid(group[0])
        # 初始化在线好友数量
        online_friend_count = 0
        # 通过循环判断好友是否在已登录用户中
        for friend_id in group_friend_id:
            if friend_id[0] in login_user:
                online_friend_count += 1
        msg += '\n%d,%s,%d,%d'%(group[0],group[1],online_friend_count,friend_count[0][0])
    return msg

# 处理获取分组中好友的请求
def do_get_friend(arr):
    um = UserManage()
    fm = FriendManage()
    main_arr = arr[0].split(',')
    #通过分组id获取分组中的所有好友id
    group_friend_id = fm.query_friend_by_groupid(main_arr[0])
    msg = 'friendInfo'
    for friend_id in group_friend_id:
        #通过friend_id查询好友的详细信息
        friend_info = um.query_user_by_id(friend_id[0])[0]
        if friend_info[3] is None:
            msg += '\n%d,%s,%s,什么也没有留下' % (friend_info[0], friend_info[1], friend_info[2])
        else:
            msg += '\n%d,%s,%s,%s'%(friend_info[0],friend_info[1],friend_info[2],friend_info[3])
    return msg


#　处理查找好友请求
def do_search_user(arr):
    um = UserManage()
    main_arr = arr[0].split(',')
    # 得到查询内容
    search_result = um.query_users_by_content(main_arr[0])
    users = []
    if search_result:
        for user in search_result:
            dic = {
                'id':user[0],
                'username':user[1],
                'nickname':user[2]
            }
            users.append(dic)
        jsonstr = json.dumps(users)
        return jsonstr
    else:
        return 'No_Result'



# 处理添加好友请求
def do_add_friend(arr,login_user):
    afrm = AddFriendRecordManage()
    main_arr = arr[0].split(',')
    myid = main_arr[0]
    add_id = main_arr[1]
    mynickaname = main_arr[2]
    add_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 通过自己的id和要添加的id判断该用户是否已经被添加为好友
    queryresult = afrm.query_is_friend(myid,add_id)
    if not queryresult:
        # 将添加记录插入添加好友的记录表中
        insert_result = afrm.insert_record(myid,add_id,add_datetime)
        if insert_result == 'update_True':
            # 添加记录成功则查询该条记录id
            add_friend_record_id = afrm.query_record_id(myid,add_id,add_datetime)[0][0]
            # 判断要添加的用户是否已经登录，已经登录则将添加信息发送过去
            if int(add_id) in login_user.keys():
                msg = {
                    'header':'add',
                    'record_id':add_friend_record_id,
                    'add_id':myid,
                    'add_nickname':mynickaname
                }
                jsonstr = json.dumps(msg)
                udp_send_msg.udp_send_msg(login_user[int(add_id)],jsonstr)
        return insert_result
    return 'friend_Exsit'


# 处理发送消息请求
def do_send_msg(arr,session_addr):
    mm = MessageManage()
    # 通过长度判断是否后面的内容被分割
    if len(arr)>1:
        main_info = ('\n').join(arr)
    else:
        main_info = arr[0]
    # 解析json字符串
    main_dic = json.loads(main_info)
    # 获取发送的内容
    content = main_dic['content'].split('\n')[0]
    result = mm.insert_msg_record(main_dic['myid'],main_dic['friend_id'],content,main_dic['send_time'])
    key = (str(main_dic['friend_id']),str(main_dic['myid']))
    # 如果插入成功并且朋友已经登录则将消息通过udp形式发送给好友
    if result == 'update_True' and key in session_addr:
        addr = session_addr[key]
        msg_dic = {
            'content':main_dic['content'],
            'send_time':main_dic['send_time']
        }
        jsonstr = json.dumps(msg_dic)
        # 将消息用udp方式发送过去
        udp_send_msg.udp_send_msg(addr,jsonstr)
    return  result

# 处理获取消息请求
def do_get_msg(arr):
    mm = MessageManage()
    main_arr = arr[0].split(',')
    myid = main_arr[0]
    friend_id = main_arr[1]
    msg_record = mm.query_record_by_id(myid,friend_id)
    msg_list = []
    if msg_record:
        for msg in msg_record:
            msg_dic = {
                'from_id':msg[0],
                'to_id':msg[1],
                'content':msg[2],
                'send_time':msg[3].strftime('%Y-%m-%d %H:%M:%S')
            }
            msg_list.append(msg_dic)
        jsonstr = json.dumps(msg_list)
        return jsonstr
    else:
        return 'No_record'

# 处理接受添加好友请求
def do_accept_add(arr,login_user):
    um = UserManage()
    gm = GroupManage()
    fm = FriendManage()
    afrm = AddFriendRecordManage()
    main_arr = arr[0].split(',')
    print(main_arr)
    record_id = main_arr[0]
    # 接受方id
    accepter_id = main_arr[1]
    # 发起方id
    initiator_id = main_arr[2]
    # 更新加好友记录表中的添加状态为1
    update_result = afrm.update_isAdd1(record_id)
    if update_result == 'update_True':
        # 将接受方加入发起方的默认的分组的好友中
        # 查询到默认分组的id
        initiator_group_id = gm.query_id(initiator_id)[0][0]
        accepter_group_id =  gm.query_id(accepter_id)[0][0]
        #　将分组id和好友id插入friend表中
        add_result = fm.insert_friend(initiator_group_id,accepter_id,accepter_group_id, initiator_id)
        if add_result == 'update_True':
            #　向发起方发送消息提示添加好友成功
            accept_info = um.query_user_by_id(accepter_id)[0]
            if accept_info[3] is None:
                msg_dic = {
                    'header':'add_success',
                    'group_id':initiator_group_id,
                    'friend_id':accept_info[0],
                    'friend_username':accept_info[1],
                    'friend_nickname':accept_info[2],
                    'friend_signature':'没有什么留下'
                }
            else:
                msg_dic = {
                    'header': 'add_success',
                    'group_id': initiator_group_id,
                    'friend_id': accept_info[0],
                    'friend_username': accept_info[1],
                    'friend_nickname': accept_info[2],
                    'friend_signature': accept_info[3]
                }
            jsonstr = json.dumps(msg_dic)
            udp_send_msg.udp_send_msg(login_user[int(initiator_id)],jsonstr)
    return add_result

# 处理拒绝添加好友请求
def do_refuse_add(arr,login_user):
    afrm = AddFriendRecordManage()
    main_arr = arr[0].split(',')
    record_id = main_arr[0]
    # 接受方id
    refuse_nickname = main_arr[2]
    # 发起方id
    initiator_id = main_arr[3]
    # 更新加好友记录表中的添加状态为2
    update_result = afrm.update_isAdd2(record_id)
    msg_dic = {
        'header': 'add_failed',
        'refuse_nickname':refuse_nickname
    }
    jsonstr = json.dumps(msg_dic)
    udp_send_msg.udp_send_msg(login_user[int(initiator_id)],jsonstr)
    return update_result

# 保存会话地址请求
def do_save_session_addr(arr,c,session_addr):
    main_arr = arr[0].split(',')
    myid = main_arr[0]
    friend_id = main_arr[1]
    port = int(main_arr[2])
    session_addr[(myid,friend_id)] = (c.getpeername()[0],port)

    return 'save_True'

# 处理退出请求
def login_out():
    pass
