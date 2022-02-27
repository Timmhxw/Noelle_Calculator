#增益列表：攻击力、防御力、伤害加成、岩元素伤害加成、伤害数值加成（基于攻击力）、伤害数值加成（基于防御力）、额外伤害倍率（刀波等）
buff_list = ["ATK","DEF","Dmg_Inc","Rock_Dmg_Inc",
             "Dmg_Num_Inc_A","Dmg_Num_Inc_D","Other_Dmg"]
on = 1
off = 0
accu_rate = 0.001
class Buff():
    
    def __init__(self):
        self.on = {}
        self.off = {}

    def set_buff(self,status:int,buff_type:str,num:float):
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
    b.set_buff(on,"ATK",0.466)
    b.set_buff(off,"Dmg_Num_Inc_A",0.8)
    b2.set_buff(on,"ATK",0.6)
    print(b+b2)

