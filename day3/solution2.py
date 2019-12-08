import collections
import unittest
from functools import reduce

'''
#start at 0,0

+x move right -> addCol
-x move left -> prependCol
+y move down -> addRow
-y move up -> prependRow

'''
Pos = collections.namedtuple('Pos', 'x y')
PanelLimits = collections.namedtuple('PanelLimits', 'U D L R')

class Matrix():

	#define a zeroed square matrix of size NxN
	def __init__(self, N):

		self.center = Pos(x=N//2, y=N//2)
		self.__N = N
		self.__matrix = [[0 for x in range(N)] for y in range(N)] 
		#self.__setitem__(self.center, "O") 

	def add(self):
		newMatrix = Matrix(self.__N + 2)

		for j,y in enumerate(self.__matrix):
			for i,x	in enumerate(y):
				newMatrix.__matrix[j+1][i+1] = x

		return newMatrix

	def addRow(self):
		self.__matrix.append([0 for x in range(self.__N)])
		self.__N += 1

	def prependRow(self):
		self.__matrix = [[0 for x in range(self.__N)]] + self.__matrix
		self.center = Pos(x=self.center.x, y=self.center.y - 1)
		self.__N += 1

	def addColumn(self):
		for x in self.__matrix:
			x.append(0)
		self.__N += 1

	def prependColumn(self):
		for i,x in enumerate(self.__matrix):
			self.get()[i] = [0] + self.get()[i] 
		self.center = Pos(x=self.center.x+1, y=self.center.y)
		self.__N += 1

	def get(self):
		return self.__matrix

	def pos2Idx(self, pos):
		return Pos(x=pos.x + self.center.x, y=pos.y + self.center.y)

	def __setitem__(self, position, value):
		idx = self.pos2Idx(position)
		self.get()[idx.y][idx.x] = value

	def __getitem__(self, position):
		idx = self.pos2Idx(position)
		return self.get()[idx.y][idx.x] 


class TestMatrix(unittest.TestCase):
	def run(self):

		self.assertEqual(Matrix(1).get(), [["O"]])
		self.assertEqual(Matrix(2).get(), [[0, 0], [0, 0]])

		A = Matrix(1)
		A.addRow()
		self.assertEqual(A.get(), [[0], [0]])

		A = Matrix(1)
		A.get()[0][0] = 1
		A.prependRow()
		self.assertEqual(A.get(), [[0], [1]])

		A = Matrix(1)
		A.addColumn()
		self.assertEqual(A.get(), [[0,0]])

		A = Matrix(1)
		A.get()[0][0] = 1
		A.prependColumn()
		self.assertEqual(A.get(), [[0,1]])

class Panel():

	def __init__(self, N=1):
		self.map = Matrix(N)
		self.position = Pos(x=0, y=0)
		self.max = 0 #PanelLimits(U=0,D=0, L=0, R=0)

		self.wire = 0
		self.visited = {}
		self.timings = {}
		self.time = 0
		self.crosses = []

	def checkAndMark(self):
		if self.map[self.position] == 0:
			self.map[self.position] = self.wire

		elif self.map[self.position] != self.wire:
			self.crosses.append(self.position)
			self.map[self.position] = self.wire

	def checkAndUpdate(self):
		if ((abs(self.position.x) > self.max) or (abs(self.position.y) > self.max)):
			self.map = self.map.add()
			self.max += 1

	def addPosition(self):
		self.visited[self.wire].append(self.position)
		self.timings[self.wire].append(self.time)

	def moveLeft(self):
		self.position = Pos(x=self.position.x - 1, y=self.position.y)
		self.addPosition()

	def moveRight(self):
		self.position = Pos(x=self.position.x + 1, y=self.position.y)
		self.addPosition()
		
	def moveUp(self):
		self.position = Pos(x=self.position.x, y=self.position.y + 1)
		self.addPosition()

	def moveDown(self):
		self.position = Pos(x=self.position.x, y=self.position.y - 1)
		self.addPosition()


	def move(self, cmd):

		direction = cmd[0]
		magnitude = int(cmd[1:])

		for i in range(magnitude):
			self.time += 1
			if (direction == "U"):
				self.moveUp()
			if (direction == "D"):
				self.moveDown()
			if (direction == "L"):
				self.moveLeft()
			if (direction == "R"):
				self.moveRight()

	def distance(self, position):
		return abs(position.x) + abs(position.y)

	def getCrosses(self):
		A = set(self.visited[1])
		B = set(self.visited[2])

		self.crosses = A.intersection(B)

	def nearest(self):
		self.getCrosses()
		return min(self.distance(x) for x in self.crosses)

	def howLong(self, position):
		idx1 = self.visited[1].index(position)
		time1 = self.timings[1][idx1]
		idx2 = self.visited[2].index(position)
		time2 = self.timings[2][idx2]

		return time1 + time2

	def shortest(self):
		self.getCrosses()
		return min(self.howLong(x) for x in self.crosses)

	def oneWire(self, inputString):
		self.wire += 1
		self.time = 0
		self.timings[self.wire] = []
		self.visited[self.wire] = []
		self.position = Pos(x=0, y=0)
		items = inputString.split(",")

		length = len(items)
		for i,x in enumerate(items):
			self.move(x)

	def print(self):
		for line in self.map.get():
			print(line)


class Examples(unittest.TestCase):
	def run(self):
		#myPanel = Panel()
		#myPanel.oneWire("L1")

		#self.assertEqual(myPanel.map.get(), [[0,0,0],[1,0,0],[0,0,0]] )

		myPanel = Panel()
		myPanel.oneWire("R8,U5,L5,D3")
		myPanel.oneWire("U7,R6,D4,L4")

		print(myPanel.crosses)
		#myPanel.print()

		self.assertEqual(myPanel.nearest(), 6)

		myPanel = Panel()
		myPanel.oneWire("R75,D30,R83,U83,L12,D49,R71,U7,L72")
		myPanel.oneWire("U62,R66,U55,R34,D71,R55,D58,R83")
		print(myPanel.crosses)
		self.assertEqual(myPanel.nearest(), 159)

		myPanel = Panel()
		myPanel.oneWire("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51")
		myPanel.oneWire("U98,R91,D20,R16,D67,R40,U7,R15,U6,R7")
		print(myPanel.crosses)
		self.assertEqual(myPanel.nearest(), 135)
	

		#part2	
		myPanel = Panel()
		myPanel.oneWire("R8,U5,L5,D3")
		myPanel.oneWire("U7,R6,D4,L4")

		self.assertEqual(myPanel.shortest(), 30)

		myPanel = Panel()
		myPanel.oneWire("R75,D30,R83,U83,L12,D49,R71,U7,L72")
		myPanel.oneWire("U62,R66,U55,R34,D71,R55,D58,R83")
		print(myPanel.crosses)
		self.assertEqual(myPanel.shortest(), 610)

		myPanel = Panel()
		myPanel.oneWire("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51")
		myPanel.oneWire("U98,R91,D20,R16,D67,R40,U7,R15,U6,R7")
		print(myPanel.crosses)
		self.assertEqual(myPanel.shortest(), 410)

def get_input(input_file):
	return open(input_file).read().strip().split("\n")
	#return [int(x) for x in open(input_file).read().strip().split(",")]


if __name__ == "__main__":
	#TestMatrix().run()

	Examples().run()

	ansPanel = Panel(2000)
	[wire1, wire2] = get_input("input.txt")

	ansPanel.oneWire(wire1)
	ansPanel.oneWire(wire2)

	print("Part 1")
	print(ansPanel.nearest())

	print("Part 2")
	print(ansPanel.shortest())
