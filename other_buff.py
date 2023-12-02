import buff,abc
from ui_further_query import Query_for_other_person
other_buff_list = {"双岩":0,"岩伤杯":1,"钟离":2,"夜兰":3,'五郎':4,'云堇':5,'芙宁娜':6}
cache = {}
class Person(abc.ABC):
    def __init__(self) -> None:
        pass
    @abc.abstractproperty
    def name(self):
        pass
    @property
    def id(self):
        return other_buff_list[self.name]
    @abc.abstractproperty
    def query(self):
        '''
        [
            {
                'item': what to ask for,the type should be 'str'\n
                'type': 'int' 'choose' or 'float', need to be string\n
                'range': [low,high] or dict[str,int] if the type is choose\n
            },
            ...
        ]
        '''
        pass
    @abc.abstractmethod
    def calc_buff(self,data)->buff.Buff:
        pass

class WuLang(Person):
    @property
    def name(self):
        return '五郎'
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
        self.data = data[self.name]
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
    def name(self):
        return '云堇'
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
        self.data = data[self.name]
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
    
class FuNingNa(Person):
    @property
    def name(self):
        return '芙宁娜'
    @property
    def query(self):
        return [
            {
                'item':'命座数',
                'type':'int',
                'range':[0,6]
            },
            {
                'item':'q天赋等级',
                'type':'int',
                'range':[1,13]
            }
        ]
    Q_Dmg_Inc_Magn = {1:0.07,2: 0.09, 3: 0.11, 4:0.13, 5: 0.15, 6: 0.17,
                   7:0.19,8: 0.21, 9: 0.23,10:0.25,11: 0.27, 12: 0.29,
                   13: 0.31}
    def calc_buff(self, data) -> buff.Buff:
        b = buff.Buff()
        self.data = data[self.name]
        if self.data['命座数']>=1:
            b.set(buff.off,'Dmg_Inc',self.Q_Dmg_Inc_Magn[self.data['q天赋等级']]*1.5)
            b.set(buff.on,'Dmg_Inc',self.Q_Dmg_Inc_Magn[self.data['q天赋等级']]*4)
        else:
            b.set(buff.on,'Dmg_Inc',self.Q_Dmg_Inc_Magn[self.data['q天赋等级']]*3)
        return b
    
person_register = {}
for subclass in Person.__subclasses__():
    person_register[subclass().id] = subclass
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
        else:#get subclass of Person
            person:Person = person_register[o_buff]()
            try:
                Query_for_other_person(person.name,cache,person.query)
            except:
                return None
            b_add = person.calc_buff(cache)
        b += b_add
    return b

if __name__=='__main__':
    print(get_buff())
