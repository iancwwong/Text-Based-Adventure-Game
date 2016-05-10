#! /usr/bin/python

from Queue import PriorityQueue
import GameSymbols as gs
from Gameboard import Gameboard

# A simpler version of gameboard ie without starting position
# Represents the map as a list of lists
class VirtualGameboard(object):
	
	# Attributes
	gamemap = [] 		# view of the map (explored so far)
	direction = 0
	curr_position = {}
	
	# Constructor - make an exact copy of the current gameboard, but without start position
	def __init__(self, gameboard);
		# copy over all the details from gameboard
		self.curr_position = { 'x': gameboard.curr_position['x'], 'y': gameboard.curr_position['y'] }
		self.direction = gameboard.direction
		self.gamemap = []
		for i in range(0, len(gameboard.gamemap)):
			newRow = []
			for j in range(0, len(gameboard.gamemap[i])):
				newRow.append(gameboard.gamemap[i][j])
			self.gamemap.append(newRow)		
		
# Represents a node whilst searching for a path through the gameboard to a specific goal
# Contains 4 pieces of information:
#	
class SearchNode(object):
	
	# Constructor, given a virtual gameboard
	def __init__(self, vgameboard, action, items_at_node):
		self.action = action			# A single char (if '0', init action)
		self.position = new_pos			# { 'x': X, 'y': Y }
		self.items = items_at_node		# [...]
		self.eval_cost = eval_cost		# (Heuristic + cost to reach)

class NodePriorityQueue(PriorityQueue):
	
	# Constructor
	def __init__(self):
		PriorityQueue.__init__(self)
		self.counter = 0

	# Place item into queue in its correct index with priority
	def put(self, node, priority):
		PriorityQueue.put(self, (priority, self.counter, node))
		self.counter += 1

	# Obtain the first item	
	def get(self, *args, **kwargs):
		_,_, node = PriorityQueue.get(self, *args, **kwargs)
		return node

# -------------------------------
# helper functions
# -------------------------------

# determine if an action is valid
def valid(action, gameboard):
	
	# 	

# Compare two position points for equivalence
# Both positions are given as points, in the format:
# 	pos = { 'x': X, 'y': Y }
def equalPostion(pos1, pos2):
	return ( (pos1['x'] == pos2['x']) and (pos1['y'] == pos2['y']) )

# -------------------------------
# main
# -------------------------------

# Construct scenario

# Gameboard is a list of lists
gameboard = Gameboard()
gameboard.gameMap = []
map_row1 = [' ', 'g', ' ', ' ', '~']
map_row2 = [' ', ' ', ' ', ' ', '~']
map_row3 = [' ', ' ', '^', ' ', '~']
map_row4 = ['~', '~', '~', '~', '~']
map_row5 = ['~', '~', '~', '~', '~']
gameboard.gameMap.append(map_row1)
gameboard.gameMap.append(map_row2)
gameboard.gameMap.append(map_row3)
gameboard.gameMap.append(map_row4)
gameboard.gameMap.append(map_row5)

# By default, starting position and current position is at (2,2)

# Assume jason has created:
goal = { 'x' : 1, 'y' : 0 }

# What we know from decisionmaker:
curr_items = []

# --------------------------------
# BEGIN SEARCH FOR LIST OF ACTIONS
# --------------------------------

nodepq = NodePriorityQueue

# Create a virtual gameboard of the initial gameboard state
vgameboard = VirtualGameboard(gameboard)

# Append initial node to queue
node = SearchNode(vgameboard, 0, curr_items)
nodepq.put(node, node.eval_cost)

# Begin A* Search
node = nodepq.get()
while (not equalPosition(node.position, goal)):

	# Create a simulated gameboard situation from node's action
	vgameboard.simulate(node.action)
	
	# Determine list of possible actions from the simulated situation
	possible_actions = []
	for action in gs.action_list:
		if valid(action, vgameboard):
			possible_actions.append(action)

	# For each possible action, create a node and insert into priority queue
	for action in possible_actions:
		tempGameboard = simulateAction(

