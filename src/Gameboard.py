# This is the class that represents the gameboard

#! /usr/bin/python

import sys

class Gameboard(object):

	# Constants	
	DIRECTION_UP = 0
	DIRECTION_RIGHT = 1
	DIRECTION_DOWN = 2
	DIRECTION_LEFT = 3

	# Attributes
	gamemap = [] # global view of the map (explored so far)
	direction = 0
	curr_position = {"x": 2, "y": 2}
	
	# Constructor
	def __init__(self):
		self.direction = self.DIRECTION_UP
#		self.actions = {
#			"f": action_forward, 
#			"l": action_left, 
#			"r": action_right, 
#			"c": action_chop, 
#			"u": action_unlock
#		};
		self.curr_position['x'] = 2
		self.curr_position['y'] = 2

	# Update the map given a view
	# newview is 5x5 list of lists
	def updateMap(self, newview, action):
		if (action == 'init'):
			self.gamemap = newview
		else:
			
			if action == 'f':
				self.action_forward(newview)
			elif action == 'l':
				self.action_left(newview)
			elif action == 'r':
				self.action_right(newview)			
			elif action == 'c':
				self.action_chop(newview)			
			elif action == 'u':
				self.action_unlock(newview)
		
	def action_forward(self, view):
		x = self.curr_position['x']
		y = self.curr_position['y']

		if(self.direction == self.DIRECTION_UP):
			y = y - 1
		if(self.direction == self.DIRECTION_DOWN):
			y = y + 1
		if(self.direction == self.DIRECTION_LEFT):
			x = x - 1
		if(self.direction == self.DIRECTION_RIGHT):
			x = x + 1
		self.gamemap[x][y] = view[2][2]
		self.gamemap[x-1][y] = view[1][2]
		self.gamemap[x+1][y] = view[3][2]
		self.gamemap[x][y-1] = view[2][1]
		self.gamemap[x][y+1] = view[2][3]


		if(self.direction == self.DIRECTION_UP):
			if(y - 2 < 0):
				self.expandTop()
		if(self.direction == self.DIRECTION_DOWN):
			if(y + 2 > len(self.gamemap)):
				self.expandBottom()
		if(self.direction == self.DIRECTION_LEFT):
			if(x - 2 < 0):
				self.expandLeft()
		if(self.direction == self.DIRECTION_RIGHT):
			if(x + 2 > len(self.gamemap[x])):
				self.expandRight()


	def action_left(self, view):
		self.direction = (self.direction - 1) % 4

	def action_right(self, view):
		self.direction = (self.direction + 1) % 4

	def action_chop(self, view):
		# look at curr postion and update area around it
		tree_pos = {"x": self.curr_position['x'], "y": self.curr_position['y']}
		if(self.direction == self.DIRECTION_UP):
			tree_pos.y = tree_pos.y - 1
		if(self.direction == self.DIRECTION_DOWN):
			tree_pos.y = tree_pos.y + 1
		if(self.direction == self.DIRECTION_LEFT):
			tree_pos.x = tree_pos.x - 1
		if(self.direction == self.DIRECTION_RIGHT):
			tree_pos.x = tree_pos.x + 1
		self.gamemap[tree_pos['x']][tree_pos['y']] = " "

	def action_unlock(self, view):

		door_pos = {"x": self.curr_position['x'], "y": self.curr_position['y']}
		if(self.direction == self.DIRECTION_UP):
			door_pos.y = door_pos.y - 1
		if(self.direction == self.DIRECTION_DOWN):
			door_pos.y = door_pos.y + 1
		if(self.direction == self.DIRECTION_LEFT):
			door_pos.x = door_pos.x - 1
		if(self.direction == self.DIRECTION_RIGHT):
			door_pos.x = door_pos.x + 1
		self.gamemap[door_pos['x']][door_pos['y']] = " "
	
	# Display the map
	def showMap(self):
		print "+-----+"
		for i in range(0,len(self.gamemap)):
			sys.stdout.write("|")
			for j in range(0,len(self.gamemap[i])):
				sys.stdout.write(self.gamemap[i][j])
			print "|"
		print "+-----+"

	def expandRight(self):
		numRow = len(self.gamemap)
		for i in range(0,numRow):
			self.gamemap[i].append("?")

	def expandLeft(self):
		numRow = len(self.gamemap)
		for i in range(0,numRow):
			self.gamemap[i] = ["?"] + self.gamemap[i]
		self.curr_position['x'] += 1

	def expandTop(self):
		newYRow = []
		numCol = len(self.gamemap[0])
		for i in range(0,numCol):
			newYRow.append('?')
		self.gamemap.insert(0, newYRow)
		self.curr_position['y'] += 1

	def expandBottom(self):
		newYRow = []
		numCol = len(self.gamemap[0])
		for i in range(0,numCol):
			newYRow.append('?')
		self.gamemap.append(newYRow)
