import collections
import unittest
from functools import reduce

class Planet():
	def __init__(self, name):
		self.name = name
		self.children = []
		self.numberOfOrbits = 0
		self.parent = None

	def orbit(self, planet):
		if(planet not in self.children):
			self.children.append(planet)
			self.children[-1].parent = self

	def setOrbits(self):
		#print("hello from ", self.name)
		for child in self.children:
			child.parent = self
			child.numberOfOrbits = self.numberOfOrbits + 1
			child.setOrbits()

	def getOrbits(self):
		total = self.numberOfOrbits
		for child in self.children:
			total += child.getOrbits()
		return total

	def __repr__(self):
		return self.name

class SolarMap():
	def __init__(self, inputs):
		self.planets = []
		self.inputs = inputs

	def run(self):
		self.buildPlanetNames()
		#print("planet names done")
		self.buildPlanets()
		#print("planets done")
		self.fixOrbits()
		#print("orbits done")

	def buildPlanetNames(self):
		
		for x in self.inputs:
			[a,b] = x.split(")")

			if a not in self.planets:
				self.planets.append(a)
			if b not in self.planets:
				self.planets.append(b)

	def findPlanet(self, planetName):
		return list(filter(lambda x: x.name == planetName, self.actual_planets))[0]

	def buildPlanets(self):
		self.actual_planets = list(map(lambda x: Planet(x), self.planets))

		for x in self.inputs:
			[a,b] = x.split(")")
			A = self.findPlanet(a)
			B = self.findPlanet(b)

			A.children.append(B)
			A.orbit(B)

	def fixOrbits(self):

		COM = self.findPlanet("COM")
		COM.setOrbits()

	def totalOrbits(self):

		return sum(list(map(lambda x: x.numberOfOrbits, self.actual_planets)))

	def pathToCOM(self, planet):
		if(planet.parent.name == "COM"):
			return [planet]
		else:
			return [planet] + self.pathToCOM(planet.parent)

	def minDistanceToSanta(self):
		you = self.findPlanet("YOU")
		you_planet = you.parent
		san = self.findPlanet("SAN")
		san_planet = san.parent

		min_path_planets = set(self.pathToCOM(you_planet)) ^ set(self.pathToCOM(san_planet)) 
	
		return len(min_path_planets) 


class TestSolarMap(unittest.TestCase):
	def run(self):

		inputs = get_input("example.txt")
		solMap = SolarMap(inputs)
		solMap.run()
		#print(solMap.actual_planets)
		#print(solMap.findPlanet("K").children)

		self.assertEqual(solMap.findPlanet("D").numberOfOrbits, 3)
		self.assertEqual(solMap.findPlanet("L").numberOfOrbits, 7)
		self.assertEqual(solMap.findPlanet("COM").numberOfOrbits, 0)
		self.assertEqual(solMap.totalOrbits(), 42)

	def run2(self):

		inputs = get_input("example2.txt")
		solMap = SolarMap(inputs)
		solMap.run()
		self.assertEqual(solMap.minDistanceToSanta(), 4)


def get_input(input_file):
	return open(input_file).read().strip().split("\n")


if __name__ == "__main__":
	TestSolarMap().run()

	inputs = get_input("input.txt")
	solMap = SolarMap(inputs)
	solMap.run()

	print(solMap.totalOrbits())

	TestSolarMap().run2()
	inputs = get_input("input.txt")
	solMap = SolarMap(inputs)
	solMap.run()

	print(solMap.minDistanceToSanta())

