
import plex

class ParseError(Exception):
	pass

class ParseRun(Exception):
	pass

class MyParser:
	def __init__(self):
		space = plex.Any(" \n\t")
		schar = plex.Str('(',')')
		letter = plex.Range('azAZ')
		digit = plex.Range('09')
		bit = plex.Range('01')
		bits = plex.Rep1(bit)
		name = letter+plex.Rep(letter|digit)
		keyword = plex.Str('print','PRINT')
		operator=plex.Str('AND','OR','XOR','=')
		self.st = {}
		self.lexicon = plex.Lexicon([
			(operator,plex.TEXT),
			(keyword,'PRINT'),
			(schar,plex.TEXT),
			(name,'IDENTIFIER'),
			(bits, 'bit_token'),
			(space,plex.IGNORE)
			])

	def create_scanner(self,fp):
		self.scanner = plex.Scanner(self.lexicon,fp)
		self.la,self.text=self.next_token()

	def next_token(self):
		return self.scanner.read()

	def match(self,token):
		if self.la==token:
			self.la,self.text=self.next_token()
		else:
			raise ParseError("need (")

	def parse(self,fp):
		self.create_scanner(fp)
		self.stmt_list()
		
	def stmt_list(self):
		if self.la=='IDENTIFIER' or self.la=='PRINT':
			self.stmt()
			self.stmt_list()
		elif self.la==None:
			return
		else:
			raise ParseError("need IDENTIFIER or Print")
	def stmt(self):
		if self.la=='IDENTIFIER':
			varname= self.text
			self.match('IDENTIFIER')
			self.match('=')
			e=self.expr()
			self.st[varname]= e
		elif self.la=='PRINT':
			self.match('PRINT')
			e=self.expr()
			print('{:b}'.format(e))
		else:
			raise ParseError("need IDENTIFIER or PRINT")
	def expr(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='bit_token':	
			i=self.term()
			while self.la == 'XOR':
				self.match ('XOR')
				t = self.term()
				i ^= t
			if self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la == ')':
				return i
			else:
				raise ParseError ('need XOR')
			
		else:
			raise ParseError("need ( or IDENTIFIER or bit_token or )")
	
	def term(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='bit_token':	
			i = self.factor()
			while self.la == 'OR':
				self.match ('OR')
				t = self.factor()
				i |= t
			if self.la == 'XOR' or self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la == ')':
				return i 
			else:
				raise ParseError ('need OR')
			
		else:
			raise ParseError("need ( or IDENTIFIER or bit_token or )")
	def factor(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='bit_token':	
			i=self.atom()
			while self.la == 'AND':
				self.match ('AND')
				t = self.atom()
				i &= t
			if self.la == 'XOR' or self.la == 'OR' or self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la == ')':
				return i 
			else:
				raise ParseError ('need bit_token')
			
		else:
			raise ParseError("need ( or IDENTIFIER or bit_token or )")
	
	def atom(self):
		if self.la=='(':
			self.match('(')
			e=self.expr()
			self.match(')')
			return e
		elif self.la=='IDENTIFIER':
			varname = self.text
			self.match('IDENTIFIER')
			if varname in self.st:
				return self.st[varname]
			raise ParseRun("need id ")
		elif self.la=='bit_token':
			value=int(self.text,2)
			self.match('bit_token')
			return value
		else:
			raise ParseError("need id of bit_token or (")
	
parser = MyParser()
with open('askhsh2.txt','r') as fp:
	parser.parse(fp)

