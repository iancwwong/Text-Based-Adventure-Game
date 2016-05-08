# This is the class that represents the gameboard

#!usr/bin/python

import sys

class Gameboard(object):

	# Constants	
	DIRECTION_UP = 1
	DIRECTION_DOWN = 2
	DIRECTION_LEFT = 3
	DIRECTION_LEFT = 4

	# Attributes
	gamemap = []
	direction = 0
	
	# Constructor
	def __init__(self):
		self.direction = self.DIRECTION_UP
		self.
		pass

	# Update the map given a view
	# newview is 5x5 list of lists
	def updateMap(self, newview, action, direction):
		if (action == 'init'):
			self.gamemap = newview
		else:
			if (action == 'f')

	# Display the map
	def showMap(self):
		print "+-----+"
		for i in range(0,len(self.gamemap)):
			sys.stdout.write("|")
			for j in range(0,len(self.gamemap[i])):
				sys.stdout.write(self.gamemap[i][j])
			print "|"
		print "+-----+"
		
