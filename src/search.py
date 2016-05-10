#! /usr/bin/python

from Queue import PriorityQueue
import GameSymbols as gs

class SearchNode(object):
	
	# Constructor, given the sufficient details
	def __init__(self, action, new_pos, items_at_node, eval_cost):
		self.action = action
		self.position = new_pos
		self.items = items_at_node
		self.eval_cost = eval_cost

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
	

# -------------------------------
# main
# -------------------------------

# Construct scenario

# Gameboard is a list of lists
gameboard = []
gameboard_row1 = [' ', 'g', ' ', ' ', '~']
gameboard_row2 = [' ', ' ', ' ', ' ', '~']
gameboard_row3 = [' ', ' ', '^', ' ', '~']
gameboard_row4 = ['~', '~', '~', '~', '~']
gameboard_row5 = ['~', '~', '~', '~', '~']
gameboard.append(gameboard_row1)
gameboard.append(gameboard_row2)
gameboard.append(gameboard_row3)
gameboard.append(gameboard_row4)
gameboard.append(gameboard_row5)

# From gameboard, we have:
curr_position = { 'x' : 2, 'y' : 2 }
direction = 1	# upwards

# Assume jason has created:
goal = { 'x' : 1, 'y' : 0 }

# --------------------------------
# BEGIN SEARCH FOR LIST OF ACTIONS
# --------------------------------

nodepq = NodePriorityQueue

# Determine list of possible actions
possible_actions = []
for action in gs.action_list:
	if valid(action, gameboard):
		possible_actions.append(action)

# For each possible action, create a node and insert into priority queue


