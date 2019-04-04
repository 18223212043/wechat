

import socket

#发送一次请求就断开
def send_request(msg):
    s = socket.socket()

    s.connect(('176.221.18.72',12314))

    s.send(msg.encode())
    
    data = b''
    while True:
        data1 = s.recv(1024)
        if not data1:
            break
        data += data1

    s.close()
    return data.decode()

