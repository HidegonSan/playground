"""
import inspect
import os

def alert():
	frame = inspect.currentframe().f_back
	print(f"\n\nFILE : {os.path.basename(frame.f_code.co_filename)}\nFUNC : {frame.f_code.co_name}\nLINE : {frame.f_lineno}\n\n")
"""

class Tokenize(object):

	def __init__(self, src):
		self.src = src
		self.srcLen = len(src)
		self.pos = 0
		self.ret = []
		self.cur = ""
		self.tokens = [
			"...",
			">>=",
			"<<=",
			"<=>",
			"->",
			"<-",
			">=",
			"<=",
			">>",
			"<<",
			"==",
			"!=",
			"+=",
			"-=",
			"*=",
			"/=",
			"%=",
			"&=",
			"&&",
			"|=",
			"[]",
			"::",
			"!",
			"=",
			".",
			",",
			"?",
			">",
			"<",
			"!",
			"%",
			"&",
			"^",
			"|",
			"(",
			")",
			"[",
			"]",
			"{",
			"}",
			";",
			":",
			"+",
			"-",
			"*",
			"/",
			"@",
			"#",
		]

	def addTemp(self, string):
		self.cur = self.cur + string

	def addRet(self):
		self.ret.append(self.cur)
		self.cur = ""

	def getNow(self):
		return self.src[self.pos]

	def check(self):
		return self.pos < self.srcLen

	def next(self):
		self.pos += 1

	def match(self, string):
		strlen = len(string)
		return self.pos + strlen <= self.srcLen and self.src[self.pos:self.pos + strlen] == string

	def passSpace(self):
		while self.check() and ord(self.getNow()) <= ord(" "):
			self.next()


	def Tokenize(self):

		while (self.check()):
			ch = self.getNow()
			pos2 = self.pos

			# num
			if ch.isdigit():
				while self.check():
					ch = self.getNow()
					if not ch.isdigit() and ch != ".":
						break
					self.addTemp(ch)
					self.next()
				self.addRet()

			# identifier
			elif ch.isalpha() or ch == "_":
				while self.check():
					ch = self.getNow()
					if not ch.isalnum():
						if ch != "_":
							break
					self.addTemp(ch)
					self.next()
				self.addRet()

			# string
			elif ch == '"' or ch == "'":
				self.next()
				while self.check():
					ch = self.getNow()
					if ch == '"' or ch == "'":
						break
					self.addTemp(ch)
					self.next()
				self.addRet()
				self.next()

			# reserved
			else:
				for t in self.tokens:
					if self.match(t):
						self.addTemp(t)
						self.addRet()
						self.pos += len(t)


			self.passSpace()
		return self.ret






SOURCE = """
1 + 2 * 3 + 4

if aaa {
			print("Good morning.");
}
else {
			operator<<(std::cout, "???");
}

auto&& a = my_func();

#include <iostream>
#include <string>

@ @ @
"""


tokenizeInstance = Tokenize(SOURCE)
tokens = tokenizeInstance.Tokenize()

for token in tokens:
	print(token)
