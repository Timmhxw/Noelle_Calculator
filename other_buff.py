import buff
from ui_further_query import Query_for_other_person
other_buff_list = {"双岩":0,"岩伤杯":1,"钟离":2,"夜兰":3,'五郎':4,'云堇':5}
cache = {}
class Person():
    def __init__(self) -> None:
        pass
    @property
    def query(self):
        pass
    def calc_buff(self,data)->buff.Buff:
        pass

class WuLang(Person):
    @property
    def query(self):
        return [
        {
            'item':'命座数',
            'type':'int',
            'range':[0,6],
        },
        {
            'item':'e天赋等级',
            'type':'int',
            'range':[1,13],
        },
        {
            'item':'是否至少三岩',
            'type':'choose',
            'range':{'是':1,'否':0}
        }
    ]
    E_DEF_Magn = {1:206,2: 222, 3: 237, 4:258, 5: 273, 6: 289,
                   7:309,8: 330, 9: 350,10:371,11: 392, 12: 412,
                   13: 438}
    def calc_buff(self,data)->buff.Buff:
        b = buff.Buff()
        self.data = data['五郎']
        b.set(buff.both,"DEF_num",self.E_DEF_Magn[self.data['e天赋等级']])
        if self.data['是否至少三岩']:
            b.set(buff.both,'Rock_Dmg_Inc',0.15)
        b.set(buff.both,'DEF',0.25)
        if self.data['命座数']==6:
            if self.data['是否至少三岩']:
                b.set(buff.both,"Crit_dmg",0.4)
            else:
                b.set(buff.both,"Crit_dmg",0.2)
        return b
    
class YunJin(Person):
    @property
    def query(self):
        return [
        {
            'item':'防御力(入队满华馆)',
            'type':'int',
            'range':[1000,3000],
        },
        {
            'item':'命座数',
            'type':'int',
            'range':[0,6],
        },
        {
            'item':'q天赋等级',
            'type':'int',
            'range':[1,13],
        },
        {
            'item':'元素类型数目',
            'type':'int',
            'range':[1,3]
        }
    ]
    Q_basicDmgDEF_Magn = {1:0.32,2: 0.35, 3: 0.37, 4:0.40, 5: 0.43, 6: 0.45,
                   7:0.48,8: 0.51, 9: 0.55,10:0.58,11: 0.61, 12: 0.64,
                   13: 0.68}
    def calc_buff(self,data)->buff.Buff:
        b = buff.Buff()
        basic_DEF = 734
        self.data = data['云堇']
        total_DEF = self.data['防御力(入队满华馆)']
        basic_per_DEF = self.Q_basicDmgDEF_Magn[self.data['q天赋等级']] + 0.25*self.data['元素类型数目']

        if data.get('五郎'):
            total_DEF += 0.25*basic_DEF
        if self.data['命座数']>=2:
            b.set(buff.both,'Dmg_Inc',0.15)
        if self.data['命座数']>=4:
            total_DEF += 0.2*basic_DEF
        b.set(buff.both,"Dmg_Num_Inc_O",total_DEF*basic_per_DEF)
        return b

def get_buff(others = (0,1)):
    b = buff.Buff()
    for key,value in other_buff_list.items():
        if(value not in others)and(cache.get(key)):
            cache.pop(key) 
    for o_buff in others:
        b_add = buff.Buff()
        if other_buff_list['双岩'] == o_buff:
            b_add.set(buff.both,"Dmg_Inc",0.15)
            b_add.set(buff.both,"Rock_RES_Dec",0.2)

        elif other_buff_list['岩伤杯'] == o_buff:
            b_add.set(buff.both,"Rock_Dmg_Inc",0.466)

        elif other_buff_list['钟离'] == o_buff:
            b_add.set(buff.both,"Rock_RES_Dec",0.2)
            b_add.set(buff.both,"Phy_RES_Dec",0.2)

        elif other_buff_list['夜兰'] == o_buff:
            b_add.set(buff.on,"Dmg_Inc",0.50)
            b_add.set(buff.off,"Dmg_Inc",0.01)
        elif other_buff_list['五郎'] == o_buff:
            wl = WuLang()
            try:
                Query_for_other_person('五郎',cache,wl.query)
            except:
                return None
            b_add = wl.calc_buff(cache)
        elif other_buff_list['云堇'] == o_buff:
            yj = YunJin()
            try:
                Query_for_other_person('云堇',cache,yj.query)
            except:
                return None
            b_add = yj.calc_buff(cache)
        b += b_add
    return b

if __name__=='__main__':
    print(get_buff())
