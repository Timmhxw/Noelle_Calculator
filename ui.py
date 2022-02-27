import easygui as gui
import sys

version = 3.0
title = "诺艾尔期望计算器"+str(version)
data = {}
def without_reply(reply):
    '''
    若窗口无返回自动退出程序
    '''
    if reply == None:
            sys.exit(0)

def hello_word():
    msg = '欢迎来到女仆诺艾尔的尾刀期望计算器v'+str(version)+'版本-by-bilibili夜雪千沫\n计算以90级诺艾尔为准'
    gui.msgbox(msg,title)

    with open('readme.txt', 'r',encoding = 'utf-8')as file:
        msg = file.read()

    msg = msg+"\n我已经阅读上述事项"
    while not gui.ccbox(msg,title,["同意","不同意"]):
        gui.msgbox(" 你必须读！")

def user_board_data():
    msg = "请输入你的女仆的攻击力:"
    ATK = gui.integerbox(msg,title,lowerbound=0,upperbound=5000)
    without_reply(ATK)
    
    msg = "请输入你的女仆的防御力:"
    DEF = gui.integerbox(msg,title,lowerbound=0,upperbound=5000)
    without_reply(DEF)
    
    msg = '请输入你的女仆几命:'
    Noelle_num = gui.integerbox(msg,title,lowerbound=0,upperbound=6)
    without_reply(Noelle_num)

    data.update({'ATK':ATK,'DEF':DEF,'Noelle_num':Noelle_num})

def magn_data():
    msg = '请输入你的女仆的普攻倍率等级:'
    A_Magn = gui.integerbox(msg,title,lowerbound=1,upperbound=11)
    without_reply(A_Magn)
    
    msg = '请输入你的女仆的大招倍率等级:'
    Q_Magn = gui.integerbox(msg,title,lowerbound=1,upperbound=13)
    without_reply(Q_Magn)

    data.update({'A_Magn':A_Magn,'Q_Magn':Q_Magn})
    
def crit_data():
    msg = '请输入暴击率（例：0.82）：'
    Crit_rate = gui.enterbox(msg,title)
    while Crit_rate:
        try:
            Crit_rate = float(Crit_rate)
            if 0.05<=Crit_rate<=1:
                break
            gui.msgbox('暴击率输入错误！',title)
        except:
            gui.msgbox('暴击率输入错误！',title)
        Crit_rate = gui.enterbox(msg,title)
    without_reply(Crit_rate)
    
    msg = '请输入暴击伤害（例：1.82）：'
    Crit_dmg = gui.enterbox(msg,title)
    while Crit_dmg:
        try:
            Crit_dmg = float(Crit_dmg)
            if 0.5<=Crit_dmg<=5:
                break
            gui.msgbox('暴击伤害输入错误！',title)
        except:
            gui.msgbox('暴击伤害输入错误！',title)
        Crit_dmg = gui.enterbox(msg,title)
    without_reply(Crit_dmg)
        
    data.update({'Crit_rate':Crit_rate,'Crit_dmg':Crit_dmg})
    
def weapon_data():
    msg = '请选择你的武器:'
    Weapons_list = {'赤角':1,'螭骨':2, '天空':3, '白影':4, '无工':5, '狼末':6, '黑岩':7,'西风':8}
    Weapon = gui.choicebox(msg,title,Weapons_list.keys())
    without_reply(Weapon)
    
    msg = '请输入武器精炼度:'
    Weapon_num = gui.integerbox(msg,title,1,1,5)
    without_reply(Weapon_num)

    data.update({'Weapon':Weapons_list[Weapon],'Weapon_num':Weapon_num})
    
def relic_data():
    msg = '请选择你的圣遗物:'
    Relics_list = {'角斗士':1,'逆飞':2, '华馆':3}
    Relic = gui.choicebox(msg,title,Relics_list.keys())
    without_reply(Relic)
    
    data.update({'Relic':Relics_list[Relic]})


def input_list():
    hello_word()
    user_board_data()
    magn_data()
    crit_data()
    weapon_data()
    relic_data()
    return data

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
##    print(input_list())
##    print(inspect_choose())
    output_choose('hello')
