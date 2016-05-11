#! /usr/bin/python

from Queue import PriorityQueue
import GameSymbols as gs
from Gameboard import Gameboard
from copy import deepcopy
import sys

# A simpler version of gameboard ie without starting position
# Represents the map as a list of lists
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
		if action == gs.ACTION_FOWARD:
			self.actionForward()
		elif action == gs.ACTION_RIGHT:
			self.actionRight()
		elif action == gs.ACTION_LEFT:
			self.actionLeft()
		elif action == gs.ACTION_CHOP:
			self.actionChop()
		elif action == gs.ACTION_UNLOCK:
			self.actionUnlock()

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
		print " +-----+"

	# -------------------------------
	# Simulation functions
	# -------------------------------

	# Move the agent forward in a target direction
	#def actionForward(self):

	# Turn the agent right

	# Turn the agent left
	
	# Chop down a tree
	
	# Unlock a door

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
	
	
		
# Represents a node whilst searching for a path through the gameboard to a specific goal
# Contains 4 pieces of information:
#	
class SearchNode(object):

	# Attributes
	action = ''		# Action carried out to reach this node
	eval_cost = 0		# Cost to reach this node
	vgameboard = None	# Virtual gameboard
	nodeID = 0
	prevNodeID = 0
	
	# Constructor, given a virtual gameboard
	def __init__(self, vgameboard, action, nodeID, prevNodeID):
		self.action = action				# A single char (if '0', init action)
		self.vgameboard = vgameboard			# Virtual gameboard
		self.eval_cost = self.evaluateCost(vgameboard)	# (Heuristic + cost to reach)
		self.nodeID = nodeID
		self.prevNodeID = prevNodeID

	# For inserting into priority queue
	def __cmp__(self, otherNode):
		return cmp(self.eval_cost, otherNode.eval_cost)
	
	# Calculate the cost of a virtual map
	def evaluateCost(self, vgameboard):

		# Calculate heuristic value - Manhattan Distance
		heuristic_val = abs(vgameboard.curr_position['x'] - vgameboard.goal_position['x']) \
				+ abs(vgameboard.curr_position['y'] - vgameboard.goal_position['y'])

		# Determine cost to reach this node
		reach_node_cost = 1

		return (heuristic_val + reach_node_cost)

	# Print out details of node
	def show(self):
		print "++ Node details ++"
		print "Action to reach this node: %s" % self.action
		print "Evaluation cost: %d" % self.eval_cost
		self.vgameboard.show()

# -------------------------------
# helper functions
# -------------------------------

# determine if an action is valid
def valid(action, gameboard):
	return True 	

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
map_row1 = [' ', ' ', ' ', ' ', '~']
map_row2 = [' ', ' ', 'g', ' ', '~']
map_row3 = [' ', ' ', '^', ' ', '~']
map_row4 = ['~', '~', '~', '~', '~']
map_row5 = ['~', '~', '~', '~', '~']
gameboard.gamemap.append(map_row1)
gameboard.gamemap.append(map_row2)
gameboard.gamemap.append(map_row3)
gameboard.gamemap.append(map_row4)
gameboard.gamemap.append(map_row5)

# By default, starting position and current position is at (2,2)

# Assume jason has created:
goal = { 'x' : 2, 'y' : 1 }

# What we know from decisionmaker:
curr_items = []

# --------------------------------
# BEGIN SEARCH FOR LIST OF ACTIONS
# --------------------------------

nodepq = PriorityQueue()

# Create a virtual gameboard of the initial gameboard state
vgameboard = VirtualGameboard(gameboard, curr_items, goal)

# Append initial node to queue
nodeID = 0
node = SearchNode(vgameboard, 0, nodeID, -1)	# -1 = prev node id (in this case, no such thing)
nodepq.put(node)

print "++ Initial node ++"
node.show()
print ""

# Keep track of the nodes in a list, where index = node id
node_list = []
node_list.append(node)

# Begin A* Search
final_action_list = []
while not nodepq.empty():
	node = nodepq.get()
	nodeID += 1

	if equalPosition(node.vgameboard.curr_position, goal):
		# Backtrack list of nodes to get final list of actions
		while (node.nodeID != 0):
			final_action_list.append(node.action)
			node = node_list[node.prevNodeID]

		final_action_list.reverse()
		print "Final list of actions are:"
		print final_action_list
		#return final_action_list
		exit()
	else:
	
		# Determine list of possible actions from the simulated situation
		possible_actions = []
		for action in gs.action_list:
			if valid(action, node.vgameboard):
				possible_actions.append(action)

		print "Possible actions:"
		print possible_actions

		# For each possible action, create a node and insert into priority queue
		for action in possible_actions:
			tempvgameboard = deepcopy(node.vgameboard)
			tempvgameboard.simulate(action)
			newNode = SearchNode(tempvgameboard, action, nodeID, node.nodeID)
			nodeID += 1

			print "++ Expanded node ++"
			newNode.show()
			print ""

			# Put iff newNode doesn't currently exist in list of nodes
			if exists(newNode, node_list):
				print "Node already exists. Gotta ignore it."
				nodeID -= 1
			else:
				print "Adding node with id %d ..." % newNode.nodeID
				nodepq.put(newNode, newNode.eval_cost)
				node_list.append(newNode)
				print "Number of nodes expanded: %d" % len(node_list)

			print ""	# formatting

print "Darn, no path was found."
#return []
