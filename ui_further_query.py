from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox,filedialog
from ast import literal_eval
from sys import exit

def center_window(root:Tk, width:int, height:int):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height - 75) / 2)
    root.geometry(size)
    root.update()

def get_image(im,width,height):
    im = im.resize((width,height))
    im = im.convert('RGBA')
    r, g, b, alpha = im.split()
    alpha = alpha.point(lambda i: i>0 and 128)
    im.putalpha(alpha)
    return ImageTk.PhotoImage(im)

class Query_for_other_person():
    def __init__(self,name:str,record:dict,query_list:list):
        '''
            query_list:List[dict]=
            [
                {
                    'item': what to ask for,the type should be 'str'\n
                    'type': 'int' 'choose' or 'float', need to be string\n
                    'range': [low,high] or dict[str,int] if the type is choose\n
                }
            ]
        '''
        #ui_init_start
        def closeWindow():
            ans = messagebox.askyesno(title='Warning',message='Close the window?')
            if ans:
                root.destroy()
                exit(1)
                
            else:
                return

        def ck_single_data_valid(name,temp,typed,ranged):
            print(name,temp)
            if temp == None:
                print(1)
                return False
            if typed == "choose":
                if type(temp)!=int:
                    print(2)
                    return False
                if(temp not in ranged.values()):
                    print(3)
                    return False
            else:
                if str(type(temp))!=("<class '"+typed+"'>"):
                    print(4)
                    return False
                if(temp<ranged[0])|(temp>ranged[1]):
                    print(5)
                    return False
            print(name,"is ok")
            return True

        def next():
            root.quit()
            
            for name_i,var_i,type_i,range_i in self.data:
                v = var_i.get()
                if type(v)==str:
                    try:
                        if type_i=='int':
                            v = int(v)
                        else:
                            v = float(v)
                    except:
                        msg = name_i+"类型输入错误"
                        messagebox.showerror(message=msg)
                        return
                self.record[name_i] = v
                if not ck_single_data_valid(name_i,v,type_i,range_i):
                    msg = name_i+"范围输入错误"
                    messagebox.showerror(message=msg)
                    return
            f.forget()
            self.success = True
        
        im = Image.open('background.png')
        width,height = im.size
        if height>800:
            width = int(width/height*800)
            height = 800
        root = Toplevel() # 代码运行时只允许有一个TK，另一个用toplevel以弹窗方式执行。

        #设置标题、图标，居中显示
        root.title(name+'数值获取')
        root.iconbitmap('favicon.ico')
        center_window(root,width,height)

        ##root.attributes("-toolwindow", 1)#删去最大化最小化
        root.resizable(0, 0)#禁止修改大小
        root.protocol('WM_DELETE_WINDOW', closeWindow)#关闭窗口提示
       
        #设置背景
        L_content = StringVar()
        L_content.set('')
        im = get_image(im,width,height)
        L = Label(root,image=im,textvariable = L_content,justify = 'center',
                compound = 'center',#组合方式,图片相对于文字
                            font = ('宋体',15),
                            fg='red')
        L.place(x=0,y=0,width=width,height=height)
        if record.get(name):
            ans = messagebox.askyesno(title='提示',message='已填写数据，是否读取缓存?')
            if ans:
                root.destroy()
                return
        self.data = []
        self.record = {}
        #ui_init_end
        f = Frame(root,bg='white')
        Label(f,text="请输入{}的以下数据".format(name),font = ('宋体',15),bg='white').pack(side='top',fill='x',expand=True)
        for query in query_list:
            if(type(query.get('item',0))!=str)or(query.get('type',0)not in ['int','float','choose']):
                print('query wrong!')
                return
            if((query['type']=='choose')and(type(query.get('range',0))!=dict))or((query['type']!='choose')and(type(query.get('range','0'))!=list)):
                print('query wrong!')
                return
            if query['type']!='choose':
                f1 = Frame(f,bg='white')
                Label(f1,text=f"{query['item']}:",font = ('宋体',15),bg='white',justify='right',width=20).grid(row=0,column=0,sticky='e')
                v1 = StringVar()
                Entry(f1,textvariable=v1).grid(row=0,column=1,sticky='w')
                f1.pack(side='top',fill='x',expand=True,pady=10)
            else:
                f1 = Frame(f,bg='white')
                Label(f1,text=f"{query['item']}:",font = ('宋体',15),bg='white',anchor='e',width=20).grid(row=0,column=0,rowspan=len(query['range']),sticky='e')
                v1 = IntVar()
                for k,v in query['range'].items():
                    Radiobutton(f1,text=k,variable=v1,value=v,font = ('宋体',10),bg='white').grid(row=v,column=1,sticky='w')
                v1.set(1)
                f1.pack(side='top',fill='x',expand=True,pady=10)
            f1.columnconfigure(0,minsize=width//2)
            f1.columnconfigure(1,minsize=width//2)

            self.data.append((query['item'],v1,query['type'],query['range']))
        frame_button = Frame(root,bg='white')
        frame_button.pack(side='bottom',fill='x')
        B = Button(frame_button,text='确定',width=10,height=2,command=next)
        B.pack(side='top')
        self.success = False
        while not self.success:
            f.pack(side='top',fill='x',expand=True)
            root.mainloop()
        root.destroy()
        record.update({name:self.record.copy()})

if __name__=='__main__':
    A = {}
    from Relic_data import Relics_list
    try:
        Query_for_other_person('五郎',A,[
            {
                'item':'暴击',
                'type':'float',
                'range':[0.5,5]
            },
            {
                'item':'命座',
                'type':'int',
                'range':[0,6]
            },
            {
                'item':'圣遗物',
                'type':'choose',
                'range':Relics_list
            },
            {
                'item':'是否至少三岩',
                'type':'choose',
                'range':{'是':1,'否':0}
            }
        ])
        print(A)
    except:
        print('window has been closed')
    