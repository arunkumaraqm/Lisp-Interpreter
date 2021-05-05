from interpreter import *

import sys

def repl():
	myenv = standard_env()
	while True:
		minput = input("scheme >>> ")
		if minput == 'exit':
			break
		step1 = tokenize(minput)
		try: step2 = parse(step1)
		except ValueError as e: 
			print('ERROR', str(e))
			continue
		try: 
			step3 = eval(step2, myenv)
			print(step3)
		except Exception as e:
			print('ERROR', 'Semantic error.')
			continue
if __name__ == '__main__':
	repl()