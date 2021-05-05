# type definitions
Symbol = str
Number = (int, float)
Atom = (Symbol, Number)
List = list
Expression = (Atom, List)
Env = dict

class Procedure(object):

	def __init__(self, params, body, myenv):
		self.params, self.body, self.myenv = params, body, myenv
	def __call__(self, *args):
		newenv = self.myenv
		for param, arg in zip(self.params, args):
			newenv[param] = arg
		return eval(self.body, newenv)


def tokenize(program):
	# insert spaces around each paranthesis so that split works the way we want it to.
	return program.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(tokens):
	i = 0
	if tokens.count('(') != tokens.count(')'):
		raise ValueError('Parantheses issue.')

	def inner():
		nonlocal i
		if tokens[i] == '(':
			i += 1
			mylist = []
			while i < len(tokens):
				if tokens[i] == ')':
					return mylist
				else:
					mylist += [inner()]
					i += 1
		else: 
			return atom(tokens[i])
	return inner()

def atom(token: str):
	try:
		return int(token)
	except ValueError:
		try:
			return float(token)
		except ValueError:
			return Symbol(token)

def standard_env():
	import operator as op
	myenv = Env()

	# arithmetic operators
	myenv.update({
		'+': op.add,
		'*': op.mul,
		'-': op.sub,
		'/': op.truediv, # floating point division
		'%': op.mod,
	})

	# comparison operators
	myenv.update({ #DOUBT guile displays True as #t
		'=': op.eq,
		'<': op.lt,
		'>': op.gt,
		'<=': op.le,
		'>=': op.ge,
	})

	myenv.update({
		'max': max,
		'min': min,
		'round': round,
		'expt': pow,
	})

	myenv.update({
		'list': lambda *elements: List(elements),
		'car': lambda alist: alist[0], # first element of a list
		'cdr': lambda alist: alist[1:], # list except first element
		'cons': lambda ele, alist: list(ele) + alist, # return a list whose car is ele and cdr is alist
		'print': print,

	})

	myenv.update({
		'equal?': op.eq,
		'list?': lambda expr: isinstance(expr, List),
		'null?': lambda expr: expr == [],
		'number?': lambda expr: isinstance(expr, Number),
		'procedure?': callable,
		'symbol?': lambda expr: isinstance(expr, Symbol),
	})

	return myenv

def eval(expr, myenv):

	# isinstance takes in a class or a tuple
	# constant literal number
	if isinstance(expr, Number):
		# print("here 1")
		return expr

	# variable reference
	elif isinstance(expr, Symbol):
		# print("here 2")
		return myenv[expr]

	# if else conditional
	elif expr[0] == 'if':
		_, condition, if_block, else_block = expr
		if eval(condition, myenv):
			return eval(if_block, myenv)
		else:
			return eval(else_block, myenv)

	# defining a variable
	elif expr[0] == 'define': 
		# print("here 3")
		try:
			_, symbol, expr = expr
		except:
			raise ValueError('Invalid syntax for define.')
		myenv[symbol] = eval(expr, myenv)
		return

	# defining a function
	elif expr[0] == 'lambda':
		_, params, body = expr
		return Procedure(params, body, myenv)

	# procedure call
	else:
		# print("here 4")
		proc = eval(expr[0], myenv)
		args = [eval(i, myenv) for i in expr[1:]]
		return proc(*args)

if __name__ == '__main__':
	
	myenv = standard_env()
	fullinput = """(+ 4 5) 
(define vari (- 8 2))
(if (= vari 6) (* vari 10) 0)
(if (= vari 5) (* vari 10) 0)
(if vari (* vari 10) 0)
(list 8 3 2)
(define myl (list 8 2 4 8))
(car myl)
(cdr myl)
(max 8 9 3)
(max (list 8 9 3))
(round 8.5)
(round 9.5)
(define square (lambda x (* x x)))
(define area_circle (lambda r (* (* r r) 3.14)))
(square 5)
(area_circle 7)
"""

	definite_errors = """(list (99 90)
(car (8 7 3))
(define square x (* x x))
"""

	for minput in fullinput.splitlines():
		step1 = tokenize(minput)
		step2 = parse(step1)
		step3 = eval(step2, myenv)
		print(minput, "| Ans", step3)

