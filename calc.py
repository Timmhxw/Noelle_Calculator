import buff
def DEF_RES(basic_RES,RES_Dec = 0,enemy = 93,player = 90):
    "防御抗性乘区计算"
    RES = basic_RES - RES_Dec
    if(RES<=0):
        return (100.0+player)/(200.0+enemy+player)*(1-RES/2)
    elif(0<RES<=0.75):
        return (100.0+player)/(200.0+enemy+player)*(1-RES)
    else:
        return (100.0+player)/(200.0+enemy+player)*1.0/(1+RES*4)
        
def calc(data,b:buff.Buff,A_Magn,DEF2ATK):

    calc_hit = {buff.on:{},buff.off:{}}#每刀伤害
    total_calc_ATK = {buff.on:0,buff.off:0}#开大攻击力
    calc_expect = {buff.on:0,buff.off:0}#伤害期望
    
    for st in buff.status_list:
        calc_DEF = data["DEF"]+b.get(st,"DEF")*data["basic_DEF"]+b.get(st,"DEF_num")
        calc_ATK = data["ATK"]+b.get(st,"ATK")*data["basic_ATK"]+calc_DEF*DEF2ATK+b.get(st,"ATK_num")
        total_calc_ATK[st] = calc_ATK

        multi_second = data["Crit_dmg"]+ b.get(st,"Crit_dmg") +1#双爆乘区
        multi_third = b.get(st,"Dmg_Inc")+b.get(st,"Rock_Dmg_Inc")+1#增伤乘区
        multi_fourth = DEF_RES(0.1,b.get(st,"Rock_RES_Dec"))#防御抗性乘区，岩抗10%，双岩减岩抗20%
        
        for k,v in A_Magn.items():
            multi_first = v * calc_ATK + b.get(st,"Dmg_Num_Inc_A")*calc_ATK + b.get(st,"Dmg_Num_Inc_D")*calc_DEF + b.get(st,"Dmg_Num_Inc_O")#基础伤害乘区
            
            hit = multi_first * multi_second * multi_third * multi_fourth
            if b.get(st,"Other_Dmg"):
                hit_add = b.get(st,"Other_Dmg") * calc_ATK * multi_second * (b.get(st,"Dmg_Inc")+1)*  DEF_RES(0.3,b.get(st,"Phy_RES_Dec"))#物抗30%
                hit = hit + hit_add
            calc_hit[st][k] = hit
        expect = multi_first * (min((data["Crit_rate"]+b.get(st,"Crit_rate")),1)*(data["Crit_dmg"]+ b.get(st,"Crit_dmg") )+1)*multi_third*multi_fourth
        if b.get(st,"Other_Dmg"):
            expect_add = b.get(st,"Other_Dmg") * calc_ATK * ((data["Crit_rate"]+b.get(st,"Crit_rate"))*data["Crit_dmg"]+1) * (b.get(st,"Dmg_Inc")+1)* DEF_RES(0.3,b.get(st,"Phy_RES_Dec"))#物抗30%
            expect = expect + expect_add
        calc_expect[st] = expect
    return calc_hit,total_calc_ATK,calc_expect

if __name__=='__main__':
    data = {'ATK': 1309, 'DEF': 2011, 'Noelle_num': 6,
                'A_Magn': 10, 'Q_Magn': 13, 'Crit_rate': 0.591, 'Crit_dmg': 2.587,
                'Weapon': 1, 'Weapon_num': 2, 'Relic': 1,'basic_ATK':733,'basic_DEF':799}
    b = buff.Buff()
    b.set(buff.on,"Rock_RES_Dec",0.2)
    b.set(buff.off,"Rock_RES_Dec",0.2)
    A_Magn = {1:1,2:1.1,3:1.2,4:1.3}
    DEF2ATK = 1.35
    print(calc(data,b,A_Magn,DEF2ATK))
    
