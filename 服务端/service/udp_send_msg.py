from socket import *

def udp_send_msg(addr,msg):

    s = socket(AF_INET,SOCK_DGRAM)

    s.sendto(msg.encode(),addr)
    print('发送完毕')

    s.close()