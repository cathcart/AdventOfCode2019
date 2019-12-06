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

		self.center = Pos(x=0, y=0)
		self.__N = N
		self.__matrix = [[0 for x in range(N)] for y in range(N)] 

	def addRow(self):
		self.__matrix.append([0 for x in range(self.__N)])

	def prependRow(self):
		self.__matrix = [[0 for x in range(self.__N)]] + self.__matrix
		self.center = Pos(x=self.center.x, y=self.center.y - 1)

	def addColumn(self):
		for x in self.__matrix:
			x.append(0)

	def prependColumn(self):
		for i,x in enumerate(self.__matrix):
			self.get()[i] = [0] + self.get()[i] 
		self.center = Pos(x=self.center.x+1, y=self.center.y)

	def get(self):
		return self.__matrix

	def __setitem__(self, position, value):
		self.get()[position.y - self.center.y][position.x - self.center.x] = value

	def __getitem__(self, position):
		return self.get()[position.y - self.center.y][position.x - self.center.x]


class TestMatrix(unittest.TestCase):
	def run(self):

		self.assertEqual(Matrix(1).get(), [[0]])
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

	def __init__(self):
		self.map = Matrix(1)
		self.position = Pos(x=0, y=0)
		self.max = PanelLimits(U=0,D=0, L=0, R=0)

		self.crosses = []

	def checkAndMark(self):
		if self.map[self.position] == 1:
			self.crosses.append(self.position)
		else:
			self.map[self.position] = 1

	def moveLeft(self):
		self.position = Pos(x=self.position.x - 1, y=self.position.y)
		if self.position.x < self.max.L:
			self.max = PanelLimits(L=self.position.x, R=self.max.R, U=self.max.U, D=self.max.D)
	
		self.map.prependColumn()
		self.checkAndMark()

	def moveRight(self):
		self.position = Pos(x=self.position.x + 1, y=self.position.y)
		if self.position.x > self.max.R:
			self.max = PanelLimits(R=self.position.x, L=self.max.L, U=self.max.U, D=self.max.D)
	
		self.map.addColumn()
		self.checkAndMark()
		
	def moveUp(self):
		self.position = Pos(x=self.position.x, y=self.position.y - 1)
		if self.position.y > self.max.U:
			self.max = PanelLimits(U=self.position.y, R=self.max.R, L=self.max.L, D=self.max.D)
	
		self.map.prependRow()
		self.checkAndMark()

	def moveDown(self):
		self.position = Pos(x=self.position.x, y=self.position.y + 1)
		if self.position.y < self.max.D:
			self.max = PanelLimits(D=self.position.y, L=self.max.L, U=self.max.U, R=self.max.R)
	
		self.map.addRow()
		self.checkAndMark()


	def move(self, cmd):

		direction = cmd[0]
		magnitude = int(cmd[1:])

		for i in range(magnitude):
			if (direction == "U"):
				self.moveUp()
			if (direction == "D"):
				self.moveDown()
			if (direction == "L"):
				self.moveLeft()
			if (direction == "R"):
				self.moveRight()

	def distance(self, position):
		return position.x + position.y

	def nearest(self):
		return min(self.distance(x) for x in self.crosses)

	def oneWire(self, inputString):
		items = inputString.split(",")

		for x in items:
			self.move(x)


class Examples(unittest.TestCase):
	def run(self):
		myPanel = Panel()
		myPanel.moveLeft()

		self.assertEqual(myPanel.map.get(), [[1,0]] )

		myPanel = Panel()
		myPanel.oneWire("R75,D30,R83,U83,L12,D49,R71,U7,L72")
		myPanel.oneWire("U62,R66,U55,R34,D71,R55,D58,R83")

		self.assertEqual(myPanel.nearest(), 159)

		

def get_input(input_file):
	return [int(x) for x in open(input_file).read().strip().split(",")]


if __name__ == "__main__":
	TestMatrix().run()

	Examples().run()
