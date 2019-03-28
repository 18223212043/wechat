from tkinter import *


class LoginPage(Frame):
    def __init__(self,root):
        super().__init__()
        self.username = StringVar()
        self.password = StringVar()
        self.pack()
        self.root = root

    def createForm(self):
        Label(self).grid(row = 0,stick = W,pady = 10)
        Label(self,text = "用户名：").grid(row=1,stick=W,pady = 10)
        Entry(self,textvariable = self.username).grid(row = 1,column = 1,stick = E)
        Label(self,text = "密  码：").grid(row=2,stick=W,pady = 10)
        Entry(self,textvariable = self.password,show = "*").grid(row = 2,column = 1,stick = E)
        Button(self,text = "登　　录",command = self.login).grid(row = 3,stick = W,pady=10)
        Button(self,text = "退　　出",command = self.quit).grid(row = 3,column=1,stick = E)

    def login(self):
        name = self.username.get()
        password = self.password.get()
        if name == password:
            self.root.destroy()
            