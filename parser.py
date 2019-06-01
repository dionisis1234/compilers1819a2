import plex

class ParseError(Exception):
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
		self.lexicon = plex.Lexicon([
			(operator,plex.TEXT),
			(keyword,'PRINT'),
			(schar,plex.TEXT),
			(name,'IDENTIFIER'),
			(space,plex.IGNORE),
			(bits,'bit_token')
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
			raise ParseError("perimenw ")

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
			raise ParseError("perimenw IDENTIFIER or Print")
	def stmt(self):
		if self.la=='IDENTIFIER':
			self.match('IDENTIFIER')
			self.match('=')
			self.expr()
		elif self.la=='PRINT':
			self.match('PRINT')
			self.expr()
		else:
			raise ParseError("perimenw IDENTIFIER or PRINT")
	def expr(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='bit_token':	
			self.term()
			self.term_tail()
		else:
			raise ParseError("perimenw ( or IDENTIFIER or bit_token or )")
	def term_tail(self):
		if self.la=='XOR':
			self.match('XOR')
			self.term()
			self.term_tail()
		elif self.la=='IDENTIFIER' or self.la=='PRINT' or self.la== None or self.la==')':
			return
		else:
			raise ParseError("perimenw XOR")
	def term(self):
		if self.la=='(' or self.la=='IDENTIFIER' or self.la=='bit_token':	
			self.factor()
			self.factor_tail()
		else:
			raise ParseError("perimenw ( or IDENTIFIER or  )")
	def factor_tail(self):
		if self.la=='OR':
			self.match('OR')
			self.factor()
			self.factor_tail()
		elif self.la=='XOR' or self.la=='IDENTIFIER' or self.la=='PRINT' or self.la== None or self.la==')':
			return
		else:
			raise ParseError("perimenw OR ")
	def factor(self):
		if self.la=='(' or self.la == 'IDENTIFIER' or self.la == 'bit_token':
			self.atom()
			self.atom_tail()
		else:
			raise ParseError("perimenw id bit_token ")
	def atom_tail(self):
		if self.la=='AND':
			self.match('AND)
			self.atom()
			self.atom_tail()
		elif self.la == 'XOR' or self.la == 'OR' or self.la == 'IDENTIFIER' or self.la == 'PRINT' or self.la == None or self.la == ')':
			return
		else:
			raise ParseError("perimenw AND")
	def atom(self):
		if self.la == '(':
			self.match('(')
			self.expr()
			self.match(')')
		elif self.la == 'IDENTIFIER':
			self.match('IDENTIFIER')
		elif self.la == 'bit_token':
			self.match('bit_token')
		else:
			raise ParseError("perimenw  bit_token")

parser = MyParser()
with open('askhsh2.txt','r') as fp:
	parser.parse(fp)
