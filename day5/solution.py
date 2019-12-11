import unittest
from functools import reduce

class Examples(unittest.TestCase):

	def run(self):
		C = Computer([1,0,0,0,99])
		C.start()
		self.assertEqual(C.tape[0], 2)

		C = Computer([2,3,0,3,99])
		C.start()
		self.assertEqual(C.tape[3], 6)

		C = Computer([2,4,4,5,99,0])
		C.start()
		self.assertEqual(C.tape[-1], 9801)

		C = Computer([1,1,1,4,99,5,6,0,99])
		C.start()
		self.assertEqual(C.tape[0], 30)

		C = Computer([1002,4,3,4,33])
		C.start()
		self.assertEqual(C.tape[-1], 99)



	def test(self):
		ins = [32198]
		C = Computer(ins)
		[opcode, params] = C.opCodeDecoder(ins[0])

		self.assertEqual(opcode, "98")
		self.assertEqual(params, "123")

def get_input(input_file):
	return [int(x) for x in open(input_file).read().strip().split(",")]


class Computer():
	def __init__(self, tape):
		self.tape = tape
		self.PC = 0 #program counter
		self.run = True

		self.codes = {"01":self.add, "02":self.mul, "03":self.getUserInput, "04":self.printToUser, "05":self.jmpIfTrue, "06":self.jmpIfFalse, "07":self.lessThan, "08":self.equals, "99":self.halt}

	def comparison2(self, func, params):
		A = self.get_value(1, params[0])
		B = self.get_value(2, params[1])

		if (func(A, B)):
			self.PC = B
		else:
			self.PC += 3

	def jmpIfTrue(self, params):
		func = lambda x, y: x != 0
		self.comparison2(func, params)

	def jmpIfFalse(self, params):
		func = lambda x, y: x == 0
		self.comparison2(func, params)

	def comparison3(self, func, params):
		A = self.get_value(1, params[0])
		B = self.get_value(2, params[1])
		C = self.get_value(3, "1")
		#print("hi", self.PC, A, B, C)

		if (func(A, B)):
			self.tape[C] = 1
		else:
			self.tape[C] = 0

		self.PC += 4

	def lessThan(self, params):
		func = lambda x, y: x < y
		self.comparison3(func, params)
	
	def equals(self, params):
		func = lambda x, y: x == y
		self.comparison3(func, params)

	def halt(self, params):
		self.run = False

	def start(self):
		while self.run:
			ins = self.tape[self.PC]
			[opcode, params] = self.opCodeDecoder(ins)
			self.codes[opcode](params)
			#print(self.PC, self.tape)

	def getUserInput(self, params):
		value = input()
		idx = self.get_value(1, "1")
		self.tape[idx] = int(value)

		self.PC += 2

	def printToUser(self, params):
		print(self.get_value(1, params[0]))

		self.PC += 2
	
	def add(self, params):
		func = lambda x, y: x + y
		self.twoValues(func, params)
	
	def mul(self, params):
		func = lambda x, y: x * y
		self.twoValues(func, params)

	def twoValues(self, func, params):

		output_idx = self.get_value(3, "1")
		A = self.get_value(1, params[0])
		B = self.get_value(2, params[1])

		self.tape[output_idx] = func(A, B)

		self.PC += 4

	def get_value(self, offset, param):
		x = self.tape[self.PC + offset]
	
		if(param == "1"): #immediate mode
			return x
		else: # position mode
			return self.tape[x]

	def opCodeDecoder(self, inputIns):
		ins = str.zfill(str(inputIns), 5)

		opcode = ins[-2:]
		params = ''.join(reversed(ins[:-2]))

		return [opcode, params]


def noun_verb(noun, verb):
	inputs = get_input("input.txt")

	#inputs[1] = noun
	#inputs[2] = verb

	C = Computer(inputs)
	C.start()

	#return C.tape[0]

if __name__ == "__main__":
	#Examples().run()
	#Examples().test()

	#C = Computer([3,0,4,0,99])
	#C.start()	

	#C = Computer([3,9,8,9,10,9,4,9,99,-1,8])
	#C = Computer([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])
	#C.start()
		

	noun_verb(12, 2)


#	for noun in range(0, 100):
#		for verb in range(0,100):
#			if noun_verb(noun, verb) == 19690720:
#				print(100*noun + verb)
#				break
