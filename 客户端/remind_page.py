
from tkinter import *
from send_msg_page import *
from tkinter.messagebox import *

class MsgRemindPage():
    def __init__(self,myid,mynickname,friend_id,friend_nickname):
        self.myid = myid
        self.mynickname = mynickname
        self.friend_id = friend_id
        self.friend_nickname = friend_nickname
        self.initForm()
        self.createFrame()
        self.bind_event()
        self.root.mainloop()

    def initForm(self):
        self.root = Tk()
        self.root.title("")
        width = 200
        height = 100
        self.root.maxsize(200,100)
        self.root.minsize(200,100)
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d"%(width,height,(screenwidth-width-20),(screenheight-height-60))
        self.root.geometry(alignstr)
        self.root['bg'] = '#FBFFFF'
    
    def createFrame(self):
        self.remind = Label(self.root,text='您有一条新消息',bg='#FBFFFF',fg='#F92434')
        self.remind.pack(pady=30)
        

    def bind_event(self):
        self.remind.bind_all('<Enter>',self.enter_remind)
        self.remind.bind_all('<Button-1>',self.btn_remind)

    def btn_remind(self,event):
        self.root.destroy()
        SendMsgPage(self.myid,self.mynickname,self.friend_id,self.friend_nickname)

    def enter_remind(self,event):
        self.remind['cursor'] = 'fleur' 

class AddRemindPage():
    def __init__(self,myid,mynickname,add_id,add_nickname,record_id):
        self.myid = myid
        self.mynickname = mynickname
        self.add_id = add_id
        self.add_nickname = add_nickname
        self.record_id = record_id
        self.initForm()
        self.createFrame()
        self.bind_event()
        self.root.mainloop()

    def initForm(self):
        self.root = Tk()
        self.root.title("")
        width = 200
        height = 100
        self.root.maxsize(200,100)
        self.root.minsize(200,100)
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d"%(width,height,(screenwidth-width-20),(screenheight-height-60))
        self.root.geometry(alignstr)
        self.root['bg'] = '#FBFFFF'
    
    def createFrame(self):
        self.remind = Label(self.root,text=self.add_nickname+'  请求添加您为好友',bg='#FBFFFF',fg='#F92434')
        self.remind.grid(row=0,columnspan=2,pady=30,padx=40)
        self.button1 = Label(self.root,text = '接受',bg='white',fg='#51B2F7')
        self.button1.grid(row=1,column=0)
        self.button2 = Label(self.root,text = '拒绝',bg='white',fg='#51B2F7')
        self.button2.grid(row=1,column=1)
        

    def bind_event(self):
        self.button1.bind('<Enter>',lambda Event,func=self.enter_remind,f=self.button1:func(Event,f))
        self.button2.bind('<Enter>',lambda Event,func=self.enter_remind,f=self.button2:func(Event,f))
        self.button1.bind('<Button-1>',self.btn_accept)
        self.button2.bind('<Button-1>',self.btn_refuse)

    def btn_accept(self,event):
        self.root.destroy()
        msg = 'acceptAdd\n%s,%s,%s'%(self.record_id,self.myid,self.add_id)
        response = send_request(msg)
        if response == 'update_True':
            # 添加成功则将好友放入初始分组
            pass
        else:
            # 失败则提示添加好友失败
            showinfo(title='',message='添加好友失败')
    
    def btn_refuse(self,event):
        self.root.destroy()
        msg = 'refuseAdd\n%s,%s,%s,%s'%(self.record_id,self.myid,self.mynickname,self.add_id)
        send_request(msg)

    def enter_remind(self,event,f):
        f['cursor'] = 'fleur' 

if __name__ == '__main__':
    AddRemindPage(1,3,'wo')