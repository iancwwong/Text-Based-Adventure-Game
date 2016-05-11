#! /usr/bin/python

from Queue import PriorityQueue
import GameSymbols as gs
from Gameboard import Gameboard
from MoveValidator import MoveValidator
from copy import deepcopy
import sys

# A simpler version of gameboard ie without starting position
# Represents the map as a list of lists
# Like Gameboard, a point is interpreted as:
#	point = { "x": x, "y": y }
class VirtualGameboard(object):
	# Constants
	# Direction
	DIRECTION_UP = 0
	DIRECTION_RIGHT = 1
	DIRECTION_DOWN = 2
	DIRECTION_LEFT = 3
	
	# Attributes
	gamemap = [] 		# view of the map (explored so far) (assumed to be rectangular)
	direction = 0
	curr_position = {}
	goal_position = {}
	items = []
	
	# Constructor - make an exact copy of the current gameboard, but without start position
	def __init__(self, gameboard, items, goal):
		# copy over all the details from gameboard
		self.curr_position = deepcopy(gameboard.curr_position)
		self.goal_position = deepcopy(goal)
		self.direction = gameboard.direction
		self.gamemap = deepcopy(gameboard.gamemap)
		self.items = deepcopy(items)

	# Change the map based on an action
	# Assumes the action is valid
	def simulate(self, action):
		if action == gs.ACTION_FORWARD:
			self.actionForward()
		elif action == gs.ACTION_RIGHT:
			self.actionRight()
		elif action == gs.ACTION_LEFT:
			self.actionLeft()
		elif action == gs.ACTION_CHOP:
			self.actionChop()
		elif action == gs.ACTION_UNLOCK:
			self.actionUnlock()

	# -------------------------------
	# Simulation functions
	# -------------------------------

	# Move the agent forward in a target direction
	def actionForward(self):
		newPos = self.movePoint(self.curr_position, self.direction)

		# Check for any items
		if self.hasItem(newPos):
			self.items.append(self.getTile(newPos))
	
		# Make the old curr_position blank
		# NOTE: This will simply assume previous position is reachable
		self.changeTile(self.curr_position, gs.TILE_BLANK)
		
		# Update agent's position and icon
		self.curr_position = newPos
		self.updatePlayerIcon()

	# Update icon of agent as facing the new direction when turned left
	def actionLeft(self):
		self.direction = (self.direction - 1) % 4
		self.updatePlayerIcon()

	# Update icon of agent as facing the new direction when turned right
	def actionRight(self):
		self.direction = (self.direction + 1) % 4
		self.updatePlayerIcon()
	
	# Set position of a tree to be blank
	def actionChop(self):
		tree_pos = self.movePoint(self.curr_position, self.direction)

		# Change the door to blank ONLY if position originally contains a door
		# Else throw an error
		if (self.getTile(tree_pos) == gs.TILE_TREE):
			self.changeTile(tree_pos, gs.TILE_BLANK)

	# Set position of a door to be blank
	def actionUnlock(self):
		door_pos = self.movePoint(self.curr_position, self.direction)

		# Change the door to blank ONLY if position originally contains a door
		# Else throw an error
		if (self.getTile(door_pos) == gs.TILE_DOOR):
			self.changeTile(door_pos, gs.TILE_BLANK)

	# -----------------------
	# Map Manipulation
	# -----------------------

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


	# Change a tile to a particular icon
	def changeTile(self, pos, newTileChar):
		try:
			self.gamemap[pos['y']][pos['x']] = newTileChar
		except IndexError:
			print "Error: " + pos + " is invalid for current map."

	# -----------------------
	# Map Info
	# -----------------------

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
			print "Error: " + point + " is invalid for current map."

	# Check whether a particular position has an item
	def hasItem(self, pos):
		return (self.getTile(pos) in gs.item_list)

	# Print out details of virtual gameboard
	def show(self):
		print "Current position: (%d, %d)" % (self.curr_position['x'], self.curr_position['y'])
		print "Goal position: (%d, %d)" % (self.goal_position['x'], self.goal_position['y'])
		print "Current direction: %d" % self.direction
		print "Items: %s" % str(self.items)
		print "Map:"
		self.showMap()

	# Print out the map (essentially same as gameboard's showMap function)
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
		
# Represents a node whilst searching for a path through the gameboard to a specific goal	
class SearchNode(object):

	# Attributes
	action = ''		# Action carried out to reach this node
	eval_cost = 0		# Cost to reach this node
	vgameboard = None	# Virtual gameboard
	prevNode = None
	
	# Constructor, given a virtual gameboard
	def __init__(self, vgameboard, action, prevNode):
		self.action = action				# A single char (if '0', init action)
		self.vgameboard = vgameboard			# Virtual gameboard
		self.eval_cost = self.evaluateCost()		# Calculate the node cost based on gameboard
		self.prevNode = prevNode

	# For inserting into priority queue
	def __cmp__(self, otherNode):
		if otherNode == None:
			return 1
		return cmp(self.eval_cost, otherNode.eval_cost)
	
	# Calculate the evaluation value of a virtual map
	def evaluateCost(self):

		heuristic_val = self.getHeuristicValue()
		reach_node_cost = self.getReachCost()
		return (heuristic_val + reach_node_cost)

	# Print out details of node
	def show(self):
		print "++ Node details ++"
		print "Action to reach this node: %s" % self.action
		print "Evaluation cost: %d" % self.eval_cost
		self.vgameboard.show()

	# Use the Manhattan distance to obtain the heuristic value
	def getHeuristicValue(self):
		return abs(self.vgameboard.curr_position['x'] - self.vgameboard.goal_position['x']) \
				+ abs(self.vgameboard.curr_position['y'] - self.vgameboard.goal_position['y'])

	def getReachCost(self):
		return 1

# -------------------------------
# helper functions
# -------------------------------

# Compare two position points for equivalence
# Both positions are given as points, in the format:
# 	pos = { 'x': X, 'y': Y }
def equalPosition(pos1, pos2):
	return ( (pos1['x'] == pos2['x']) and (pos1['y'] == pos2['y']) )

# Check whether a search node is in a list of search nodes (equivalence)
def exists(searchNode, nodeList):
	for node in nodeList:
		if equalVGameboards(node.vgameboard, searchNode.vgameboard):
			return True
	return False

# Check for equivalence between virtual gameboards
def equalVGameboards(vgameboard1, vgameboard2):

	# Direction
	if vgameboard1.direction != vgameboard2.direction:
		return False

	# Current position
	if not equalPosition(vgameboard1.curr_position, vgameboard2.curr_position):
		return False

	# Goal position
	if not equalPosition(vgameboard1.goal_position, vgameboard2.goal_position):
		return False

	# Item list
	if not (set(vgameboard1.items) == set(vgameboard2.items)):
		return False
	
	# Gamemap
	if (len(vgameboard1.gamemap) != len(vgameboard2.gamemap)) or \
	   (len(vgameboard1.gamemap[0]) != len(vgameboard2.gamemap[0])):
		return False

	for i in range(0, len(vgameboard1.gamemap)):
		for j in range(0, len(vgameboard1.gamemap)):
			if (vgameboard1.gamemap[i][j] != vgameboard2.gamemap[i][j]):
				return False
	return True

# -------------------------------
# main
# -------------------------------

# Construct scenario

# Gameboard is a list of lists
gameboard = Gameboard()
gameboard.gamemap = []
map_row0 = [' ', 'g', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
map_row1 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
map_row2 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
map_row3 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
map_row4 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
map_row5 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
map_row6 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
map_row7 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
map_row8 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '<', ' ']
map_row9 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
gameboard.gamemap.append(map_row0)
gameboard.gamemap.append(map_row1)
gameboard.gamemap.append(map_row2)
gameboard.gamemap.append(map_row3)
gameboard.gamemap.append(map_row4)
gameboard.gamemap.append(map_row5)
gameboard.gamemap.append(map_row6)
gameboard.gamemap.append(map_row7)
gameboard.gamemap.append(map_row8)
gameboard.gamemap.append(map_row9)

# Set current position
gameboard.curr_position = { 'x': 8, 'y': 8 }

# Set direction
gameboard.direction = Gameboard.DIRECTION_LEFT

# Assume jason has created
goal = { 'x' : 1, 'y' : 0 }

# What we know from decisionmaker:
curr_items = []

# --------------------------------
# BEGIN SEARCH FOR LIST OF ACTIONS
# --------------------------------

# Prepare priority queue
nodepq = PriorityQueue()

# Prepare a move validator
mv = MoveValidator()

# Create a virtual gameboard of the initial gameboard state
vgameboard = VirtualGameboard(gameboard, curr_items, goal)

# Append initial node to queue
node = SearchNode(vgameboard, 0, None)	# 0 = no previous action; None = No previous node
nodepq.put(node)

print "Initial Position:"
node.show()
print ""

# Keep track of the nodes in a list, where index = node id
node_list = []
node_list.append(node)

# Begin A* Search
final_action_list = []
while not nodepq.empty():
	node = nodepq.get()

	if equalPosition(node.vgameboard.curr_position, goal):

		# Show final position
		print "Final position:"
		node.show()

		# Backtrack list of nodes to get final list of actions
		while not node.prevNode == None:
			final_action_list.append(node.action)
			node = node.prevNode

		final_action_list.reverse()
		print "Final list of actions are:"
		print final_action_list
		#return final_action_list
		exit()
	else:
	
		# Determine list of possible actions from the simulated situation
		#possible_actions = mv.getAllValidMoves(node.vgameboard.gamemap)
		possible_actions = ['f', 'l', 'r']

		# For each possible action, create a node and insert into priority queue
		for action in possible_actions:
			tempvgameboard = deepcopy(node.vgameboard)
			tempvgameboard.simulate(action)
			newNode = SearchNode(tempvgameboard, action, node)

			# Put iff newNode doesn't currently exist in list of nodes
			if exists(newNode, node_list):
				""" Ignore """
			else:
				nodepq.put(newNode, newNode.eval_cost)
				node_list.append(newNode)

print "Darn, no path was found."
#return []
