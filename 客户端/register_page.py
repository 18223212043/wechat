
from tkinter import *
from tkinter.messagebox import *
from tcpClient import *
from login_page import *

class RegisterPage(Frame):
    def __init__(self):
        super().__init__()
        self.username = StringVar()
        self.password = StringVar()
        self.password2 = StringVar()
        self.pack()
        self.createForm()
    
    def createForm(self):
        Label(self).grid(row = 0,stick = W,pady = 10)
        Label(self,text = "用户名：").grid(row=1,stick=W,pady = 10)
        Entry(self,textvariable = self.username).grid(row = 1,column = 1,stick = E)
        Label(self,text = "密　　码：").grid(row=2,stick=W,pady = 10)
        Entry(self,textvariable = self.password,show = "*").grid(row = 2,column = 1,stick = E)
        Label(self,text = "确认密码：").grid(row=3,stick=W,pady = 10)
        Entry(self,textvariable = self.password2,show = "*").grid(row = 3,column = 1,stick = E)
        Button(self,text = "注　　册",command = self.register).grid(row = 4,stick = W,pady=10)
        Button(self,text = "退　　出",command = self.quit).grid(row = 4,column=1,stick = E)
    
    def register(self):
        name = self.username.get()
        password = self.password.get()
        password2 = self.password2.get()
        if password == password2:
            msg = "register\n%s,None,%s"%(name,password)
            response = send_request(msg)
            if response == "register_True":
                self.destroy()
                root.title('登录界面')
                LoginPage(root).createForm()
            else:
                showinfo(title = "提示",message = "注册失败！！！")
        else:
            showinfo(title = "提示",message = "两次密码输入不一致！！！")


root = Tk()
root.title("注册界面")
width = 300
height = 300
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = "%dx%d+%d+%d"%(width,height,(screenwidth-width)/2,(screenheight-height)/2)
root.geometry(alignstr)

RegisterPage()
root.mainloop()