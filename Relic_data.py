import buff
Relics_list = {'角斗士':1,'逆飞':2, '华馆':3, '华馆（防御面板已叠满）':4,'猎人':5}
def get_buff(Relic:int):
    b = buff.Buff()
    if Relic == 1:
        b.set(buff.on,"Dmg_Inc",0.35)
        b.set(buff.off,"Dmg_Inc",0.35)
    elif Relic == 2:
        b.set(buff.on,"Dmg_Inc",0.4)
        b.set(buff.off,"Dmg_Inc",0.4)
    elif Relic == 3:
        b.set(buff.on,"Rock_Dmg_Inc",0.24)
        b.set(buff.on,"DEF",0.24)
    elif Relic == 4:
        b.set(buff.on,"Rock_Dmg_Inc",0.24)
        b.set(buff.off,"DEF",-0.24)
    elif Relic == 5:
        b.set(buff.on,"Dmg_Inc",0.15)
        b.set(buff.on,"Crit_rate",0.36)
        b.set(buff.off,"Dmg_Inc",0.15)
    return b

if __name__=='__main__':
    for k,v in Relics_list.items():
        print("the buff of",k,"is:\n",get_buff(v))

