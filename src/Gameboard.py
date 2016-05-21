# This is the class that represents the gameboard
# Note: A point on the map is represented as a dict in the format:
#	point = { "x": x, "y": y }
# Gamemap is a list of lists, where the first index is the 'y' coordinate,
# and the second index is the 'x' coordinate
# ie gamemap[y][x]
#! /usr/bin/python

import sys
import GameSymbols as gs

class Gameboard(object):

	# Constants

	# Direction
	DIRECTION_UP = 0
	DIRECTION_RIGHT = 1
	DIRECTION_DOWN = 2
	DIRECTION_LEFT = 3

	# Map Location Types
	LOCATION_EDGE = 0

	null_position = {'x': -1, 'y': -1}

	# Attributes
	gamemap = [] 		# global view of the map (explored so far)
	direction = 0
	curr_position = {}
	start_position = {}

	# Constructor
	def __init__(self):
		self.direction = self.DIRECTION_UP
		self.curr_position['x'] = 2
		self.curr_position['y'] = 2
		self.start_position['x'] = 2
		self.start_position['y'] = 2

	# ---------------------------
	# MAP MANIPULATION
	# ---------------------------

	# Update the map given a view "newview", which is 5x5 list of lists
	# Note: Assumes the real map has changed in some way
	def updateMap(self, newview, action):
		if (action == 'init'):
			self.gamemap = newview
		else:
			if action == gs.ACTION_FORWARD:
				self.action_forward(newview)
			elif action == gs.ACTION_LEFT:
				self.action_left(newview)
			elif action == gs.ACTION_RIGHT:
				self.action_right(newview)
			elif action == gs.ACTION_CHOP:
				self.action_chop(newview)
			elif action == gs.ACTION_UNLOCK:
				self.action_unlock(newview)

	# Update map from view given as agent moved FORWARD
	def action_forward(self, view):

		# Determine new position
		newPos = self.movePoint(self.curr_position, self.direction)

		# Expand the map (if necessary) in the appropriate direction
		if(self.direction == self.DIRECTION_UP):
			if(newPos['y'] - 2 < 0):
				self.expandTop()
				newPos = self.movePoint(self.curr_position, self.direction)
		elif(self.direction == self.DIRECTION_DOWN):
			if(newPos['y'] + 2 >= len(self.gamemap)):
				self.expandBottom()
		elif(self.direction == self.DIRECTION_LEFT):
			if(newPos['x'] - 2 < 0):
				self.expandLeft()
				newPos = self.movePoint(self.curr_position, self.direction)
		elif(self.direction == self.DIRECTION_RIGHT):
			if(newPos['x'] + 2 >= len(self.gamemap[newPos['y']])):
				self.expandRight()

		# Update the player's current position and icon
		self.updatePlayerPosition(newPos)

		# Correct (ie rotate) the view as appropriate to direction
		correctedView = view
		if (self.direction == self.DIRECTION_RIGHT):
			correctedView = self.rotateView(view)

		elif (self.direction == self.DIRECTION_DOWN):
			correctedView = self.rotateView(self.rotateView(view))

		elif (self.direction == self.DIRECTION_LEFT):
			correctedView = self.rotateView(self.rotateView(self.rotateView(view)))

		print "Corrected view, with direction %d:" % self.direction
		self.showView(correctedView)

		print "Portion of map to update:"
		print "From (%d, %d) to (%d, %d)" %(self.curr_position['y'] - 2, self.curr_position['x'] - 2, \
							self.curr_position['y'] + 2, self.curr_position['x'] + 2)

		# Overwrite the portion of the map using the corrected view
		# ie the 24 squares around the agent's new current position
		#	[ (currpos.x - 2, currpos.y - 2), (currpos.x + 2, currpos.y + 2) ]
		viewrow = 0										# row index of view
		for maprow in range(self.curr_position['y'] - 2, self.curr_position['y'] + 3):		# row index of actual map
			viewcol = 0									# col index of view
			for mapcol in range(self.curr_position['x'] - 2, self.curr_position['x'] + 3):	# col index of actual map

				# Check for player position in view  at (2,2)
				if (viewrow != 2 or viewcol != 2):
					# Overwrite the tile with the corresponding one provided in view
					self.gamemap[maprow][mapcol] = correctedView[viewrow][viewcol]
				viewcol += 1
			viewrow += 1

		# Place important markers
		self.placeMarkers()


	# Update icon of agent as facing the new direction when turned left
	def action_left(self, view):
		self.direction = (self.direction - 1) % 4
		self.updatePlayerIcon()

	# Update icon of agent as facing the new direction when turned right
	def action_right(self, view):
		self.direction = (self.direction + 1) % 4
		self.updatePlayerIcon()

	# Set position of a tree to be blank
	def action_chop(self, view):
		tree_pos = self.movePoint(self.curr_position, self.direction)

		# Change the door to blank ONLY if position originally contains a door
		# Else throw an error
		if (self.getTile(tree_pos) == gs.TILE_TREE):
			self.changeTile(tree_pos, gs.TILE_BLANK)

	# Set position of a door to be blank
	def action_unlock(self, view):
		door_pos = self.movePoint(self.curr_position, self.direction)

		# Change the door to blank ONLY if position originally contains a door
		# Else throw an error
		if (self.getTile(door_pos) == gs.TILE_DOOR):
			self.changeTile(door_pos, gs.TILE_BLANK)

	# Expand the map by adding in a column on the right
	def expandRight(self):
		numRow = len(self.gamemap)
		for i in range(0,numRow):
			self.gamemap[i].append(gs.TILE_UNKNOWN)

	# Expand the map by adding in a column on the left
	def expandLeft(self):
		numRow = len(self.gamemap)
		for i in range(0,numRow):
			self.gamemap[i] = ["?"] + self.gamemap[i]
		self.curr_position['x'] += 1		# Move player one tile to the right
		self.start_position['x'] += 1		# Move starting position one tile to the right

	# Expand the map by adding in a row on the top
	def expandTop(self):
		newYRow = []
		numCol = len(self.gamemap[0])
		for i in range(0,numCol):
			newYRow.append('?')
		self.gamemap.insert(0, newYRow)
		self.curr_position['y'] += 1		# Move player one tile down
		self.start_position['y'] += 1		# Move starting position one tile down

	# Expand the map by adding in a row on the bottom
	def expandBottom(self):
		newYRow = []
		numCol = len(self.gamemap[0])
		for i in range(0,numCol):
			newYRow.append('?')
		self.gamemap.append(newYRow)

	# Update the player icon according to the direction
	def updatePlayerIcon(self):
		if (self.direction == self.DIRECTION_UP):
			self.changeTile(self.curr_position, gs.PLAYER_UP)
		elif (self.direction == self.DIRECTION_RIGHT):
			self.changeTile(self.curr_position, gs.PLAYER_RIGHT)
		elif (self.direction == self.DIRECTION_DOWN):
			self.changeTile(self.curr_position, gs.PLAYER_DOWN)
		elif (self.direction == self.DIRECTION_LEFT):
			self.changeTile(self.curr_position, gs.PLAYER_LEFT)

	# Update the player's position (given as a dict)
	def updatePlayerPosition(self, newPos):
		self.curr_position = newPos

	# Place important markers on the map
	def placeMarkers(self):
		# Starting position
		self.changeTile(self.start_position, gs.TILE_START_POS)

		# Player
		self.updatePlayerIcon()

	# Change the tile to a specific tile character
	def changeTile(self, pos, newTileChar):
		try:
			self.gamemap[pos['y']][pos['x']] = newTileChar
		except IndexError:
			print "Error: " + pos + " is invalid for current map."

	# Rotate a view 90 degrees to the right
	# Assume to be a 5x5 2d array
	def rotateView(self, view):
		# Prepare the new view
		rotatedView = []

		# Load the values
		for i in range(0,5):			# column
			rotatedRow = []
			for j in range(0, 5):		# row
				rotatedRow.append(view[len(view) - j - 1][i])
			rotatedView.append(rotatedRow)

		# Return the rotated view
		return rotatedView


	# ---------------------------
	# MAP INFO
	# ---------------------------
	# Display the map
	def showMap(self):
		numCol = len(self.gamemap[0])

		# Print column indexes
		sys.stdout.write(" +")
		for i in range(0, numCol):
			sys.stdout.write(str(i))
		print "+"
		for i in range(0,len(self.gamemap)):
			# Print out row index
			sys.stdout.write(str(i))
			sys.stdout.write("|")
			for j in range(0,len(self.gamemap[i])):
				sys.stdout.write(self.gamemap[i][j])
			print "|"
		sys.stdout.write(' +')
		sys.stdout.write(''.join(['-' for i in range(0, numCol)]))
		print "+"

	# Determine a new point, given it has moved one space in a target direction
	def movePoint(self, point, direction):
		newPos = { "x": point['x'], "y": point['y'] }
		if(direction == self.DIRECTION_UP):
			newPos['y'] = newPos['y'] - 1
		elif(direction == self.DIRECTION_DOWN):
			newPos['y'] = newPos['y'] + 1
		elif(direction == self.DIRECTION_LEFT):
			newPos['x'] = newPos['x'] - 1
		elif(direction == self.DIRECTION_RIGHT):
			newPos['x'] = newPos['x'] + 1
		return newPos

	# Return the character at a particular position on the map
	def getTile(self, point):
		try:
			return self.gamemap[point['y']][point['x']]
		except IndexError:
			print "Error: " + str(point) + " is invalid for current map."

	# returns the number of column in the gameboard
	def numCols(self):
		return len(self.gamemap[0])

	# return the number of rows in the gameboard
	def numRows(self):
		return len(self.gamemap)

	# return whether a position is a valid position on the map
	def isValidPosition(self, pos):
		if (pos['y'] < self.numRows()) and (pos['y'] >= 0):
			if (pos['x'] < self.numCols()) and (pos['x'] >= 0):
				return True
		return False

	# return whether the 4 adjacent squares to a given position contains
	# a particular tile type
	def hasAdjacent(self, pos, tileType):
		for adjSquare in self.getAdjacentSquares(pos):
			if self.getTile(adjSquare) == tileType:
				return True
		return False

	# return whether a given position is located in a particular region
	# Pos given as format:
	# 	pos = { 'x': x, 'y': y }
	def located(self, pos, locType):
		# Obtain the list of all positions with the given locType
		locPosList = []

		# Case of map edge: first and last columns, first and last rows
		if locType == self.LOCATION_EDGE:
			for i in range(0, self.numRows()):
				if (i > 0 and i < self.numRows() - 1):
					for j in [0, self.numCols() - 1]:
						currPos = { 'x': j, 'y': i}
						locPosList.append(currPos)				
				else:
					for j in range(0, self.numCols()):
						currPos = { 'x': j, 'y': i}
						locPosList.append(currPos)

		# Check whether the given pos is in the region
		for locPos in locPosList:
			if self.equalPosition(locPos, pos):
				return True
		return False

	# Return all valid adjacent squares around a given position as a list
	# arg[0] = pos
	# arg[1] = tile type
	def getAdjacentSquares(self, *args):
		pos = args[0]

		# Construct a list of all 4 valid positions around a given position
		possibleAdjSquares = []
		squareUp = { 'x': pos['x'], 'y' : pos ['y'] - 1 }
		squareRight = { 'x': pos['x'] + 1, 'y' : pos ['y'] }
		squareDown = { 'x': pos['x'], 'y' : pos ['y'] + 1 }
		squareLeft = { 'x': pos['x'] - 1, 'y' : pos ['y'] }
		possibleAdjSquares.append(squareUp)
		possibleAdjSquares.append(squareRight)
		possibleAdjSquares.append(squareDown)
		possibleAdjSquares.append(squareLeft)

		if len(args) > 1:
			return [square for square in possibleAdjSquares if ( \
						self.isValidPosition(square) and (self.getTile(square) == args[1])
					)]
		else:
			return [square for square in possibleAdjSquares if self.isValidPosition(square)]

	# Return the position of the gold on gamemap if found.
	# else return the null_position value
	def getItemPosition(self, itemToGet):
		itemPosList = []
		for i in range(0, self.numRows()):
			for j in range(0, self.numCols()):
				currpoint = {"x" : j, "y" : i}
				if(self.getTile(currpoint) == itemToGet):
					itemPosList.append(currpoint)
		return itemPosList

	# Find all the blank tiles on the edge of a map
	def getBlankEdgeTiles(self):
		blankEdgeTilePositions = []

		# Check only edge tiles
		for i in range(0, self.numRows()):
			if (i > 0 and i < self.numRows() - 1):
				for j in [0, self.numCols() - 1]:
					currPos = { 'x': j, 'y': i}
					if (self.getTile(currPos) == gs.TILE_BLANK):
						blankEdgeTilePositions.append(currPos)					
			else:
				for j in range(0, self.numCols()):
					currPos = { 'x': j, 'y': i}
					if (self.getTile(currPos) == gs.TILE_BLANK):
						blankEdgeTilePositions.append(currPos)

		return blankEdgeTilePositions

	# Find all the question tiles on a map
	def getUnknownTiles(self):
		unknownTiles = []
		for i in range(0, self.numRows()):
			for j in range(0, self.numCols()):
				currPos = { 'x': j, 'y': i}
				if (self.getTile(currPos) == gs.TILE_UNKNOWN):
					unknownTiles.append(currPos)
		return unknownTiles

	# [DEBUG] Print out a particular view
	def showView(self, view):
		viewStr = "+-----+\n"
		for i in range(0,len(view)):
			viewStr += "|"
			for j in range(0,len(view[i])):
				viewStr += view[i][j]
			viewStr += "|\n"
		viewStr += "+-----+"
		print viewStr

	# ---------------------------
	# HELPER FUNCTIONS
	# ---------------------------

	# Compare two position points for equivalence
	# Both positions are given as points, in the format:
	# 	pos = { 'x': X, 'y': Y }
	def equalPosition(self, pos1, pos2):
		return ( (pos1['x'] == pos2['x']) and (pos1['y'] == pos2['y']) )
