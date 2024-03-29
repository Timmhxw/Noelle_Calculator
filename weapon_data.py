import buff

weapons_list = {'赤角':1,'螭骨':2, '天空':3, '白影':4, '无工':5, '狼末':6, '黑岩':7,'西风':8}
basic_ATK = {1:542,2:510,3:674,4:510,5:608,6:608,7:510,8:510}

#攻击
ATK_wugong_on = {1:0.4,2: 0.5, 3: 0.6, 4: 0.7, 5: 0.8}
ATK_wugong_off = {1:0.2,2: 0.25, 3: 0.3, 4: 0.35, 5: 0.4}
ATK_langmo_on = {1:0.4,2: 0.5, 3: 0.6, 4: 0.7, 5: 0.8}
ATK_heiyan_on = {1:0.36,2:0.45,3: 0.54,4:0.63, 5: 0.72}
ATK_baiying_on = {1:0.24,2: 0.30,3: 0.36, 4: 0.42, 5: 0.48}

#防御
DEF_baiying_on = {1:0.24,2: 0.30, 3: 0.36, 4: 0.42, 5: 0.48}

#伤害加成
Dmg_Inc_chigu_on = {1:0.3,2: 0.35, 3: 0.4, 4: 0.45, 5: 0.5}
Dmg_Inc_tiankong_on = {1:0.08,2: 0.1, 3: 0.12, 4: 0.14, 5: 0.16}

#伤害数值加成
Dmg_Num_Inc_D_chijiao = {1:0.4,2: 0.5, 3: 0.6, 4: 0.7, 5: 0.8}


#额外伤害
Other_Dmg_tiankong_on = {1:0.8,2: 1, 3: 1.2, 4: 1.4, 5: 1.6}

def get_buff(Weapon,Weapon_num:int):
    b = buff.Buff()
    if Weapon == weapons_list['赤角']:
        b.set(buff.on,"Dmg_Num_Inc_D",Dmg_Num_Inc_D_chijiao[Weapon_num])
        b.set(buff.off,"Dmg_Num_Inc_D",Dmg_Num_Inc_D_chijiao[Weapon_num])
    elif Weapon == weapons_list['螭骨']:
        b.set(buff.on,"Dmg_Inc", Dmg_Inc_chigu_on[Weapon_num])
    elif Weapon == weapons_list['天空']:
        b.set(buff.on,"Dmg_Inc", Dmg_Inc_tiankong_on[Weapon_num])
        b.set(buff.on,"Other_Dmg", Other_Dmg_tiankong_on[Weapon_num])
    elif Weapon == weapons_list['白影']:
        b.set(buff.on,"ATK" , ATK_baiying_on[Weapon_num])
        b.set(buff.on,"DEF" , DEF_baiying_on[Weapon_num])
    elif Weapon == weapons_list['无工']:
        b.set(buff.on,"ATK" , ATK_wugong_on[Weapon_num])
        b.set(buff.off,"ATK" , ATK_wugong_off[Weapon_num])
    elif Weapon == weapons_list['狼末']:
        b.set(buff.on,"ATK" , ATK_langmo_on[Weapon_num])
    elif Weapon == weapons_list['黑岩']:
        b.set(buff.on,"ATK" , ATK_heiyan_on[Weapon_num])
    elif Weapon == weapons_list['西风']:
        pass
    return b

if __name__ == '__main__':
    for k,v in weapons_list.items():
        print('buff of',k,'is:\n',get_buff(v,1))
    
