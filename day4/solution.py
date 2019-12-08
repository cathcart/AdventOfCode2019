import unittest
from functools import reduce


def accending(inputStr, desiredLen):
	if (len(inputStr) == desiredLen):
		return [inputStr]

	else:
		results = []
		
		n = int(inputStr[-1])

		for x in range(n, 10):
			results += accending(inputStr+str(x), desiredLen)
		return results


def checkDoubles(inputStr):
	if (len(inputStr) == len(set(inputStr))):
		return False

	for x in set(inputStr):
		if(inputStr.count(x) > 1):
			idx = inputStr.index(x)

			if(idx > 0):
				if(inputStr[idx - 1] == x):
					return True
			if(idx < len(inputStr) - 1):
				if(inputStr[idx + 1] == x):
					return True
	return False

def checkDoubles2(inputStr):
	if (len(inputStr) == len(set(inputStr))):
		return False

	results = [False]
	for x in set(inputStr):
		if(inputStr.count(x) == 2):
			idx = inputStr.index(x)

			if(idx > 0):
				if(inputStr[idx - 1] == x):
					results.append(True)
			if(idx < len(inputStr) - 1):
				if(inputStr[idx + 1] == x):
					results.append(True)

	return reduce(lambda x, y: x or y, results)


class TestAccending(unittest.TestCase):
	def run(self):

		self.assertEqual(accending("1", 1), ["1"])
		self.assertEqual(accending("9", 2), ["99"])
		self.assertEqual(accending("8", 2), ["88", "89"])
		self.assertEqual(accending("8", 3), ["888", "889", "899"])

class TestDoubles(unittest.TestCase):
	def run(self):
		self.assertEqual(checkDoubles("123789"), False)
		self.assertEqual(checkDoubles("111111"), True)
		self.assertEqual(checkDoubles("121212"), False)
		self.assertEqual(checkDoubles("223450"), True)
		
		self.assertEqual(checkDoubles2("123789"), False)
		self.assertEqual(checkDoubles2("111111"), False)
		self.assertEqual(checkDoubles2("121212"), False)
		self.assertEqual(checkDoubles2("223450"), True)
		self.assertEqual(checkDoubles2("112233"), True)
		self.assertEqual(checkDoubles2("123444"), False)
		self.assertEqual(checkDoubles2("111122"), True)

def get_input(input_file):
	return open(input_file).read().strip().split("\n")
	#return [int(x) for x in open(input_file).read().strip().split(",")]


if __name__ == "__main__":
	TestAccending().run()
	TestDoubles().run()

	range_min = 382345
	range_max = 843167
	count1 = 0
	count2 = 0

	for n in range(3, 9):
		for x in accending(str(n), 6):

			if (int(x) >= range_min and int(x) <= range_max):
				if checkDoubles(x):
					count1 += 1
				if checkDoubles2(x):
					count2 += 1

	print("part 1: ", count1)
	print("part 2: ", count2)



	

