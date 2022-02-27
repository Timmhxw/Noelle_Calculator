import buff
other_buff_list = {"双岩","岩伤杯"}

def get_buff(others = (0,1)):
    b = buff.Buff()
    for o_buff in others:
        b_add = buff.Buff()
        if o_buff == 0:
            b_add.set_buff(buff.on,"Dmg_Inc",0.15)
            b_add.set_buff(buff.off,"Dmg_Inc",0.15)
        elif o_buff == 1:
            b_add.set_buff(buff.on,"Rock_Dmg_Inc",0.466)
            b_add.set_buff(buff.off,"Rock_Dmg_Inc",0.466)
        b += b_add
    return b

if __name__=='__main__':
    print(get_buff())
