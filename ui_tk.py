from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox,filedialog
from ast import literal_eval
from weapon_data import weapons_list
from Relic_data import Relics_list
from other_buff import other_buff_list
from sys import exit
version = 3.0
title = "诺艾尔期望计算器"+str(version)
data = {}
error_place = []
data_name = [["ATK","攻击力"],
            ["DEF","防御力"],
            ["Noelle_num","命座数"],
            ["A_Magn","普攻等级"],
            ["Q_Magn","大招等级"],
            ["Crit_rate","暴击率"],
            ["Crit_dmg","暴击伤害"],
            ["Weapon","武器"],
            ["Weapon_num","武器精炼度"],
            ["Relic","圣遗物套装"]]
data_type = ["int",
             "int",
             "int",
             "int",
             "int",
             "float",
             "float",
             "choose",
             "int",
             "choose"]
data_range = [[0,5000],
              [0,5000],
              [0,6],
              [1,11],
              [1,13],
              [0.05,1],
              [0.5,5],
              weapons_list,
              [1,5],
              Relics_list]


def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height - 75) / 2)
    root.geometry(size)
    root.update()


def get_image(filename,width,height):
    im = Image.open(filename).resize((width,height))
    im = im.convert('RGBA')
    r, g, b, alpha = im.split()
    alpha = alpha.point(lambda i: i>0 and 128)
    im.putalpha(alpha)
    return ImageTk.PhotoImage(im)

def closeWindow():
    ans = messagebox.askyesno(title='Warning',message='Close the window?')
    if ans:
        root.destroy()
        exit(0)

    else:
        return

#ui_init_start

width=600
height=800
root = Tk()

#设置标题、图标，居中显示
root.title(title)
root.iconbitmap('favicon.ico')
center_window(root,width,height)

##root.attributes("-toolwindow", 1)#删去最大化最小化
root.resizable(0, 0)#禁止修改大小
root.protocol('WM_DELETE_WINDOW', closeWindow)#关闭窗口提示

#设置背景
L_content = StringVar()
im = get_image('background.png',width,height)
L = Label(root,image=im,textvariable = L_content,justify = 'center',
          compound = 'center',#组合方式,图片相对于文字
                    font = ('宋体',15),
                    fg='red')
L.place(x=0,y=0,width=width,height=height)

#ui_init_end


def hello_world():
    msg = '欢迎来到女仆诺艾尔的尾刀期望计算器v'+str(version)+'版本\nby-bilibili夜雪千沫\n计算以90级诺艾尔对虚弱的93级急冻树伤害为准'
    L_content.set(msg)
    f = Frame(root,bg='white')
    f.pack(side='bottom',fill='x')
    B = Button(f,text = "开始使用",width=15,height=2,command=root.quit)
    B.pack(side='bottom')
    root.mainloop()
    f.forget()
    
    with open('readme.txt', 'r',encoding = 'utf-8')as file:
        msg = file.read()

    msg = msg+"我已经阅读上述事项"
    L_content.set(msg)
    L.config(font = ('宋体',20))
    global frame_button,B1,B2,frame_single,B3
    frame_button = Frame(root,bg='white')
    frame_button.pack(side='bottom',fill='x')
    B1 = Button(frame_button,text='同意',width=10,height=2,command=root.quit)
    B1.grid(row=0,column=1,padx=100)
    B2 = Button(frame_button,text='不同意',width=10,height=2,command=lambda : messagebox.showwarning(message=" 你必须读！"))
    B2.grid(row=0,column=0,padx=100)
    frame_single = Frame(root,bg='white')
    frame_single.pack(side='bottom',fill='x')
    frame_single.pack_forget()
    B3 = Button(frame_single,text='确定',width=10,height=2,command=root.quit)
    B3.pack(side='top')

    root.mainloop()
    L_content.set('')
##    L.place_forget()

def cut_map(m):
    s= '\t{'
    i=0
    for k,v in m.items():
        s = s + "%s:%s  "%(k,v)
        i=(i+1)%4
        if i==0:
            s = s+'\n\t'
    while(s[-1]in[' ','\n','\t']):
        s = s[:-1]
    return s+'}'

def ck_single_data_valid(i):
    name = data_name[i][0]
    error_place.append(name)
    temp = data.get(name)
    print(name,temp)
    if temp == None:
        print(1)
        return False
    typed = data_type[i]
    if typed == "choose":
        if type(temp)!=int:
            print(2)
            return False
        if(temp<1)|(temp>len(data_range[i])):
            print(3)
            return False
    else:
        if str(type(temp))!=("<class '"+typed+"'>"):
            print(4)
            return False
        if(temp<data_range[i][0])|(temp>data_range[i][1]):
            print(5)
            return False
    error_place.pop()
    print(name,"is ok")
    return True

def ck_data_valid():
    for i in range(len(data_name)):
        if not ck_single_data_valid(i):
            return False
    return True
  
def choose_text_data():
    reply = messagebox.askyesno(message="是否选择从文件读取数据？")
    if not reply:
        return False
    msg = "请在input.txt中输入/修改数据，对应关系为：\n"
    msg = msg + '''
        "ATK":"攻击力"
        "DEF":"防御力"
        "Noelle_num":"命座数"
        "A_Magn":"普攻等级"
        "Q_Magn":"大招等级"
        "Crit_rate":"暴击率"
        "Crit_dmg":"暴击伤害"
        "Weapon":"武器" 此处输入武器对应编号：\n%s
        "Weapon_num":"武器精炼度"
        "Relic":"圣遗物套装" 此处输入圣遗物对应编号：\n%s
        '''%(cut_map(weapons_list),cut_map(Relics_list))
    msg = msg + "\n是否已输入完成？"
    L = Label(root,text=msg,fg='black',bg='white',justify='left',font = ('宋体',15))
    L.pack(side='top',fill='x',expand=True)
    global frame_single,frame_button
    frame_button.pack_forget()
    frame_single.pack(side='bottom',fill='x')
    while True:
        root.mainloop()
        try:
            with open("input.txt",'r',encoding = "utf-8")as f:
                s = f.readline()               
            data.update(literal_eval(s))
            if ck_data_valid():
                L.forget()
                return True
            else:
                msg = "%s数据错误，是否重试？若否，跳转至UI输入..."%(error_place[0])
                reply = messagebox.askretrycancel(message=msg)
                if not reply:
                    break
        except:
            msg = "文件读写错误，是否重试？若否，跳转至UI输入..."
            reply = messagebox.askretrycancel(message=msg)
            if not reply:
                break
    L.forget()
    frame_single.pack_forget()
    frame_button.pack(side='bottom',fill='x')
    return False

index = 0
frame_list = []


def build_AD():
    f = Frame(root,bg='white')
    Label(f,text="请输入女仆的攻击力与防御力",font = ('宋体',15),bg='white').pack(side='top',fill='x',expand=True)
    f1 = Frame(f,bg='white')
    Label(f1,text="攻击力:",font = ('宋体',15),bg='white',justify='right',width=20).grid(row=0,column=0,padx=25)
    v1 = StringVar()
    Entry(f1,textvariable=v1).grid(row=0,column=1)
    f1.pack()
    
    f2 = Frame(f,bg='white')
    Label(f2,text="防御力:",font = ('宋体',15),bg='white',justify='right',width=20).grid(row=0,column=0,padx=25)
    v2 = StringVar()
    Entry(f2,textvariable=v2).grid(row=0,column=1)
    f2.pack()
    
    frame_list.append([f,[0,1],[v1,v2]])

def build_level():
    f = Frame(root,bg='white')
    Label(f,text="请选择女仆的命座数、普攻天赋等级与大招天赋等级",font = ('宋体',15),bg='white').pack(side='top',fill='x',expand=True)
    f1 = Frame(f,bg='white')
    Label(f1,text="命座数:",font = ('宋体',15),bg='white',anchor='e',padx=0,width=20).grid(row=0,column=0,padx=25)#右对齐
    v1 = IntVar()
    Scale(f1,
          from_ = 0,         #设置最小值
          to = 6,             #设置最大值
          resolution = 1,       #设置步距值
          orient = HORIZONTAL,  #设置水平方向
          variable = v1,          #绑定变量
          tickinterval=1,       #分辨率
          length = 200,         #长度（像素）
          showvalue=1,          #是否显示数值
          bg='white'
          ).grid(row=0,column=1)
    v1.set(6)
    f1.pack(fill='x',expand=True)
    
    f2 = Frame(f,bg='white')
    Label(f2,text="普攻天赋等级:",font = ('宋体',15),bg='white',anchor='e',padx=0,width=20).grid(row=0,column=0,padx=25)
    v2 = IntVar()
    Scale(f2,
          from_ = 1,         #设置最小值
          to = 11,             #设置最大值
          resolution = 1,       #设置步距值
          orient = HORIZONTAL,  #设置水平方向
          variable = v2,          #绑定变量
          tickinterval=1,
          length = 200,
          showvalue=1,          #是否显示数值
          bg='white'
          ).grid(row=0,column=1)
    v2.set(10)
    f2.pack(fill='x',expand=True)

    f3 = Frame(f,bg='white')
    Label(f3,text="大招天赋等级:",font = ('宋体',15),bg='white',anchor='e',padx=0,width=20).grid(row=0,column=0,padx=25)
    v3 = IntVar()
    Scale(f3,
          from_ = 1,         #设置最小值
          to = 13,             #设置最大值
          resolution = 1,       #设置步距值
          orient = HORIZONTAL,  #设置水平方向
          variable = v3,          #绑定变量
          tickinterval=1,
          length = 200,
          showvalue=1,          #是否显示数值
          bg='white'            
          ).grid(row=0,column=1)
    v3.set(13)
    f3.pack(fill='x',expand=True)

    frame_list.append([f,[2,3,4],[v1,v2,v3]])

def build_crit():
    f = Frame(root,bg='white')
    Label(f,text="请输入女仆的暴击率与暴击伤害",font = ('宋体',15),bg='white').pack(side='top',fill='x',expand=True)
    f1 = Frame(f,bg='white')
    Label(f1,text="暴击率（例：0.81）:",font = ('宋体',15),bg='white',anchor='e',width=20).grid(row=0,column=0,padx=25)
    v1 = StringVar()
    Entry(f1,textvariable=v1).grid(row=0,column=1)
    f1.pack()
    
    f2 = Frame(f,bg='white')
    Label(f2,text="暴击伤害（例：1.83）:",font = ('宋体',15),bg='white',anchor='e',width=20).grid(row=0,column=0,padx=25)
    v2 = StringVar()
    Entry(f2,textvariable=v2).grid(row=0,column=1)
    f2.pack()
    frame_list.append([f,[5,6],[v1,v2]])

def build_WR():
    f = Frame(root,bg='white')
    Label(f,text="请选择女仆的武器、精炼度以及圣遗物",font = ('宋体',15),bg='white').pack(side='top',fill='x',expand=True)
    f1 = Frame(f,bg='white')
    n = 3
    Label(f1,text="武器:",font = ('宋体',15),bg='white',anchor='e',padx=0,width=20).grid(row=0,column=0,padx=25,pady=10,rowspan=len(weapons_list)//n+1)
    v1 = IntVar()
    for k,v in weapons_list.items():
        Radiobutton(f1,text=k,variable=v1,value=v,font = ('宋体',10),bg='white').grid(row=(v-1)//n,column=(v-1)%n+1,padx=25,pady=10)
    v1.set(1)
    f1.pack(fill='x',expand=True)
    
    f2 = Frame(f,bg='white')
    Label(f2,text="精炼度:",font = ('宋体',15),bg='white',anchor='e',padx=0,width=20).grid(row=0,column=0,padx=25)
    v2 = IntVar()
    Scale(f2,
          from_ = 1,         #设置最小值
          to = 5,             #设置最大值
          resolution = 1,       #设置步距值
          orient = HORIZONTAL,  #设置水平方向
          variable = v2,          #绑定变量
          tickinterval=1,
          length = 200,
          showvalue=1,          #是否显示数值
          bg='white'
          ).grid(row=0,column=1)
    v2.set(1)
    f2.pack(fill='x',expand=True,pady=10)

    f3 = Frame(f,bg='white')
    Label(f3,text="圣遗物:",font = ('宋体',15),bg='white',anchor='e',padx=0,width=20).grid(row=0,column=0,padx=25,pady=10,rowspan=len(Relics_list))
    v3 = IntVar()
    for k,v in Relics_list.items():
        Radiobutton(f3,text=k,variable=v3,value=v,font = ('宋体',10),bg='white').grid(row=v,column=1,padx=25,pady=10)
    v3.set(1)
    f3.pack(fill='x',expand=True)
    frame_list.append([f,[7,8,9],[v1,v2,v3]])

def frame_next():
    root.quit()
    global index
    for i in range(len(frame_list[index][1])):
        i_ = frame_list[index][1][i]
        v = frame_list[index][2][i].get()
        
        if type(v)==str:
            try:
                if data_type[i_]=='int':
                    v = int(v)
                else:
                    v = float(v)
            except:
                msg = data_name[i_][1]+"类型输入错误"
                messagebox.showerror(message=msg)
                return
        name = data_name[i_][0]
        data[name] = v
        if  not ck_single_data_valid(i_):
            msg = data_name[i_][1]+"范围输入错误"
            messagebox.showerror(message=msg)
            return
    frame_list[index][0].forget()
    index += 1

def frame_last():
    root.quit()
    global index
    if index>0:
        frame_list[index][0].forget()
        index -= 1
    else:
        messagebox.showerror(message="当前已是第一处数据")

def input_list():
    hello_world()
    if choose_text_data():
        return data
    global frame_button,B1,B2,index

    B1.config(text='确定',command=frame_next)
    B2.config(text='返回',command=frame_last)

    
    build_AD()
    build_level()
    build_crit()
    build_WR()

    while index<len(frame_list):
        frame_list[index][0].pack(side='top',fill='x',expand=True)
        root.mainloop()
    messagebox.showinfo(message="输入完毕")
    frame_button.forget()

    with open("input.txt",'w',encoding = 'utf-8')as f:
        f.write(str(data))
    return data

def choose_buff():
    msg = "是否自定义buff？当前默认双岩、岩伤杯"
    return messagebox.askyesno(message=msg)

def get_buff():
    f = Frame(root,bg='white')
    Label(f,text="请选择buff:",font = ('宋体',15),bg='white').pack(side='top',fill='x',expand=True)
    v = StringVar()
    
    lb = Listbox(f,listvariable=v,selectmode='multiple',bg='white')
    for key in other_buff_list.keys():
        lb.insert('end',key)
    lb.selection_set(0,1)

    lb.config(selectmode='multiple')
    lb.pack()
    f.pack(side='top',fill='x',expand=True)
    global frame_single
    frame_single.pack(side='bottom',fill='x')
    root.mainloop()
    f.forget()
    frame_single.pack_forget()
    return lb.curselection()


def show_msg(s:str):
    '''
    提示消息
    参数s为输出的内容
    '''
    if type(s)!=str:
        s = str(s)
    msg = s
    L = Label(root,text=msg,fg='black',bg='white',justify='left',font = ('宋体',15),pady=50)
    L.pack(side='top',fill='x',expand=True)
    global frame_single
    frame_single.pack(side='bottom',fill='x')
    root.mainloop()
    frame_single.pack_forget()
    L.forget()

def inspect_choose():
    msg = '是否检查你的女仆的练度?'
    return messagebox.askyesno(message=msg)

def output_choose(s:str):
    '''
    选择是否保存到本地
    参数s为待保存的内容
    '''
    if type(s)!=str:
        s = str(s)
    if not messagebox.askyesno(message='是否保存到本地？'):
        return
    file_path = filedialog.asksaveasfilename(title=u'保存文件',defaultextension='.txt',filetypes=[("文本文件",".txt")])
    if file_path==None:
        return
    if(file_path.find('.')==-1):
        file_path = file_path + '.txt'
    with open(file_path,'w')as file:
        file.write(s)

def goodbye_word():
    msg = '欢迎来到女仆诺艾尔的尾刀期望计算器v'+str(version)+'版本\nby-bilibili夜雪千沫\n感谢您的使用'
    L_content.set(msg)
    global frame_single,B3
    B3.config(text = '退出',command=root.destroy)
    frame_single.pack(side='bottom',fill='x')
    root.mainloop()
    

if __name__=='__main__':
    input_list()
    print(get_buff())
    show_msg('you ara')
    print(inspect_choose())
    output_choose('hi')
    goodbye_word()

