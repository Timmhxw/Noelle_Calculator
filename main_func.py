import ui
import weapon_data as wp
import Relic_data as re
import buff
import skill_data
import other_buff
class Noelle():
    def __init__(self):
        '''
        初始化数据
        basic_data_list={
            "ATK":"攻击力"
            "DEF":"防御力"
            "Noelle_num":"命座数"
            "A_Magn":"普攻等级"
            "Q_Magn":"大招等级"
            "Crit_rate":"暴击率"
            "Crit_dmg":"暴击伤害"
            "Weapon":"武器"
            "Weapon_num":"武器精炼度"
            "Relic":"圣遗物套装"
            "basic_ATK":"攻击力白板"
            "basic_DEF":"防御力白板"
        }
        '''
        data =  ui.input_list()
##        data = {'ATK': 1308, 'DEF': 2011, 'Noelle_num': 6,
##                'A_Magn': 10, 'Q_Magn': 13, 'Crit_rate': 0.591, 'Crit_dmg': 2.587,
##                'Weapon': 1, 'Weapon_num': 2, 'Relic': 1}#测试数据
        self.basic_data = data
        self.basic_data.update({'basic_ATK':191+wp.basic_ATK[data['Weapon']],'basic_DEF':799})
        self.A_Magn ={}
        for k,v in skill_data.A_Magn.items():
            self.A_Magn[k]= v[data["A_Magn"]]
        self.DEF2ATK = skill_data.Q_Magn[data["Q_Magn"]]
        if(data["Noelle_num"]==6):
            self.DEF2ATK += 0.5
        self.buff = wp.get_buff(data["Weapon"],data["Weapon_num"])+re.get_buff(data["Relic"])+other_buff.get_buff()
        self.output = ''

    def calc(self):
        data = self.basic_data.copy()
        self.hit = {buff.on:{},buff.off:{}}
        self.calc_ATK = {buff.on:0,buff.off:0}
        self.expect = {buff.on:0,buff.off:0}
        b = self.buff
        for st in buff.status_list:
            calc_DEF = data["DEF"]+b.get(st,"DEF")*data["basic_DEF"]
            calc_ATK = data["ATK"]+b.get(st,"ATK")*data["basic_ATK"]+calc_DEF*self.DEF2ATK
            self.calc_ATK[st] = calc_ATK
            for k,v in self.A_Magn.items():
                multi_first = v * calc_ATK + b.get(st,"Dmg_Num_Inc_A")*calc_ATK + b.get(st,"Dmg_Num_Inc_D")*calc_DEF#基础伤害乘区
                multi_second = data["Crit_dmg"]+1#双爆乘区
                multi_third = b.get(st,"Dmg_Inc")+b.get(st,"Rock_Dmg_Inc")+1#增伤乘区
                multi_fourth = 190.0/(200.0+90+93)*1.05#防御抗性乘区，岩抗10%，双岩减岩抗20%
                hit = multi_first * multi_second * multi_third * multi_fourth
                if b.get(st,"Other_Dmg"):
                    hit_add = b.get(st,"Other_Dmg") * calc_ATK * multi_second * (b.get(st,"Dmg_Inc")+1)* 190.0/(200.0+90+93)*0.7#物抗30%
                    hit = hit + hit_add
                self.hit[st][k] = hit
            expect = multi_first * (data["Crit_rate"]*data["Crit_dmg"]+1)*multi_third*multi_fourth
            if b.get(st,"Other_Dmg"):
                expect_add = b.get(st,"Other_Dmg") * calc_ATK * (data["Crit_rate"]*data["Crit_dmg"]+1) * (b.get(st,"Dmg_Inc")+1)* 190.0/(200.0+90+93)*0.7#物抗30%
                expect = expect + expect_add
            self.expect[st] = expect

    def __str__(self):
        if self.output:
            return self.output
        s = ''
        s = s+'女仆吃满被动时的开大攻击力为：{:.2f}'.format(self.calc_ATK[buff.on])+'\n'
        for i in range(1,5):
            s = s+'女仆开大第{:d}刀暴击的伤害为：{:.2f}'.format(i,self.hit[buff.on][i])+'\n'
        s = s+'女仆无被动时的开大攻击力为：{:.2f}'.format(self.calc_ATK[buff.off])+'\n'
        for i in range(1,5):
            s = s+'女仆开大第{:d}刀暴击的伤害为：{:.2f}'.format(i,self.hit[buff.off][i])+'\n'
        s = s+'该女仆开大尾刀的最大输出期望值为：{:.2f}'.format(self.expect[buff.on])+'\n'
        s = s+'该女仆开大尾刀的最小输出期望值为：{:.2f}'.format(self.expect[buff.off])
        self.output = s
        return s

    __repr__ = __str__

    def inspect(self):
        '''
        练度检查
        '''
        if ui.inspect_choose()==1:
            s = ''
            if self.basic_data["A_Magn"]<9:
                s += '你的普攻等级过低！\n'
            if self.basic_data["Q_Magn"]<12:
                s += '你的大招等级过低！'
            if self.basic_data["A_Magn"]<self.basic_data["Q_Magn"]-3:
                s += '先拉普攻！！哼啊啊啊啊啊啊啊啊！'
            expect = self.expect[buff.on]
            if expect < 18000:
                s += '你的女仆DPS不及格！'
            elif 18000 < expect < 22000:
                s += '你的女仆处于及格水平'
            elif 22000 < expect < 24000:
                s += '你的女仆处于小毕业水平'
            elif 24000 < expect:
                s += '你的女仆已经毕业啦！'
            ui.show_msg(s)
    

if __name__ =='__main__':
    n = Noelle()
    print(n.basic_data)
    n.calc()
    ui.show_msg(n)
    n.inspect()
    ui.output_choose(n)
    ui.goodbye_word()
