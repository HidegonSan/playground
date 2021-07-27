try:
	from forbiddenfruit import curse
except:
	__import__("os").system("pip install forbiddenfruit")

def replaceAll(self, replaceDict):
	ret = [self]
	[ret.append(ret.pop().replace(i, j)) for i, j in replaceDict.items()]
	return ret[0]

curse(str, "replaceAll", replaceAll)


# abCDEFGhIJKLMN
print("ABCDEFGHIJKLMN".replaceAll({"A": "a", "B": "b", "H": "h"})) 
