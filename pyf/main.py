print("exec("+"+".join(["chr("+("1+"*ord(i))[:-1]+")" for i in input(">> ")])+")")
