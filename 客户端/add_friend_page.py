from tkinter import *
from tcpClient import *
import json
from tkinter.messagebox import *


class AddFriendPage():
    def __init__(self,userinfo):
        self.userinfo = userinfo
        self.init_form()
        self.createFrame()

    def init_form(self):
        self.root = Toplevel()
        self.root.title("添加好友")
        width = 400
        height = 300
        self.root.maxsize(400,300)
        self.root.minsize(400,300)
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d"%(width,height,(screenwidth-width)/2,(screenheight-height)/2)
        self.root.geometry(alignstr)
        self.root['bg'] = '#2E3138'


    def createFrame(self):
        SearchFrame(self.root,self.userinfo)
        self.root.mainloop()
        

class SearchFrame(Frame):
    def __init__(self,root,userinfo):
        super().__init__(root,bg='#2E3138')
        self.userinfo = userinfo
        self.search_content = StringVar()
        self.pack(pady=14)
        self.createForm(root)
        self.bind_event()

    def createForm(self,root):
        self.entry1 = Entry(self,textvariable=self.search_content,bg='#6A7788')
        self.entry1.pack(side=LEFT,ipadx=10,ipady=4)
        self.button1 = Button(self,text='查找好友',bg='#6A7788',fg='white',state=DISABLED,
        relief=FLAT,activebackground='#6A7788',activeforeground='white',
        command=lambda func=self.search,root=root:func(root))
        self.button1.pack(padx=20,ipadx=10)
        # 利用Frame画一条分割线
        Frame(root,bg='#26292E').pack(ipady=1,fill='x')

    def bind_event(self):
        self.entry1.bind('<KeyRelease>',self.check_content)

    def check_content(self,event):
        if self.search_content.get().strip():
            self.button1['state'] = NORMAL

    def search(self,root):
        if self.search_content.get().strip():
            SearchResultFrame(root,self.search_content,self.userinfo)


class SearchResultFrame(Frame):
    def __init__(self,root,search_content,userinfo):
        super().__init__(root)
        self.search_content = search_content
        self.userinfo = userinfo
        self.pack()
        self.createForm()
        self.bind_event()

    def createForm(self):
        # 查找结果界面
        self.canvas=Canvas(self,width=400)
        self.frame1=Frame(self.canvas,bg='#2E3138')
        myscrollbar=Scrollbar(self,orient="vertical",command=self.canvas.yview,
        bg='#2E3138',activebackground='#2E3138',background='#2E3138',
        troughcolor='#6A7788',width=16,relief=FLAT)
        self.canvas.configure(yscrollcommand=myscrollbar.set,highlightthickness=0)

        myscrollbar.pack(side="right",fill=BOTH)
        self.canvas.config(background='#2E3138')
        self.canvas.pack(side="left",fill=BOTH)
        self.canvas.create_window((0,0),window=self.frame1,anchor='nw',width=600)
        self.get_result_data()
    
    def bind_event(self):
        self.frame1.bind("<Enter>",self.myfunction)

    # 根据内容改变滚动条
    def myfunction(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # 得到返回的数据并显示
    def get_result_data(self):
        msg = 'searchUser\n%s'%self.search_content.get()
        response = send_request(msg)
        if response == 'No_Result':
            f = Frame(self.frame1,bg='#2E3138')
            label1 = Label(f,text='没有搜索到相关信息',bg='#2E3138',fg='#37373D',font=('',10))
            label1.grid(ipady=8,padx=30)
            f.pack(fill=BOTH)
        else:
            users = json.loads(response)
            # 创建字典，绑定分组Frame和它的控件
            self.search_result_frame = {}
            for user in users:
                user_label = []
                f = Frame(self.frame1,bg='#2E3138')
                label1 = Label(f,text=user['nickname']+'('+user['username']+')',
                bg='#2E3138',fg='white',font=('',10))
                label1.grid(stick=W,ipady=8,padx=10)
                label2 = Label(f,text='+',bg='#2E3138',fg='white',font=('',12))
                label2.grid(row=0,column=1,stick=E)

                # 鼠标移入
                f.bind('<Enter>',lambda Event,func=self.enter_frame,f=f:func(Event,f))
                label2.bind('<Enter>',lambda Event,func=self.enter_add,f=label2:func(Event,f))
                # 鼠标移出
                f.bind('<Leave>',lambda Event,func=self.leave_frame,f=f:func(Event,f))
                # 点击加号触发事件
                label2.bind('<Button-1>',lambda Event,func=self.btn_add,f=f:func(Event,f))
                f.pack(fill=BOTH)

                # 将子控件放入列表
                user_label.append(label1)
                user_label.append(label2)
                # 将此frame的信息放入列表
                user_label.append(user['id'])
                user_label.append(user['nickname'])

                self.search_result_frame[f] = user_label
    

    # frame鼠标移出事件
    def leave_frame(self,event,f):
        f['bg'] = '#2E3138'
        for f_child in self.search_result_frame[f][0:2]:
             f_child['bg'] = '#2E3138'

    # frame鼠标移入事件
    def enter_frame(self,event,f):
        f['bg'] = '#6A7788'
        for f_child in self.search_result_frame[f][0:2]:
             f_child['bg'] = '#6A7788'
             
    # 加号鼠标移入事件
    def enter_add(self,event,f):
        f['bg'] = '#6A7788'
        f['cursor'] = 'fleur'

    # 创建子窗体提示确认是否添加
    def btn_add(self,event,f):
        nickname_len = len(self.search_result_frame[f][3].encode())
        self.add_confirm = Toplevel()
        self.add_confirm.title("")
        width = 200 + nickname_len - 3
        height = 200 + nickname_len -3
        self.add_confirm.maxsize(width,height)
        self.add_confirm.minsize(width,height)
        screenwidth = self.add_confirm.winfo_screenwidth()
        screenheight = self.add_confirm.winfo_screenheight()
        alignstr = "%dx%d+%d+%d"%(width,height,(screenwidth-width)/2,(screenheight-height)/2)
        self.add_confirm.geometry(alignstr)
        self.add_confirm['bg'] = '#2E3138'
        # 文字label
        Label(self.add_confirm,bg='#2E3138').grid(row=0,column=0,padx=18,pady=height//5)
        Label(self.add_confirm,text='是否添加',bg='#2E3138',fg='#FBFFFF').grid(row=0,column=1,stick=E)
        Label(self.add_confirm,text=self.search_result_frame[f][3],bg='#2E3138',
        fg='#F15A24').grid(row=0,column=2,stick=W)
        Label(self.add_confirm,text='为好友?',bg='#2E3138',fg='#FBFFFF').grid(row=0,column=3)
        # 按钮选项
        Button(self.add_confirm,text='确定',bg='#2E3138',fg='#FBFFFF',command=lambda func=self.ensure,f=f:func(f),
        relief=FLAT).grid(row=1,column=0,columnspan=2,stick=E)
        Button(self.add_confirm,text='取消',bg='#2E3138',fg='#FBFFFF',command=self.add_confirm_quit,
        relief=FLAT).grid(row=1,column=2,columnspan=2)
        self.add_confirm.mainloop()
    
    def ensure(self,f):
        myid = self.userinfo['id']
        add_id = self.search_result_frame[f][2]
        mynickname = self.userinfo['nickname']
        msg = 'addFriend\n%s,%s,%s'%(myid,add_id,mynickname)
        response = send_request(msg)
        if response == 'update_True':
            self.add_confirm.destroy()
            showinfo(title='',message='好友请求已发送')
        if response == 'friend_Exsit':
            self.add_confirm.destroy()
            showinfo(title='',message='该用户已是您的好友')
            
    
    def add_confirm_quit(self):
        self.add_confirm.destroy()



if __name__ == '__main__':
    AddFriendPage()