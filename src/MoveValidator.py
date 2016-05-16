# This class validates actions according to the rules of the game

#! /usr/bin/python
import GameSymbols as gs

class MoveValidator(object):

	# Constructor
	def __init__(self):
		pass

	# Given a game map in the form of a list of lists,
	# check if a given move is valid
	def isValid(self, action, curr_items, gamemap):
		if action == gs.ACTION_RIGHT:
			return True
		if action == gs.ACTION_LEFT:
			return True
		player = self.findPlayer(gamemap)
		x = player['x']
		y = player['y']

		if(player['dir'] == gs.PLAYER_UP):
			y -= 1
		if(player['dir'] == gs.PLAYER_DOWN):
			y += 1
		if(player['dir'] == gs.PLAYER_RIGHT):
			x += 1
		if(player['dir'] == gs.PLAYER_LEFT):
			x -= 1

		# Check validity of tile to check
		tileToCheck = {'x': x, 'y': y}
		if (self.isValidPosition(tileToCheck, gamemap)):

			# Check possiblity of each action
			if(action == gs.ACTION_FORWARD):
				if gamemap[y][x] == gs.TILE_WATER:
					if(gs.TILE_STEPPING_STONE not in curr_items):
						return False
				elif gamemap[y][x] == gs.TILE_DOOR:
					return False
				elif gamemap[y][x] == gs.TILE_TREE:
					return False
				elif gamemap[y][x] == gs.TILE_WALL:
					return False
				elif gamemap[y][x] == gs.TILE_MAP_EDGE:
					return False
				elif gamemap[y][x] == gs.TILE_UNKNOWN:
					return False

			elif(action == gs.ACTION_CHOP):
				if gamemap[y][x] == gs.TILE_TREE:
					if(gs.TILE_AXE not in curr_items):
						return False
				else:
					return False

			elif(action == gs.ACTION_UNLOCK):
				if gamemap[y][x] == gs.TILE_DOOR:
					if(gs.TILE_KEY not in curr_items):
						return False
				else:
					return False

			# All impossible moves have been ruled out
			return True

		# Case that tile does not exist on map
		else:
			return False

	# Given a game map in the form of a list of lists,
	# return ALL valid moves
	def getAllValidMoves(self, curr_items, gamemap):
		return [a for a in gs.action_list if self.isValid(a, curr_items, gamemap)]

	# ---------------------------
	# HELPER FUNCTIONS
	# ---------------------------

	# Return the location and direction of the player on the map in the format:
	# 	 position = { 'x': x, 'y': y, 'dir': dir }
	def findPlayer(self, gamemap):
		player = {"x": 0, "y": 0, "dir": 0}
		for i in range(0, len(gamemap)):
			for j in range(0, len(gamemap[0])):
				if(gamemap[i][j] == gs.PLAYER_UP):
					player['dir'] = gs.PLAYER_UP
					player['x'] = j
					player['y'] = i
					return player
				elif(gamemap[i][j] == gs.PLAYER_RIGHT):
					player['dir'] = gs.PLAYER_RIGHT
					player['x'] = j
					player['y'] = i
					return player
				elif(gamemap[i][j] == gs.PLAYER_DOWN):
					player['dir'] = gs.PLAYER_DOWN
					player['x'] = j
					player['y'] = i
					return player
				elif(gamemap[i][j] == gs.PLAYER_LEFT):
					player['dir'] = gs.PLAYER_LEFT
					player['x'] = j
					player['y'] = i
					return player

	# Return whether a specific position on the map is valid,
	# given in the format:
	#	pos = { 'x': x, 'y': y }
	# Note: assumes gamemap is RECTANGULAR in shape
	def isValidPosition(self, pos, gamemap):
		numRows = len(gamemap)
		numCols = len(gamemap[0])
		if (pos['y'] < numRows) and (pos['y'] >= 0):
			if (pos['x'] < numCols) and (pos['x'] >= 0):
				return True
		return False
