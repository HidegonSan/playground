print("".join([i if i in ("。", "、", "ー", "！", "？") else chr(ord(i) + 0x60) for i in input("平仮名→片仮名 >> ")])) 
