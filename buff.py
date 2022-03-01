#增益列表：攻击力、防御力、伤害加成、岩元素伤害加成、
#   伤害数值加成（基于攻击力）、伤害数值加成（基于防御力）、额外伤害倍率（刀波等）、物理抗性降低、岩元素抗性降低
buff_list = ["ATK","DEF","Dmg_Inc","Rock_Dmg_Inc",
             "Dmg_Num_Inc_A","Dmg_Num_Inc_D","Other_Dmg","Phy_RES_Dec","Rock_RES_Dec"]
on = 1
off = 0
status_list = [on,off]
accu_rate = 0.001
class Buff():
    
    def __init__(self):
        self.on = {}
        self.off = {}
        
    def get(self,status:int,buff_type:str):
        '''
        status on满层，off0层
        buff_type 增益类型 取buff_list内容
        num 增益数值，如80% 输入0.8
        '''
        if buff_type not in buff_list:
            print("get_buff error")
            return 0
        if status == on:
            return self.on.get(buff_type,0)
        elif status == off:
            return self.off.get(buff_type,0)
        else:
            print("get_buff error")
            return 0
    
    def set(self,status:int,buff_type:str,num:float):
        '''
        status on满层，off0层
        buff_type 增益类型 取buff_list内容
        num 增益数值，如80% 输入0.8
        '''
        if buff_type not in buff_list:
            print("set_buff error")
            return
        if status == on:
            self.on[buff_type]=num
        elif status == off:
            self.off[buff_type]=num
        else:
            print("set_buff error")
            return

    #set_buff = set

    def __add__(self,other):
        target = Buff()
        for b in buff_list:
            buff1 = self.on.get(b,0)
            buff2 = other.on.get(b,0)
            target_buff = int(buff1/accu_rate + buff2/accu_rate)*accu_rate
            if(target_buff>0):
                target.on[b] = target_buff
            buff1 = self.off.get(b,0)
            buff2 = other.off.get(b,0)
            target_buff = int(buff1/accu_rate + buff2/accu_rate)*accu_rate
            if(target_buff>0):
                target.off[b] = target_buff
        return target

    def __str__(self):
        return 'on:'+str(self.on)+'\noff:'+str(self.off)

    __repr__ = __str__
        

if __name__=='__main__':
    b = Buff()
    b2 = Buff()
    b.set(on,"ATK",0.466)
    b.set(off,"Dmg_Num_Inc_A",0.8)
    b2.set(on,"ATK",0.6)
    print(b+b2)

