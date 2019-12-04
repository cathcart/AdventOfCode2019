import unittest
from functools import reduce

class Examples(unittest.TestCase):

    def run(self):
        self.assertEqual(runComp([1,0,0,0,99])[0], 2)
        self.assertEqual(runComp([2,3,0,3,99])[3], 6)
        self.assertEqual(runComp([2,4,4,5,99,0])[-1], 9801)
        self.assertEqual(runComp([1,1,1,4,99,5,6,0,99])[0], 30)

def get_input(input_file):
	return [int(x) for x in open(input_file).read().strip().split(",")]

def arg1_idx(idx):
	return idx + 1
def arg2_idx(idx):
	return idx + 2
def out_idx(idx):
	return idx + 3

def func(idx, inputs):
	
	cmds = {1:(lambda x,y:  x+y), 2: (lambda x,y: x*y)}

	c = inputs[idx]
	a = inputs[arg1_idx(idx)]
	A = inputs[a]
	b = inputs[arg2_idx(idx)]
	B = inputs[b]
	o = inputs[out_idx(idx)]

	inputs[o] = cmds[c](A,B)


def runComp(myinput):

	idx = 0 

	while(1):

		cmd = myinput[idx]
		if (cmd == 99):
			break
		
		func(idx, myinput)

		idx += 4

	return myinput

def noun_verb(noun, verb):
	inputs = get_input("input.txt")

	inputs[1] = noun
	inputs[2] = verb

	runComp(inputs)

	return inputs[0]

if __name__ == "__main__":
	Examples().run()

	print(noun_verb(12, 2))


	for noun in range(0, 100):
		for verb in range(0,100):
			if noun_verb(noun, verb) == 19690720:
				print(100*noun + verb)

