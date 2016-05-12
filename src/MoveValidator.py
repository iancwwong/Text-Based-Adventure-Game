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
		if(action == gs.ACTION_FORWARD):
			if gamemap[x][y] == gs.TILE_WATER:
				if(gs.TITLE_STEPPING_STONE not in curr_items):
				return False
			elif gamemap[x][y] == gs.TITLE_DOOR:
				return False
			elif gamemap[x][y] == gs.TITLE_TREE:
				return False
			elif action[x][y] == gs.TITLE_WALL:
				return False
			elif action[x][y] == gs.TITLE_MAP_EDGE:
				return False
		if(action == gs.ACTION_CHOP):
			if gamemap[x][y] == gs.TILE_TREE:
				if(gs.TITLE_AXE not in curr_items):
					return False
			elif
				return False
		if(action == gs.ACTION_UNLOCK):
			if gamemap[x][y] == gs.TITLE_DOOR:
				if(gs.TITLE_KEY not in curr_items):
					return False
			elif
				return False
		return True

	def findPlayer(self, gamemap):
		player = {"x": 0, "y": 0, "dir": 0}
		for i in range(0, len(gamemap)):
			for j in range(0, len(gamemap[0])):
				if(gamemap[i][j] == gs.PLAYER_UP):
					player['dir'] = gs.PLAYER_UP
					player['x'] = i
					player['y'] = j
					return player
				elif(gamemap[i][j] == gs.PLAYER_RIGHT):
					player['dir'] = gs.PLAYER_RIGHT
					player['x'] = i
					player['y'] = j
					return player
				elif(gamemap[i][j] == gs.PLAYER_DOWN):
					player['dir'] = gs.PLAYER_DOWN
					player['x'] = i
					player['y'] = j
					return player
				elif(gamemap[i][j] == gs.PLAYER_LEFT):
					player['dir'] = gs.PLAYER_LEFT
					player['x'] = i
					player['y'] = j
					return player
	# Given a game map in the form of a list of lists,
	# return ALL valid moves
	def getAllValidMoves(self, curr_items, gamemap):
		pass
