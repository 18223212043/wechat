import socket
import select,os,sys
from service.msg_parse import *

def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
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
                #创建子进程处理连接进来的客户端请求
                pid = os.fork()

                if pid == 0:
                    do_child(c)
                    print('Break from:',c.getpeername())
                    sys.exit()
            
def do_child(c):
    while True:
        msg = c.recv(1024*2).decode()
        if not msg:
            break
        response =  msg_parse(msg)
        c.send(response.encode())

if __name__ == '__main__':
    main()
