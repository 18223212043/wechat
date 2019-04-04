import select
from service.msg_parse import *
from threading import Thread


# 存储已经登录的用户
login_user = {}
# 存储用户打开的对话窗口所对应的udp地址和端口，以用户和好友id的元组作为键,地址作为值
session_addr = {}

def main():
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(('0.0.0.0',12314))
    s.listen(3)

    rlist = [s]
    wlist = []
    xlist = []

    while True:
        rl,wl,xl = select.select(rlist,wlist,xlist)
        for r in rl:
            if r is s:
                c,addr = r.accept()
                print("Connect from:",addr)

                #创建子线程处理连接进来的客户端请求
                t = Thread(target=do_child,args=(c,))
                t.setDaemon(True)
                t.start()
                t.join()
            
def do_child(c):
    msg = c.recv(1024*1024).decode()


    print('Break from:',c.getpeername())

    response =  msg_parse(msg,c,login_user,session_addr)
    c.send(response.encode())
    c.close()

if __name__ == '__main__':
    main()
