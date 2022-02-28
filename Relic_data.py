import buff
Relics_list = {1:'角斗士',2: '逆飞', 3: '华馆'}
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
    return b

if __name__=='__main__':
    for k,v in Relics_list.items():
        print("the buff of",v,"is:\n",get_buff(k))

