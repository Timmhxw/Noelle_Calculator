import easygui as gui
from sys import exit
from ast import literal_eval
from weapon_data import weapons_list
from Relic_data import Relics_list
from other_buff import other_buff_list
version = 3.0
title = "诺艾尔期望计算器"+str(version)
data = {}
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
    
def without_reply(reply,back_able=False):
    '''
    若窗口无返回自动退出程序
    '''
    if reply == None:
        if back_able:
            msg = "是退出程序，还是退至上一界面"
            if gui.ccbox(msg,title,["退出","退至上一界面"]):
                exit(0)
            else:
                return(False)
        exit(0)
    return True

def hello_word():
    msg = '欢迎来到女仆诺艾尔的尾刀期望计算器v'+str(version)+'版本-by-bilibili夜雪千沫\n计算以90级诺艾尔对虚弱的93级急冻树伤害为准'
    without_reply(gui.msgbox(msg,title))

    with open('readme.txt', 'r',encoding = 'utf-8')as file:
        msg = file.read()

    msg = msg+"\n我已经阅读上述事项"
    while not gui.ccbox(msg,title,["同意","不同意"]):
        gui.msgbox(" 你必须读！")
        
def ck_data_valid():
    for i in range(len(data_name)):
        name = data_name[i][0]
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
        print(name,"is ok")
    return True
 
def choose_text_data():
    msg = "是否选择从文件读取数据？"
    if gui.ccbox(msg,title,["是","否"]):
        msg = "请在input.txt中输入/修改数据，对应关系为：\n"
        msg = msg + '''
            "ATK":"攻击力"
            "DEF":"防御力"
            "Noelle_num":"命座数"
            "A_Magn":"普攻等级"
            "Q_Magn":"大招等级"
            "Crit_rate":"暴击率"
            "Crit_dmg":"暴击伤害"
            "Weapon":"武器" 此处输入武器对应编号：%s
            "Weapon_num":"武器精炼度"
            "Relic":"圣遗物套装" 此处输入圣遗物对应编号：%s
            '''%(weapons_list,Relics_list)
        msg = msg + "\n是否已输入完成？"
        without_reply(gui.msgbox(msg,title))
        try:
            with open("input.txt",'r',encoding = "utf-8")as f:
                s = f.readline()               
            data.update(literal_eval(s))
            if ck_data_valid():
                return True
            else:
                msg = "数据错误，自动跳转至UI输入..."
                gui.msgbox(msg,title)
        except:
            msg = "文件读写错误，自动跳转至UI输入..."
            gui.msgbox(msg,title)
    return False

def work(name,typed,ranged):
    if typed == "int":
        msg = "请输入女仆的"+name[1]
        reply = gui.integerbox(msg,title,lowerbound=ranged[0],upperbound=ranged[1])
    elif typed == "choose":
        msg = "请选择女仆的"+name[1]
        reply = gui.choicebox(msg,title,ranged.keys())
        if reply:
            reply = ranged[reply]
    elif typed == "float":
        msg = "请输入女仆的"+name[1]+"(例："+str(ranged[0]*2+0.8)+")"
        while True:
            reply = gui.enterbox(msg,title)
            if reply!=None:
                try:
                    reply = float(reply)
                    if ranged[0]<=reply<=ranged[1]:
                        break
                except:
                    pass
                msg = name[1]+"输入错误！"
                gui.msgbox(msg,title)
    if without_reply(reply,True):
        data.update({name[0]:reply})
        return True
    else:
        return False

def input_list():
    hello_word()
    if choose_text_data():
        return data
##    user_board_data()
##    magn_data()
##    crit_data()
##    weapon_data()
##    relic_data()
    index = 0
    while index<len(data_type):
        if work(data_name[index],data_type[index],data_range[index]):
            index += 1
        else:
            if index :
                index -= 1
            else:
                msg = "当前已是第一处数据"
                gui.msgbox(msg,title)
    
    with open("input.txt",'w',encoding = 'utf-8')as f:
        f.write(str(data))
    return data

def choose_buff():
    msg = "是否自定义buff？当前默认双岩、岩伤杯"
    if gui.ccbox(msg,title,["是","否"]):
        return True
    else:
        return False

def get_buff():
    msg = "请选择buff："
    reply = gui.multchoicebox(msg,title,other_buff_list.keys())
    if reply:
        buff = ()
        for key in reply:
            buff += (other_buff_list[key],)
    else:
        buff = (0,1)
    return buff
            

def show_msg(s:str):
    '''
    提示消息
    参数s为输出的内容
    '''
    if type(s)!=str:
        s = str(s)
    msg = s
    without_reply(gui.msgbox(msg,title))

def inspect_choose():
    msg = '是否检查你的女仆的练度'
    reply = gui.ynbox(msg,title)
    if reply:
        return 1
    else:
        return 2

def output_choose(s:str):
    '''
    选择是否保存到本地
    参数s为待保存的内容
    '''
    if type(s)!=str:
        s = str(s)
    msg = '是否保存到本地？'
    reply = gui.ynbox(msg,title)
    if reply:
        msg = '请输入文件的名称：'
        filename = gui.filesavebox(msg,title,filetypes = ['*.txt'])
        without_reply(filename)
        if(filename.find('.')==-1):
            filename = filename + '.txt'    
        with open(filename,'w')as file:
            file.write(s)   
    
def goodbye_word():
    msg = '欢迎来到女仆诺艾尔的尾刀期望计算器v'+str(version)+'版本-by-bilibili夜雪千沫\n感谢您的使用'
    gui.msgbox(msg,title)

if __name__=='__main__':
    print(input_list())
    print(get_buff())
##    print(inspect_choose())
    output_choose('hello')
