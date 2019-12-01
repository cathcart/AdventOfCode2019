import unittest
from functools import reduce

class Examples(unittest.TestCase):

    def run(self):
        self.assertEqual(fuel(12), 2)
        self.assertEqual(fuel(14), 2)
        self.assertEqual(fuel(1969), 654)
        self.assertEqual(fuel(100756), 33583)

    def run2(self):
        self.assertEqual(fuel2(14), 2)
        self.assertEqual(fuel2(1969), 966)
        self.assertEqual(fuel2(100756), 50346)

def get_input(input_file):
	return [int(x) for x in open(input_file).read().strip().split("\n")]

def fuel(mass):
	return ((mass//3) - 2)

def fuel_fuel(fuel_mass):
	#ammount of fuel the fuel needs
	f = fuel(fuel_mass)
	if (f <= 0 ):
		return 0
	else:
		return f + fuel_fuel(f)

def fuel2(mass):
	f = fuel(mass)
	return f + fuel_fuel(f)

if __name__ == "__main__":
	inputs = get_input("input.txt")
	print(len(inputs))
	#print(inputs)

	Examples().run()

	#function, sequence, start
	print("part1")
	print(reduce(lambda x,y: fuel(y) + x, inputs, 0))
	#print(sum([fuel(x) for x in inputs]))


	Examples().run2()

	#function, sequence, start
	print("part2")
	print(reduce(lambda x,y: fuel2(y) + x, inputs, 0))
