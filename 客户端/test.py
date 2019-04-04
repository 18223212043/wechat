# from tkinter import *

# def data():
#     for i in range(50):
#        Label(frame,text=i).grid(row=i,column=0)
#        Label(frame,text="my text"+str(i)).grid(row=i,column=1)
#        Label(frame,text="..........").grid(row=i,column=2)

# def myfunction(event):
#     canvas.configure(scrollregion=canvas.bbox("all"),width=750,height=400)

# root=Tk()
# sizex = 800
# sizey = 600
# posx  = 100
# posy  = 100
# root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))


# myframe=Frame(root,relief=GROOVE,width=750,height=400,bd=1)
# myframe.pack()


# canvas=Canvas(myframe)
# frame=Frame(canvas)
# myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
# canvas.configure(yscrollcommand=myscrollbar.set)

# myscrollbar.pack(side="right",fill=BOTH)
# canvas.pack(side="left")
# canvas.create_window((0,0),window=frame,anchor='nw')
# root.bind("<Enter>",myfunction)
# data()
# root.mainloop()


# import tkinter

# frame = tkinter.Frame()
# #:建一个canvas,和一个Label
# C = tkinter.Canvas(frame, bg="blue", height=300, width=300)
# label = tkinter.Label(C, text='hello' )
# #将Label放置到坐上点在Canvas的纵横30%的处
# label.place( height=100, width=100,relx= 0.3, rely=0.3)
# C.pack()
# C.create_window((100,100),window=frame,anchor='w',width=388,height=200)

# from datetime import datetime
# print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# import json
# dic = {
#     'myid':'myid',
#     'friend_id':'friend_id',
#     'content':'text',
#     'send_time':'send_time'
# }
# jsonstr = json.dumps(dic)
# print(jsonstr)


# from threading import Thread
# from socket import *
# import os

# def main():
#     print('主线程')
#     pid = os.fork()
#     if pid == 0:
#         child()
#     else:
#         s = socket(AF_INET,SOCK_DGRAM)
#         s.recvfrom(1024)
    

# def child():
#     print('子线程')
    

# main()
# import random
# port = random.randint(10000,60000)
# print(port)

# import os
# from multiprocessing import Queue
# import time
# from tkinter import *
# q = Queue(maxsize = 100)



# class child():
#     def __init__(self):
#         self.root = Tk()
#         q.put()
#         self.root.mainloop()
        
    

# pid = os.fork()
# if pid == 0:
#     child()
# else:
#     time.sleep(1)
#     print(1)
#     root = q.get()
#     print(root)
#     time.sleep(10)


s = (1,2)
a = [(1,2),(2,2)]
print(s in a)

