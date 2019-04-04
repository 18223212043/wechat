from tkinter import *
from datetime import datetime
import json,random
from tcpClient import *
from threading import Thread
from socket import *


class SendMsgPage():
    def __init__(self,myid,mynickname,friend_id,friend_nickname):
        self.port = random.randint(10000,60000)
        self.myid = myid
        self.mynickname = mynickname
        self.friend_id = friend_id
        self.friend_nickname = friend_nickname
        msg = 'sendMsgPort\n%s,%s,%d'%(self.myid,self.friend_id,self.port)
        response =  send_request(msg)
        if response == 'save_True':
            self.initForm()
            self.createFrame()
    
    def initForm(self):
        self.root = Tk()
        self.root.title(self.friend_nickname)
        width = 600
        height = 460
        self.root.maxsize(600,460)
        self.root.minsize(600,460)
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d"%(width,height,(screenwidth-width)/2,(screenheight-height)/2)
        self.root.geometry(alignstr)
        self.root['bg'] = '#2E3138'
    
    def createFrame(self):
        self.headFrame = Frame(self.root,bg='#2E3138')
        self.headFrame.pack(fill=BOTH)
        Label(self.headFrame,text=self.friend_nickname,bg='#2E3138',fg='#FBFFFF',font=('',12)).pack()
        # 利用Frame画一条分割线
        Frame(self.root,bg='#26292E').pack(ipady=1,fill='x')
        self.msg_frame = MsgFrame(self.root,self.myid,self.mynickname,self.friend_id,self.friend_nickname)
        # 利用Frame画一条分割线
        Frame(self.root,bg='#26292E').pack(ipady=1,fill='x')
        self.send_frame = SendFrame(self.root,self.msg_frame.frame1,self.msg_frame.canvas,
        self.myid,self.mynickname,self.friend_id,self.friend_nickname)
        t = Thread(target=self.udp_recv_msg,args=(self.port,))
        t.setDaemon(True)
        t.start()
        self.root.mainloop()

    # 处理服务器转发过来的好友消息
    def udp_recv_msg(self,port):
        while True:
            s = socket(AF_INET,SOCK_DGRAM)
            s.bind(('0.0.0.0',port))
            msg,addr = s.recvfrom(1024*512)
            self.handle_recv_msg(msg.decode())
    
    # 将消息显示到窗口上
    def handle_recv_msg(self,msg):
        content = json.loads(msg)
        self.send_frame.show_friend_msg(self.friend_nickname,content['send_time'],content['content'])


class MsgFrame(Frame):
    def __init__(self,root,myid,mynickname,friend_id,friend_nickname):
        super().__init__(root,bg='#2E3138')
        self.myid= myid
        self.mynickname = mynickname
        self.friend_id = friend_id
        self.friend_nickname = friend_nickname
        self.pack(fill=BOTH,expand=True)
        self.createForm()
        self.bind_event()

    def createForm(self):
        self.canvas=Canvas(self,width=600)
        self.frame1=Frame(self.canvas,bg='#2E3138')
        myscrollbar=Scrollbar(self,orient="vertical",command=self.canvas.yview,
        bg='#2E3138',activebackground='#2E3138',background='#2E3138',
        troughcolor='#6A7788',width=16,relief=FLAT)
        self.canvas.configure(yscrollcommand=myscrollbar.set,highlightthickness=0)

        myscrollbar.pack(side="right",fill=BOTH)
        self.canvas.config(background='#2E3138')
        self.canvas.pack(side="left",fill=BOTH)
        self.canvas.create_window((10,0),window=self.frame1,anchor='nw')

        # self.show_record_frame = Frame(self.frame1,bg='#2E3138')
        self.show_record_label = Label(self.frame1,text='查看以前的消息',bg='#2E3138',fg='#9CD0B1',
        font=('',10))
        self.show_record_label.pack(padx=230)
        # self.show_record_frame.pack()

    def bind_event(self):
        self.frame1.bind('<Enter>',self.frame1_enter)
        self.show_record_label.bind('<Enter>',self.enter_show_record_label)
        self.show_record_label.bind('<Button-1>',self.btn_show_record_label)

    def enter_show_record_label(self,event):
        self.show_record_label['cursor'] = 'fleur'

    def btn_show_record_label(self,event):
        self.get_all_msg()
    
    # 获取所有聊天记录
    def get_all_msg(self):
        msg = 'getMsg\n%s,%s'%(self.myid,self.friend_id)
        response = send_request(msg)
        if response == 'No_record':
            self.show_record_label['text'] = '没有更多消息'
        else:
            self.show_record_label.destroy()
            msgs = json.loads(response)
            for msg in msgs:
                if msg['from_id'] == int(self.myid):
                    self.show_me_msg(self.mynickname,msg['send_time'],msg['content'])
                if msg['from_id'] == int(self.friend_id):
                    self.show_friend_msg(self.friend_nickname,msg['send_time'],msg['content'])

    # 显示我发送的消息到界面
    def show_me_msg(self,mynickname,send_time,text):
        head = mynickname+':'+ send_time
        space_len1 = 125 - len(head.encode())
        space_len2 = 125 - len(text.encode())
        self.msg1 = Frame(self.frame1,bg='#2E3138')
        Label(self.msg1,text=' '*space_len1+head,bg='#2E3138',fg='#519ABA').grid(row=0,column=0,stick=E)
        Label(self.msg1,text=' '*space_len2+text,bg='#2E3138',fg='#FBFFFF').grid(row=1,column=0,stick=E)
        self.msg1.pack()

    def frame1_enter(self,event):
        # 根据内容改变滚动条
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # 显示朋友发送的消息到界面
    def show_friend_msg(self,friendnickname,send_time,text):
        head = friendnickname+':'+ send_time
        space_len1 = 125 - len(head.encode())
        space_len2 = 125 - len(text.encode())
        self.msg1 = Frame(self.frame1,bg='#2E3138')
        Label(self.msg1,text=head+' '*space_len1,bg='#2E3138',fg='#519ABA').grid(row=0,column=0,stick=W)
        Label(self.msg1,text=text+' '*space_len2,bg='#2E3138',fg='#FBFFFF').grid(row=1,column=0,stick=W)
        self.msg1.pack()
    


class SendFrame(Frame):
    def __init__(self,root,msg_frame1,msg_frame_canvas,myid,mynickname,friend_id,friend_nickname):
        super().__init__(root,bg='#2E3138')
        self.myid = myid
        self.mynickname = mynickname
        self.friend_id = friend_id
        self.friend_nickname = friend_nickname
        self.root = root
        self.msg_frame1 = msg_frame1
        self.msg_frame_canvas = msg_frame_canvas
        self.createForm()
    
    def createForm(self):
        f = Frame(self.root).pack()
        self.text = Text(self.root,bg='#2E3138',fg='#FBFFFF',height=4,bd=0,selectbackground='#6A7788',
        width=600)
        self.text.pack(ipady=20)
        self.button = Button(self.root,text='发  送',bg='#2E3138',fg='#FBFFFF',relief=FLAT,bd=0,
        activebackground='#2E3138',activeforeground='#FBFFFF',command=self.send)
        self.button.pack()

    # 发送消息主要方法
    def send(self):
        # 获取text中的内容
        text = self.text.get('0.0',END)
        # 按照指定格式获取时间
        send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dic = {
            'myid':self.myid,
            'mynickname':self.mynickname,
            'friend_id':self.friend_id,
            'content':text,
            'send_time':send_time
        }
        # 封装json串
        jsonstr = json.dumps(dic)
        msg = 'sendMsg\n%s'%(jsonstr)
        # 发送请求
        response = send_request(msg)
        if response == 'update_True':
            self.show_me_msg(self.mynickname,send_time,text)

    # 显示发送信息到界面
    def show_me_msg(self,mynickname,send_time,text):
        head = mynickname+':'+ send_time
        space_len1 = 125 - len(head.encode())
        space_len2 = 125 - len(text.encode())
        self.msg1 = Frame(self.msg_frame1,bg='#2E3138')
        Label(self.msg1,text=' '*space_len1+head,bg='#2E3138',fg='#519ABA').grid(row=0,column=0)
        Label(self.msg1,text=' '*space_len2+text,bg='#2E3138',fg='#FBFFFF').grid(row=1,column=0)
        self.msg1.pack()
        # 根据内容改变滚动条
        self.msg_frame_canvas.configure(scrollregion=self.msg_frame_canvas.bbox("all"))
    
    def show_friend_msg(self,friend_nickname,send_time,text):
        friend_nickname = friend_nickname.strip()
        send_time = send_time.strip()
        text = text.strip()
        head = friend_nickname+':'+ send_time
        space_len1 = 125 - len(head.encode())
        space_len2 = 125 - len(text.encode())
        self.msg1 = Frame(self.msg_frame1,bg='#2E3138')
        Label(self.msg1,text=head+' '*space_len1,bg='#2E3138',fg='#519ABA').grid(row=0,column=0,stick=W)
        Label(self.msg1,text=text+' '*space_len2,bg='#2E3138',fg='#FBFFFF').grid(row=1,column=0,stick=W)
        self.msg1.pack()
        # 根据内容改变滚动条
        self.msg_frame_canvas.configure(scrollregion=self.msg_frame_canvas.bbox("all"))

if __name__ == '__main__':
    SendMsgPage(1,'wo',3,'ta')