from tkinter import *
from PIL import Image as pilImage,ImageTk
import os,sys
from add_friend_page import AddFriendPage
from tcpClient import *
from send_msg_page import *
from socket import *
from select import select
from remind_page import *
from threading import Thread

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class MainPage():
    def __init__(self,userinfo,port):
        self.userinfo = userinfo
        self.port = port
        self.init_form()
        self.createFrame()

    def init_form(self):
        self.root = Tk()
        self.root.title("wechat")
        width = 300
        height = 600
        self.root.maxsize(388,1000)
        self.root.minsize(300,300)
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d"%(width,height,(screenwidth-width-80),(screenheight-height)/2)
        self.root.geometry(alignstr)
        self.root['bg'] = '#2E3138'

    def createFrame(self):
        self.frame_top = FrameTop(self.userinfo)
        self.frame_main = FrameMain(self.userinfo,self.root)
        self.frame_bottom = FrameBottom(self.frame_main.frame1,self.userinfo)
        t = Thread(target=self.udp_recv,args=(self.port,))
        t.setDaemon(True)
        t.start()
        self.root.mainloop()
        sys.exit()

    # udp接收传送过来的信息
    def udp_recv(self,port):
        while True:
            s = socket(AF_INET,SOCK_DGRAM)
            s.bind(('0.0.0.0',port))
            msg,addr = s.recvfrom(1024*512)
            t = Thread(target=self.handle_recv,args=(msg.decode(),))
            t.start()
            t.join()

    # 具体处理发送过来的消息
    def handle_recv(self,msg):
        # 解析json字符串
        request_msg = json.loads(msg)
        # 添加消息
        if request_msg['header'] == 'add':
            AddRemindPage(self.userinfo['id'],self.userinfo['nickname'],request_msg['add_id']
            ,request_msg['add_nickname'],request_msg['record_id'])
        # 添加成功
        if request_msg['header'] == 'add_success':
            for frame,value in self.frame_main.group_frame.items():
                if int(value[3][0]) == request_msg['group_id']:
                    friend_id = request_msg['friend_id']
                    friend_username = request_msg['friend_username']
                    friend_nickname = request_msg['friend_nickname']
                    friend_signature = request_msg['friend_signature']
                    f = self.frame_main.create_friend_frame(friend_username,friend_nickname,friend_signature,frame)
                    f.forget()
                    self.frame_main.group_frame[frame][4][f] = [friend_id,friend_nickname]
                    group_info = self.frame_main.group_frame[frame][3]
                    group_info[2] = int(group_info[2]) + 1
                    group_info[3] = int(group_info[3]) + 1
                    self.frame_main.group_frame[frame][2]['text'] = str(group_info[2])+'/'+str(group_info[3])
        # 添加失败
        if request_msg['header'] == 'add_failed':
            showinfo(title='',message=request_msg['refuse_nickname']+'拒绝添加您为好友')
    


class FrameTop(Frame):
    def __init__(self,userinfo):
        self.userinfo = userinfo
        self.nickname = StringVar(value=self.userinfo['nickname'])
        self.signature = StringVar(value=self.userinfo['signature'])
        super().__init__(bg='#2E3138')
        self.pack(fill=BOTH)
        self.createForm()
        self.bind_event()

    def createForm(self):
        # 得到图片地址并解析图片
        self.ph = get_image(50,50,'images/1.jpg')
        # 放头像的label
        self.label1 = Label(self,image=self.ph)
        self.label1.grid(rowspan=3,column=0,padx=20,pady=20)
        # 昵称标签
        self.label2 = Label(self,text=self.userinfo['nickname'],bg='#2E3138',fg='#F7F7F7')
        self.label2.grid(row=0,column=1,pady=12,stick=W)
        # 个性签名标签
        self.label3 = Label(self,text=self.userinfo['signature'],bg='#2E3138',fg='#F7F7F7')
        self.label3.grid(row=1,column=1,stick=W)
        # 利用Frame画一条分割线
        Frame(bg='#26292E').pack(ipady=1,fill='x')

    def bind_event(self):
        # 鼠标移入事件
        self.label2.bind('<Enter>',lambda Event,func=self.enter_label,f=self.label2:func(Event,f))
        self.label3.bind('<Enter>',lambda Event,func=self.enter_label,f=self.label3:func(Event,f))
        # 鼠标双击事件
        self.label2.bind('<Double-Button-1>',lambda Event,func=self.double_button_label2,f=self.label2:func(Event,f))
        self.label3.bind('<Double-Button-1>',lambda Event,func=self.double_button_label3,f=self.label3:func(Event,f))

    # 双击昵称label触发的事件
    def double_button_label３(self,event,f):
        f.forget()
        entry = Entry(self,textvariable=self.signature,
        bg='#2E3138',fg='#F7F7F7')
        entry.grid(row=1,column=1,stick=W)
        entry.bind('<Return>',lambda Event,func=self.return_signature_entry,f=entry:func(Event,f))
    
    # 在修改昵称输入框中按下回车键触发的事件
    def return_signature_entry(self,event,f):
        signature = self.signature.get()
        msg = 'updateSignature\n%s,%s'%(self.userinfo['id'],signature)
        response = send_request(msg)
        response_arr = response.split('\n')
        response_header = response_arr[0]
        f.destroy()
        self.label3.grid(row=1,column=1,stick=W)
        if response_header == 'update_True':
            self.label3['text'] = signature
        else:
            self.label3['text'] = self.userinfo['signature']

    # 双击昵称label触发的事件
    def double_button_label2(self,event,f):
        f.forget()
        entry = Entry(self,textvariable=self.nickname,
        bg='#2E3138',fg='#F7F7F7')
        entry.grid(row=0,column=1,pady=12,stick=W)
        entry.bind('<Return>',lambda Event,func=self.return_nickname_entry,f=entry:func(Event,f))
    
    # 在修改昵称输入框中按下回车键触发的事件
    def return_nickname_entry(self,event,f):
        nickname = self.nickname.get()
        msg = 'updateNickname\n%s,%s'%(self.userinfo['id'],nickname)
        response = send_request(msg)
        response_arr = response.split('\n')
        response_header = response_arr[0]
        f.destroy()
        self.label2.grid(row=0,column=1,pady=12,stick=W)
        if response_header == 'update_True':
            self.label2['text'] = nickname
        else:
            self.label2['text'] = self.userinfo['nickname']

    def enter_label(self,event,f):
        f['cursor'] = 'fleur'

class FrameMain(Frame):
    def __init__(self,userinfo,root):
        super().__init__(bg='#2E3138')
        self.userinfo = userinfo
        self.friend_img = get_image(30,30,'images/1.jpg')
        # 创建字典保存打开的发送消息的窗口
        self.send_msg_frame = {}
        self.root = root
        self.pack(fill=BOTH,expand=True)
        # 初始化Frame
        self.createForm()
        # 初始化绑定事件函数
        self.bind_event()
        # 初始化右键点击弹出的操作框
        self.selection = None

    def createForm(self):
        self.get_friendlist_form()
        # 利用Frame画一条分割线
        Frame(bg='#26292E').pack(ipady=1,fill='x')

    def bind_event(self):
        self.frame1.bind("<Enter>",self.myfunction)
        # 添加鼠标滚轮滑动事件
        self.canvas.bind('<MouseWheel>',self.on_mouseWheel) 
        
        for f in self.group_frame.keys():
            # 分组列表鼠标左键点击事件
            f.bind('<Button-1>',lambda Event,func=self.group_mouseLeft_press,f=f:func(Event,f))
            # 分组列表鼠标右键点击事件
            f.bind('<Button-3>',lambda Event,func=self.group_mouseRight_press,f=f:func(Event,f))
            # 为分组列表Frame中的每个控件添加右键点击事件
            for f_child in self.group_frame[f][1:3]:
                f_child.bind('<Button-1>',lambda Event,func=self.group_child_mouseLeft_press,f=f:func(Event,f))
                f_child.bind('<Button-3>',lambda Event,func=self.group_child_mouseRight_press,f=f,f_child=f_child:func(Event,f,f_child))
            # 分组列表鼠标移入事件
            f.bind('<Enter>',lambda Event,func=self.group_mouseEnter,f=f:func(Event,f))
            #　分组列表鼠标移出事件
            f.bind('<Leave>',lambda Event,func=self.group_mouseLeave,f=f:func(Event,f))

     # 分组列表子控件鼠标左键点击事件
    def group_child_mouseLeft_press(self,event,f):
        if not self.group_frame[f][0]:
            f['bg']='#6A7788'
            for lab in self.group_frame[f][1:3]:
                lab['bg'] = '#6A7788'
            self.group_frame[f][0] = True
            # 显示点击分组中的好友的方法
            # 判断是否已经请求过，等于5说明好友信息已经保存,否则就像服务端请求该分组的好友数据
            if self.group_frame[f][4]:
                for fri_fra in self.group_frame[f][4]:
                    fri_fra.pack(after=f,fill=BOTH,anchor='w')
            if self.group_frame[f][5]:
                for fri_fra in self.group_frame[f][5]:
                    fri_fra.pack(after=f,fill=BOTH,anchor='w')
            else:
                # 得到该分组的id
                group_id = self.group_frame[f][3][0]
                self.get_friend(group_id,f)
        else:
            f['bg']='#2E3138'
            for lab in self.group_frame[f][1:3]:
                lab['bg'] = '#2E3138'
            # 隐藏点击分组中的好友
            for fri_fra in self.group_frame[f][4]:
                fri_fra.forget()
            for fri_fra in self.group_frame[f][5]:
                fri_fra.forget()
            self.group_frame[f][0] = False
        if self.selection:
            self.selection.destroy()

    # 分组列表子控件鼠标右键点击事件
    def group_child_mouseRight_press(self,event,f,f_child):
        if self.selection:
            self.selection.destroy()
        selection_frame = Frame(self.root,bg='#FBFFFF')
        selection_frame.place(x=event.x+2,y=event.y-54,in_=f_child)
        # 添加分组Label
        add_group_lab = Label(selection_frame,text='添加分组',bg='#FBFFFF')
        add_group_lab.pack(ipadx=40,ipady=4,fill=BOTH)
        # 重命名label
        rename_group_lab = Label(selection_frame,text='重命名',bg='#FBFFFF')
        rename_group_lab.pack(ipadx=40,ipady=4,fill=BOTH)
        # 给label添加鼠标移入事件
        add_group_lab.bind('<Enter>',lambda Event,func=self.selection_mouse_Enter,
        f=add_group_lab:func(Event,f))
        rename_group_lab.bind('<Enter>',lambda Event,func=self.selection_mouse_Enter,
        f=rename_group_lab:func(Event,f))
        # 给label添加鼠标移出事件
        add_group_lab.bind('<Leave>',lambda Event,func=self.selection_mouse_Leave,
        f=add_group_lab:func(Event,f))
        rename_group_lab.bind('<Leave>',lambda Event,func=self.selection_mouse_Leave,
        f=rename_group_lab:func(Event,f))
        self.selection = selection_frame

    # 分组列表Frame鼠标右键点击事件
    def group_mouseRight_press(self,event,f):
        if self.selection:
            self.selection.destroy()
        selection_frame = Frame(self.root,bg='#FBFFFF')
        selection_frame.place(x=event.x+2,y=event.y-54,in_=f)
        # 添加分组Label
        add_group_lab = Label(selection_frame,text='添加分组',bg='#FBFFFF')
        add_group_lab.pack(ipadx=40,ipady=4,fill=BOTH)
        # 重命名label
        rename_group_lab = Label(selection_frame,text='重命名',bg='#FBFFFF')
        rename_group_lab.pack(ipadx=40,ipady=4,fill=BOTH)
        # 给label添加鼠标移入事件
        add_group_lab.bind('<Enter>',lambda Event,func=self.selection_mouse_Enter,
        f=add_group_lab:func(Event,f))
        rename_group_lab.bind('<Enter>',lambda Event,func=self.selection_mouse_Enter,
        f=rename_group_lab:func(Event,f))
        # 给label添加鼠标移出事件
        add_group_lab.bind('<Leave>',lambda Event,func=self.selection_mouse_Leave,
        f=add_group_lab:func(Event,f))
        rename_group_lab.bind('<Leave>',lambda Event,func=self.selection_mouse_Leave,
        f=rename_group_lab:func(Event,f))
        self.selection = selection_frame


    # 分组列表鼠标左键点击事件
    def group_mouseLeft_press(self,event,f):
        if not self.group_frame[f][0]:
            f['bg']='#6A7788'
            for lab in self.group_frame[f][1:3]:
                lab['bg'] = '#6A7788'
            self.group_frame[f][0] = True
            # 显示点击分组中的好友的方法
            # 判断是否已经请求过，等于5说明好友信息已经保存,否则就像服务端请求该分组的好友数据
            if self.group_frame[f][4]:
                for fri_fra in self.group_frame[f][4]:
                    fri_fra.pack(after=f,fill=BOTH,anchor='w')
            if self.group_frame[f][5]:
                for fri_fra in self.group_frame[f][5]:
                    fri_fra.pack(after=f,fill=BOTH,anchor='w')
            else:
                # 得到该分组的id
                group_id = self.group_frame[f][3][0]
                self.get_friend(group_id,f)
        else:
            f['bg']='#2E3138'
            for lab in self.group_frame[f][1:3]:
                lab['bg'] = '#2E3138'
            # 隐藏点击分组中的好友
            for fri_fra in self.group_frame[f][4]:
                fri_fra.forget()
            for fri_fra in self.group_frame[f][5]:
                fri_fra.forget()
            self.group_frame[f][0] = False
        if self.selection:
            self.selection.destroy()

    # 获取分组中的好友
    def get_friend(self,group_id,group_f):
        msg = 'getFriendByGroup\n%s'%group_id
        response = send_request(msg)
        response_arr = response.split('\n')
        # 初始化字典保存好友Frame
        friend_frame = {}
        for friend_info in response_arr[1:]:
            friend_info = friend_info.split(',')
            friend_id = friend_info[0]
            friend_username = friend_info[1]
            friend_nickname = friend_info[2]
            friend_signature = friend_info[3]
            f = self.create_friend_frame(friend_username,friend_nickname,friend_signature,group_f)
            # 将franme和好友id,nickname用字典绑定
            friend_frame[f] = [friend_id,friend_nickname]
        # 将好友frame保存在相对应分组的frame对象中
        self.group_frame[group_f][5] = friend_frame
        if self.selection:
            self.selection.destroy()
    
    def create_friend_frame(self,friend_username,friend_nickname,friend_signature,group_f):
        f = Frame(self.frame1,bg='#2E3138')
        # 好友头像lab
        img_lab = Label(f,bg='#2E3138',fg='#F7F7F7',image=self.friend_img)
        img_lab.grid(stick=W,rowspan=3,column=0,padx=10)
        nickname_lab = Label(f,text = friend_nickname+'('+friend_username+')',bg='#2E3138',fg='white',
        font=('',10))
        # 好友昵称lab
        nickname_lab.grid(row=0,column=1,stick=W,padx=10)
        sig_lab = Label(f,text = friend_signature,bg='#2E3138',fg='white',font=('',10)
        )
        # 好友签名lab
        sig_lab.grid(row=1,column=1,stick=W,padx=10)
        f.pack(after=group_f,fill=BOTH,anchor='w')
        # 给好友Frame添加鼠标移入事件
        f.bind('<Enter>',lambda Event,func=self.friend_frame_labEnter,f=f,img_lab=img_lab,
        nickname_lab = nickname_lab,sig_lab=sig_lab:func(Event,f,img_lab,nickname_lab,sig_lab))
        # 给好友Frame添加鼠标移出事件
        f.bind('<Leave>',lambda Event,func=self.friend_frame_labLeave,f=f,img_lab=img_lab,
        nickname_lab = nickname_lab,sig_lab=sig_lab:func(Event,f,img_lab,nickname_lab,sig_lab))
        # 给好友Frame添加鼠标右键点击事件,f_group代表此好友frame的分组frame,f_friend代表此好友frame
        f.bind('<Button-3>',lambda Event,func=self.friend_mouseRight_press,f_group=group_f,
        f_friend=f:func(Event,f_group,f_friend))
        # 给好友Frame的子控件添加鼠标右键点击事件,f_group代表此好友frame的分组frame,f_friend代表此好友frame,f_child代表此好友frame的子控件
        img_lab.bind('<Button-3>',lambda Event,func=self.friend_child_mouseRight_press,
        f_group=group_f,f_friend=f,f_child=img_lab:func(Event,f_group,f_friend,f_child))

        nickname_lab.bind('<Button-3>',lambda Event,func=self.friend_child_mouseRight_press,
        f_group=group_f,f_friend=f,f_child=nickname_lab:func(Event,f_group,f_friend,f_child))

        sig_lab.bind('<Button-3>',lambda Event,func=self.friend_child_mouseRight_press,
        f_group=group_f,f_friend=f,f_child=sig_lab:func(Event,f_group,f_friend,f_child))
        # 添加好友frame和其子控件的双击事件
        f.bind('<Double-Button-1>',lambda Event,func=self.open_send_page,f_group=group_f,
        f_friend=f:func(Event,f_group,f_friend))

        img_lab.bind('<Double-Button-1>',lambda Event,func=self.open_send_page,f_group=group_f,
        f_friend=f:func(Event,f_group,f_friend))

        nickname_lab.bind('<Double-Button-1>',lambda Event,func=self.open_send_page,f_group=group_f,
        f_friend=f:func(Event,f_group,f_friend))

        sig_lab.bind('<Double-Button-1>',lambda Event,func=self.open_send_page,f_group=group_f,
        f_friend=f:func(Event,f_group,f_friend))

        return f

    # 给好友Frame的子控件添加鼠标右键点击事件
    def friend_child_mouseRight_press(self,event,f_group,f_friend,f_child):
        if self.selection:
            self.selection.destroy()
        selection_frame = Frame(self.root,bg='#FBFFFF')
        selection_frame.place(x=event.x+2,y=event.y-54,in_=f_child)
        # 发送消息Label
        send_msg_lab = Label(selection_frame,text='发送消息',bg='#FBFFFF')
        send_msg_lab.pack(ipadx=40,ipady=4,fill=BOTH)
        # 查看资料label
        read_info_lab = Label(selection_frame,text='查看资料',bg='#FBFFFF')
        read_info_lab.pack(ipadx=40,ipady=4,fill=BOTH)
        # 给label添加鼠标移入事件
        send_msg_lab.bind('<Enter>',lambda Event,func=self.selection_mouse_Enter,
        f=send_msg_lab:func(Event,f))
        read_info_lab.bind('<Enter>',lambda Event,func=self.selection_mouse_Enter,
        f=read_info_lab:func(Event,f))
        # 给label添加鼠标移出事件
        send_msg_lab.bind('<Leave>',lambda Event,func=self.selection_mouse_Leave,
        f=send_msg_lab:func(Event,f))
        read_info_lab.bind('<Leave>',lambda Event,func=self.selection_mouse_Leave,
        f=read_info_lab:func(Event,f))
        # 给发送消息label添加鼠标左键单击事件,f_group代表分组frame,f_friend代表当前子控件的好友frame
        send_msg_lab.bind('<Button-1>',lambda Event,func=self.open_send_page,f_group=f_group,f_friend=f_friend
        :func(Event,f_group,f_friend))
        self.selection = selection_frame
    
    # 给好友Frame添加鼠标右键点击事件
    def friend_mouseRight_press(self,event,f_group,f_friend):
        if self.selection:
            self.selection.destroy()
        selection_frame = Frame(self.root,bg='#FBFFFF')
        selection_frame.place(x=event.x+2,y=event.y-54,in_=f_friend)
        # 发送消息Label
        send_msg_lab = Label(selection_frame,text='发送消息',bg='#FBFFFF')
        send_msg_lab.pack(ipadx=40,ipady=4,fill=BOTH)
        # 查看资料label
        read_info_lab = Label(selection_frame,text='查看资料',bg='#FBFFFF')
        read_info_lab.pack(ipadx=40,ipady=4,fill=BOTH)
        # 给label添加鼠标移入事件
        send_msg_lab.bind('<Enter>',lambda Event,func=self.selection_mouse_Enter,
        f=send_msg_lab:func(Event,f))
        read_info_lab.bind('<Enter>',lambda Event,func=self.selection_mouse_Enter,
        f=read_info_lab:func(Event,f))
        # 给label添加鼠标移出事件
        send_msg_lab.bind('<Leave>',lambda Event,func=self.selection_mouse_Leave,
        f=send_msg_lab:func(Event,f))
        read_info_lab.bind('<Leave>',lambda Event,func=self.selection_mouse_Leave,
        f=read_info_lab:func(Event,f))
        # 给发送消息label添加鼠标左键单击事件
        send_msg_lab.bind('<Button-1>',lambda Event,func=self.open_send_page,f_group=f_group,
        f_friend=f_friend:func(Event,f_group,f_friend))
        self.selection = selection_frame
    
    # 打开发送消息界面
    def open_send_page(self,event,f_group,f_friend):
        if self.selection:
            self.selection.destroy()
        # 得到好友的信息,判断是新添加的好友还是界面加载时的好友
        if f_friend in self.group_frame[f_group][4]:
            friend_info = self.group_frame[f_group][4][f_friend]
        if f_friend in self.group_frame[f_group][5]:
            friend_info = self.group_frame[f_group][5][f_friend]
        friend_id = friend_info[0]
        friend_nickname = friend_info[1]
        # 将自己的id和昵称以及朋友的id和昵称传到发送界面
        self.send_msg_page = SendMsgPage(self.userinfo['id'],self.userinfo['nickname'],
        friend_id,friend_nickname)
        self.send_msg_frame[friend_id] = self.send_msg_page
        print(self.send_msg_frame.keys())

    
    # 所有seletion的子控件的移入事件
    def selection_mouse_Leave(self,event,f):
        f['bg'] = '#FBFFFF'
    
    # 所有seletion的子控件的移入事件
    def selection_mouse_Enter(self,event,f):
        f['bg'] = '#A9A9A9'

    # 好友Frame鼠标移出事件
    def friend_frame_labLeave(self,event,f,img_lab,nickname_lab,sig_lab):
        f['bg']= '#2E3138'
        img_lab['bg'] = '#2E3138'
        nickname_lab['bg'] = '#2E3138'
        sig_lab['bg'] = '#2E3138'

    # 好友Frame鼠标移入事件
    def friend_frame_labEnter(self,event,f,img_lab,nickname_lab,sig_lab):
        f['bg']= '#6A7788'
        img_lab['bg'] = '#6A7788'
        nickname_lab['bg'] = '#6A7788'
        sig_lab['bg'] = '#6A7788'
        f['cursor'] = 'fleur'

    
    # 分组列表鼠标移入事件
    def group_mouseEnter(self,event,f):
        if not self.group_frame[f][0]:
            f['bg']='#6A7788'
            f['cursor'] = 'fleur'
            for lab in self.group_frame[f][1:3]:
                lab['bg'] = '#6A7788'
            
    
    #　分组列表鼠标移出事件
    def group_mouseLeave(self,event,f):
        if not self.group_frame[f][0]:
            f['bg']='#2E3138'
            for lab in self.group_frame[f][1:3]:
                lab['bg'] = '#2E3138'

    # 鼠标滚轮滚动事件
    def on_mouseWheel(self,event):
        self.canvas.yview_scroll(-1(event.delta/140),'units')

    # 用canvas画出好友界面
    def get_friendlist_form(self):
        # 好友界面
        self.canvas=Canvas(self)
        self.frame1=Frame(self.canvas,bg='#2E3138')
        myscrollbar=Scrollbar(self,orient="vertical",command=self.canvas.yview,
        bg='#2E3138',activebackground='#2E3138',background='#2E3138',
        troughcolor='#6A7788',width=16,relief=FLAT)
        self.canvas.configure(yscrollcommand=myscrollbar.set,highlightthickness=0)

        myscrollbar.pack(side="right",fill=BOTH)
        self.canvas.config(background='#2E3138')
        self.canvas.pack(side="left",fill=BOTH)
        self.canvas.create_window((0,0),window=self.frame1,anchor='nw',width=388)
        self.get_group_data()

    # 获取分组信息
    def get_group_data(self):
        # 创建字典，绑定分组Frame和它的控件
        self.group_frame = {}
        msg = 'getGroup\n%s'%self.userinfo['id']
        # 发送请求并获得响应
        response = send_request(msg)
        response_arr = response.split('\n')
        for group in response_arr[1:]:
            group_info = group.split(',')
            group_label = []
            f = Frame(self.frame1,bg='#2E3138')
            label1 = Label(f,text=group_info[1],bg='#2E3138',fg='white',font=('',10))
            label1.grid(stick=W,ipady=8,padx=30)
            label2 = Label(f,text=str(group_info[2])+'/'+str(group_info[3]),bg='#2E3138',
            fg='white',font=('',10))
            label2.grid(row=0,column=1,stick=W)
            f.pack(fill=BOTH)


            # 为每一个分组添加一个判断是否被点击的标志
            group_label.append(False)
            group_label.append(label1)
            group_label.append(label2)
            # 将分组的信息存入与该分组frame对象绑定的列表中
            group_label.append(group_info)
            group_label.append({})
            group_label.append([])
            self.group_frame[f] = group_label

    # 根据内容改变滚动条
    def myfunction(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

class FrameBottom(Frame):
    def __init__(self,mainFrame_frame1,userinfo):
        self.mainFrame_frame1 = mainFrame_frame1
        self.userinfo = userinfo
        super().__init__()
        self.createForm()
        self.bind_event()

    def createForm(self):
        # 主界面下方Frame
        self.bottom_frame = Frame(self.mainFrame_frame1).pack()
        self.add_friend = Label(self.bottom_frame,text='+',font=('',14),
        bg='#2E3138',fg='white')
        self.add_friend.pack(side=LEFT,padx=6,ipady=2)
        
    def bind_event(self):
        self.add_friend.bind('<Button-1>',self.to_addPage)
        self.add_friend.bind('<Enter>',self.enter_label)

    def to_addPage(self,event):
        self.add_friend_page = AddFriendPage(self.userinfo)

    def enter_label(self,event):
        self.add_friend['cursor'] = 'fleur'


# 解析图片
def get_image(width,height,filename):
    image_path = os.path.join(BASE_DIR,filename)
    img = pilImage.open(image_path)
    img.thumbnail((width,height))
    ph = ImageTk.PhotoImage(img)
    return ph

if __name__ == '__main__':
    MainPage()