

import socket

def send_request(msg):
    s = socket.socket()

    s.connect(('176.221.18.72',12314))

    s.send(msg.encode())

    data = s.recv(1024)

    s.close()
    print(data.decode())
    return data.decode()
    