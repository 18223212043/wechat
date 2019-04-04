from tkinter import *
from tcpClient import *
from tkinter.messagebox import *
from main_page import *
from register_page import *
import os,random

USER_INFO = {}

class LoginPage(Frame):
    def __init__(self,root):
        super().__init__(bg='#F7F7F7')
        self.username = StringVar()
        self.password = StringVar()
        self.root = root
        self.pack()
        self.createForm()
        self.bind_event()
        self.root.mainloop()

    def createForm(self):
        # 提示信息标签
        self.label1 = Label(self,font=('',10),bg='#F7F7F7',fg='#FF0000')
        self.label1.grid(row = 0,column=1)
        # 用户名标签
        self.label2 = Label(self,text = "用户名：",font=('',10),bg='#F7F7F7')
        self.label2.grid(row=1,pady = 12)
        # 用户名输入框
        self.entry1 = Entry(self,textvariable = self.username,font=('',10))
        self.entry1.grid(row = 1,column = 1,ipady=4)
        # 密码标签
        self.label3 = Label(self,text = "密  码：",font=('',10),bg='#F7F7F7')
        self.label3.grid(row=2,pady = 12)
        #　密码输入框
        self.entry2 = Entry(self,textvariable = self.password,show = "*",font=('',10))
        self.entry2.grid(row = 2,column = 1,ipady=4)
        # 登录按钮
        self.button1 = Button(self,text = "登　　录",command = self.login,state=DISABLED,
        font=('',10),bg='#04BE01',fg = 'white',activebackground='#04BE01',
        activeforeground='white')
        self.button1.grid(row = 3,columnspan=2,ipadx=102,pady=12)
        # 去注册标签
        self.label4 = Label(self,text='没有帐号？去注册',fg='#37373D',bg='#F7F7F7')
        self.label4.grid(row=4,columnspan=2,stick=W)

    def bind_event(self):
        # 输入框鼠标移出事件
        self.entry1.bind('<Leave>',self.check_input)
        self.entry2.bind('<Leave>',self.check_input)
        # 鼠标移入移出改变注册帐号字体颜色
        self.label4.bind('<Enter>',self.change_label4_fg)
        self.label4.bind('<Leave>',self.restore_label4_fg)
        # 鼠标按下注册帐号事件
        self.label4.bind('<Button-1>',self.to_register)

    def to_register(self,event):
        self.forget()
        self.root.title('注　　册')
        width = 380
        height = 480
        self.root.maxsize(width,height)
        self.root.minsize(width,height)
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d"%(width,height,(screenwidth-width)/2,(screenheight-height)/2)
        self.root.geometry(alignstr)
        RegisterPage(self.root)

    def change_label4_fg(self,event):
        self.label4['fg'] = '#04BE01'

    def restore_label4_fg(self,event):
        self.label4['fg'] = '#37373D'

    # 检查输入框中是否都有输入
    def check_input(self,event):
        if self.username.get().strip() and self.password.get().strip():
            self.button1['state'] = NORMAL

    # 处理登录
    def login(self):
        username = self.username.get()
        password = self.password.get()
        port = random.randint(10000,60000)
        msg = 'login\n%s,%s,%d'%(username,password,port)
        response = send_request(msg)
        response_arr = response.split('\n')
        response_header = response_arr[0]
        if response_header == 'login_True':
            response_info = response_arr[1].split(',')
            global USER_INFO
            USER_INFO['id'] = response_info[0]
            USER_INFO['username'] = response_info[1]
            USER_INFO['sex'] = response_info[2]
            USER_INFO['nickname'] = response_info[3]
            if response_info[4] == 'null':
                response_info[4] = '什么都没有留下'
            USER_INFO['signature'] = response_info[4]
            self.root.destroy()
            MainPage(USER_INFO,port)
        elif response_header == 'user_Error':
            self.label1['text'] = '用户名或密码错误!!!'
    
   
        
            

def main():
    root = Tk()
    root.title("登　　录")
    width = 430
    height = 350
    root.maxsize(width,height)
    root.minsize(width,height)
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = "%dx%d+%d+%d"%(width,height,(screenwidth-width)/2,(screenheight-height)/2)
    root.geometry(alignstr)
    root['bg'] = '#F7F7F7'

    top_frame = Frame(bg='#04BE01')
    top_frame.pack(padx=0,pady=0,fill=BOTH)
    Label(top_frame,text='WeChat',font=('',20),fg='white',bg='#04BE01').pack(pady=50)

    LoginPage(root)
            
if __name__ == '__main__':
    main()