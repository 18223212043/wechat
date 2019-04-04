
from tkinter import *
from tcpClient import *
from login_page import *

class RegisterPage(Frame):
    def __init__(self,root):
        super().__init__(bg='#F7F7F7')
        self.username = StringVar()
        self.password = StringVar()
        self.password2 = StringVar()
        self.sex = IntVar()
        self.nickname = StringVar()
        self.pack(padx=30,expand=True,fill=BOTH)
        self.createForm()
        self.bind_event()
        self.root = root
    
    # 初始化Form
    def createForm(self):
        #提示信息标签
        self.label1 = Label(self,font=('',10),bg='#F7F7F7',fg='#FF0000')
        self.label1.grid(row = 0,column=1)
        # 用户名标签
        self.label2 = Label(self,text = "用  户  名：",bg='#F7F7F7',font=('',10))
        self.label2.grid(row=1,padx=20,pady = 12)
        # 用户名输入框
        self.entry1 = Entry(self,textvariable = self.username,
        font=('',10))
        self.entry1.grid(row = 1,column = 1,padx=30,ipady=4)
        # 密码标签
        self.label3 = Label(self,text = "密　　码：",bg='#F7F7F7',font=('',10))
        self.label3.grid(row=2,pady = 12)
        # 密码输入框
        self.entry2 = Entry(self,textvariable = self.password,show = "*",font=('',10))
        self.entry2.grid(row = 2,column = 1,ipady=4)
        # 确认密码标签
        self.label4 = Label(self,text = "确认密码：",bg='#F7F7F7',font=('',10))
        self.label4.grid(row=3,pady = 12)
        # 确认密码输入框
        self.entry3 = Entry(self,textvariable = self.password2,show = "*",font=('',10))
        self.entry3.grid(row = 3,column = 1,ipady=4)
        # 性别标签
        self.label5 = Label(self,text = "性　　别：",bg='#F7F7F7',font=('',10))
        self.label5.grid(row=4,pady = 12)
        # 性别选择框
        self.radio1 = Radiobutton(self,text='男',variable=self.sex,value=1,bg='#F7F7F7')
        self.radio1.grid(row = 4,column = 1,ipady=4,stick=W,padx=30)
        self.radio2 = Radiobutton(self,text='女',variable=self.sex,value=2,bg='#F7F7F7')
        self.radio2.grid(row = 4,column = 1,ipady=4)
        # 昵称标签
        self.label6 = Label(self,text = "昵　　称：",bg='#F7F7F7',font=('',10))
        self.label6.grid(row=5,pady = 12)
        # 昵称输入框
        self.entry5 = Entry(self,textvariable = self.nickname,font=('',10))
        self.entry5.grid(row = 5,column = 1,ipady=4)
        # 注册按钮
        self.button1 = Button(self,text = "注　　册",command = self.register,font=('',10),
        bg = '#04BE01',fg='white',state=DISABLED,relief=FLAT,activebackground='#04BE01',
        activeforeground='white')
        self.button1.grid(row = 6,columnspan=2,stick=W,ipadx=102,pady=12,padx=20)
    
    #绑定事件
    def bind_event(self):
        # 绑定所有输入框的鼠标移出事件，当所有输入框都有内容时允许点击按钮
        self.entry1.bind('<Leave>',self.check_input)
        self.entry2.bind('<Leave>',self.check_input)
        self.entry3.bind('<Leave>',self.check_input)
        self.entry5.bind('<Leave>',self.check_input)

    # 检查是否所有输入框都已输入，都输入则激活注册按钮
    def check_input(self,event):
        if self.username.get().strip() and self.password.get().strip()\
             and self.password2.get().strip() and self.sex.get()!=0\
                 and self.nickname.get().strip():
            self.button1['state'] = NORMAL

    def register(self):
        username = self.username.get()
        password = self.password.get()
        password2 = self.password2.get()
        sex = self.sex.get()
        nickname = self.nickname.get()
        if password == password2:
            msg = "register\n%s,%s,%d,%s"%(username,password,sex,nickname)
            response = send_request(msg)
            response_arr = response.split('\n')
            response_header = response_arr[0]
            if response_header == "register_True":
                self.destroy()
                self.root.title('登　　录')
                width = 430
                height = 350
                self.root.maxsize(width,height)
                self.root.minsize(width,height)
                screenwidth = self.root.winfo_screenwidth()
                screenheight = self.root.winfo_screenheight()
                alignstr = "%dx%d+%d+%d"%(width,height,(screenwidth-width)/2,(screenheight-height)/2)
                self.root.geometry(alignstr)
                LoginPage(self.root)
            elif response_header == 'username_Exist':
                self.label1['text'] = '用户名已存在！！！'
            elif response_header == 'register_False':
                self.label1['text'] = '网络错误！！！'
        else:
            self.label1['text'] = '两次密码输入不一致'
