# This is the class that represents the decision making component of the agent
#
# Note: A 'position' is represented as a dict, in the format:
#	position = { 'x': X, 'y': Y }
# Note: A 'high level goal' is represented as a tuple, in the format:
#	highLevelGoal = (<TYPE>, <POSITION>)

#! /usr/bin/python

from Queue import PriorityQueue
from MoveValidator import MoveValidator
from copy import deepcopy
import sys
import GameSymbols as gs
import math
import random				# Final line of decision making

class DecisionMaker(object):
	# Constants
	null_position = {'x': -1, 'y': -1}
	
	# High Level Goal types
	GOALTYPE_REACH = 1
	GOALTYPE_GET_ITEM = 2
	GOALTYPE_EXPLORE = 3
	GOALTYPE_ELIMINATE_OBSTACLE = 4

	# Attributes
	past_actions = []		# a list of past actions (consisting of single chars)
	todo_actions = []		# a list of actions to perform
	curr_items = []			# a list of items we currently possess
	target_items = []		# a list of items to get in order to obtain the gold
	curr_goal = ()			# a tuple that contains the current goal
	gameboard = None 		# gameboard containing current environment state
	mv = None 				# Move validator

	# Constructor
	def __init__(self, gameboard):
		self.past_actions = []
		self.gameboard = gameboard
		self.todo_actions = []
		self.curr_items = []
		self.target_items = []
		self.curr_goal = ()
		self.target_items = []
		self.mv = MoveValidator()

	# Appends a given action (assumed to be a single char)
	def addPastAction(self, action_char):
		self.past_actions.append(action_char)

	# Returns the last (successful) action conducted by the agent
	def getLatestAction(self):
		return self.past_actions[-1]

	# Returns all the (successful) actions conducted by the agent as a list
	def getAllPastActions(self):
		return self.past_actions

	# Return an action to agent
	def getAction(self):
		# Check if there are currently any actions pre-determined
		if len(self.todo_actions) == 0:
			self.determineActions()
		return self.todo_actions.pop(0)

	# Determine the goal and the actions to reach that goal
	def determineActions(self):

		# Holds our final list of actions
		newActions = []

		# Determine our goal
		goal = self.determineGoal()

		print "Current goal: %s" % str(goal)

		# Perform a search on the current gameboard to determine the list of actions
		newActions = self.getReachGoalActions(goal, self.gameboard)

		# DEBUGGING
		sys.stdout.write("Goal: ")
		print goal
		sys.stdout.write("Actions to reach this goal: ")
		print newActions	
			
		self.todo_actions.extend(newActions)

		# DEBUGGING
		print "List of todo actions:"
		print self.todo_actions

		# Remember current goal
		self.curr_goal = goal

	# update the current list of items we have in the list
	def updateCurrItems(self, items):
		self.curr_items = items

	# Determine a goal based on decision making flowchart
	# Returns a goal that is GUARANTEED to be reachable
	# Goal is a 'high level goal', ie a tuple in the format:
	#		goal = ( <goal type>, <goal position> )
	# NOTE: This may conduct multiple A* searches to determine whether a goal is reachable.
	def determineGoal(self):

		# Case when we have the gold - set starting position to be goal
		if (gs.TILE_GOLD in self.curr_items):
			return (self.GOALTYPE_REACH, self.gameboard.start_position)
			
		# Prioritise other goals
		else:

			# Check whether the gold can be seen on the map
			goldPos = self.gameboard.getGoldPos()
			if not (self.equalPosition(goldPos, self.gameboard.null_position)):
				print "Gold is foun"

				# Check for gold reachability
				if self.isReachable(goldPos, self.gameboard.curr_position):
					return (self.GOALTYPE_GET_ITEM, goldPos)
				else:
					return (self.GOALTYPE_EXPLORE, self.getExplorePosition())

			# Gold cannot be seen - explore
			else:
				explorePosition = self.getExplorePosition()
				return (self.GOALTYPE_EXPLORE, explorePosition)

	# Return a 'most promising' position to reach on the map for the purpose
	# of:
	#	* expanding the map
	#	* getting more detail about area around a specific position
	# NOTE: Should ALWAYS return a reachable position
	def getExplorePosition(self, *targetPos):

		finalExplorePosition = {}

		# Get list of reachable positions from current position
		reachablePoints = self.getReachablePoints(self.gameboard.curr_position, self.gameboard)

		# DEBUGGING
		print "Reachable points from current position:"
		print reachablePoints
		self.gameboard.showMap()

		# Choose a most promising candidate point, and set that to be the goal
		if len(reachablePoints) > 0:
			
			# Filter a list of reachable points of which there are adjacent unknown tiles
			candidatePointsUnknownAdj = self.getPointsAdj(reachablePoints, gs.TILE_UNKNOWN)
			if len(candidatePointsUnknownAdj) > 0:
				return self.getClosestPosition(self.gameboard.curr_position, candidatePointsUnknownAdj)

			# Case when there are no reachable tiles that are adjacent to unknown tiles
			# Find a tile within the reachable points that is located on the edge of the map
			candidatePointsEdgeLoc = self.getPointsLoc(reachablePoints, self.gameboard.LOCATION_EDGE)
			if len(candidatePointsEdgeLoc) > 0:
				return self.getClosestPosition(self.gameboard.curr_position, candidatePointsEdgeLoc)

			# At this point, there are no tiles with adj unknown tiles, and blank squares on edge of map.
			# Choose a random boundary-reachable point
			# Note: There should ALWAYS be one
			candidatePointsBoundary = self.getPointsBoundary(reachablePoints)
			if len(candidatePointsBoundary) > 0:
				finalExplorePosition = candidatePointsBoundary[random.randint(0,len(candidatePointsBoundary)-1)]
				while self.equalPosition(finalExplorePosition, self.gameboard.curr_position):
					finalExplorePosition = reachablePoints[random.randint(0,len(reachablePoints)-1)]
				return finalExplorePosition

			# For some reason, ended up here where above cases are not possible: Pick a random position
			finalExplorePosition = reachablePoints[random.randint(0,len(reachablePoints)-1)]
			while self.equalPosition(finalExplorePosition, self.gameboard.curr_position):
				finalExplorePosition = reachablePoints[random.randint(0,len(reachablePoints)-1)]
			return finalExplorePosition

		# Return final explore position (setting it to the start position if none are found)
		if finalExplorePosition:
			return finalExplorePosition
		else:
			return self.gameboard.start_position

	# Determine whether a position is reachable from a current position in the current map
	# using the flood fill algorithm
	def isReachable(self, pos, currPos):
		reachablePoints = self.getReachablePoints(currPos, self.gameboard)
		if self.pointExists(pos, reachablePoints):
			return True
		return False

	# Given a list of positions on the map, determine which are the ones adjacent to
	# a specific tile
	def getPointsAdj(self, posList, tile):
		pointsAdj = []			# Holds the final return positions
		for pos in posList:
			if self.gameboard.hasAdjacent(pos, tile):
				pointsAdj.append(pos)
		return pointsAdj

	# Given a list of positions on the map, determine which are the ones located 
	# in a particular location on the map (type specified in gameboard)
	def getPointsLoc(self, posList, loc):
		pointsLoc = []			# Holds the final return positions
		for pos in posList:
			if self.gameboard.located(pos, loc):
				pointsLoc.append(pos)
		return pointsLoc

	# Given a list of reachable positions, return the ones that are deemed 'boundary-reachable' 
	# (ie a point that is on the boundary of the area that is reachable).
	# More specifically, defined as:
	#		* a square with less than 4 adjacent tiles
	# or 	* adjacent tiles have a wall, water, or map edge tile
	# or	* adjacent tiles have a tree while axe not in possession
	# or	* adjacent tiles have a door while key not in possession
	def getPointsBoundary(self, posList):
		pointsBoundary = []
		for pos in posList:
			adjacentTilePos = self.gameboard.getAdjacentSquares(pos)
			adjacentTileTypes = [ self.gameboard.getTile(adjPos) for adjPos in adjacentTilePos ]
			if (len(adjacentTilePos) < 4) or \
				(gs.TILE_WALL in adjacentTileTypes) or \
				(gs.TILE_MAP_EDGE in adjacentTileTypes) or \
				(gs.TILE_WATER in adjacentTileTypes) or \
				( (gs.TILE_TREE in adjacentTileTypes) and (gs.TILE_AXE not in self.curr_items) ) or \
				( (gs.TILE_DOOR in adjacentTileTypes) and (gs.TILE_KEY not in self.curr_items) ):
				
				pointsBoundary.append(pos)
		return pointsBoundary

	# Return the position that's shortest in distance to the given position
	# NOTE: Returns a position OTHER than the given position
	def getClosestPosition(self, givenPos, posList):

		# Prepare the variables
		minDist = -1
		closestPos = { 'x': -1, 'y': -1 }
		x1 = givenPos['x']
		y1 = givenPos['y']
		
		# loop through each position in list to determine minimum
		for pos in posList:
			if (self.equalPosition(givenPos, pos)):
				continue
			x2 = pos['x']
			y2 = pos['y']
			dist = math.sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1))
			if (minDist == -1) or (minDist > dist):
				minDist = dist
				closestPos = pos
		return closestPos	
	

	# ----------------------------------
	# NODE SEARCHING FUNCTIONS
	# ----------------------------------
	
	# Perform A* search on current gameboard to determine list of actions to reach a given high level goal
	def getReachGoalActions(self, goal, gameboard):

		# Parse the goal type and the position associated with the goal
		goalType, goalPos = goal

		# Prepare priority queue
		nodepq = PriorityQueue()

		# Create a virtual gameboard of the initial gameboard state
		vgameboard = VirtualGameboard(gameboard, self.curr_items, goalPos)

		# Append initial node to queue
		node = SearchNode(vgameboard, 0, None)	# 0 = no previous action; None = No previous node
		nodepq.put(node)

		# DEBUGGING
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
			#node.show()

			# Compare the agent's position AND direction in the case when highLevelGoal is of type 'ELIMINATE_OBSTACLE'
			if self.equalPosition(node.vgameboard.curr_position, goalPos):

				# DEBUGGING
				print "Final position:"
				node.show()

				# Backtrack list of nodes to get final list of actions
				while not node.prevNode == None:
					final_action_list.append(node.action)
					node = node.prevNode

				final_action_list.reverse()

				# DEBUGGING
				print "Final list of actions are:"
				print final_action_list

				return final_action_list
			else:
	
				# Determine list of possible actions from the simulated situation
				possible_actions = self.mv.getAllValidMoves(node.vgameboard.items, node.vgameboard.gamemap)

				#print "Possible actions:"
				#print possible_actions

				# For each possible action, create a node and insert into priority queue
				for action in possible_actions:
					tempvgameboard = deepcopy(node.vgameboard)
					tempvgameboard.simulate(action)
					newNode = SearchNode(tempvgameboard, action, node)

					# Put iff newNode doesn't currently exist in list of nodes
					if self.exists(newNode, node_list):
						""" Ignore """
					else:
						nodepq.put(newNode, newNode.eval_cost)
						node_list.append(newNode)

		# DEBUGGING
		print "Darn, no path was found."
		return []

	# Perform flood fill algorithm over the map to determine a list of reachable points
	# from a given start position.
	# The 'target colour' is curently the blank tile.
	def getReachablePoints(self, startPos, gameboard):

		# Final return list
		reachablePoints = []	# Position given is assumed to be reachable

		# For searching
		pointsToProcess = []
		directionList = [ gameboard.DIRECTION_UP, gameboard.DIRECTION_RIGHT, gameboard.DIRECTION_DOWN, gameboard.DIRECTION_LEFT ]

		# Begin flood fill algorithm
		pointsToProcess.append(startPos)
		while len(pointsToProcess) > 0:
			processPoint = pointsToProcess.pop(0)

			# Check that point being considered is valid
			if (gameboard.isValidPosition(processPoint)):

				if (gameboard.getTile(processPoint) in gs.player_icons) or \
				   (self.isTargetColour(processPoint, gameboard)):
				   
					reachablePoints.append(processPoint)

					# Construct the list of points that are from the four directions of process point
					movedPoints = [ gameboard.movePoint(processPoint, direction) for direction in directionList ]

					# Consider each of the moved points with regard to the 'target colour'
					for movedPoint in movedPoints:

						# Add iff not: already processed, or to be processed
						if (not self.pointExists(movedPoint, reachablePoints)) and \
						(not self.pointExists(movedPoint, pointsToProcess)):
							pointsToProcess.append(movedPoint)

		return reachablePoints

	# Determine whether a position is of 'target colour' ie reachable
	def isTargetColour(self, pos, gameboard):
		tile = gameboard.getTile(pos)
		if (tile == gs.TILE_BLANK) or (tile == gs.TILE_USED_STEPPING_STONE):
			return True
		elif (tile in gs.item_list):
			return True
		elif (tile == gs.TILE_TREE):
			# Check for axe in possession
			if (gs.TILE_AXE in self.curr_items):
				return True
		elif (tile == gs.TILE_DOOR):
			# Check for key in possession
			if (gs.TILE_KEY in self.curr_items):
				return True

		# All other cases:
		else:
			return False

	# Compare two position points for equivalence
	# Both positions are given as points, in the format:
	# 	pos = { 'x': X, 'y': Y }
	def equalPosition(self, pos1, pos2):
		return ( (pos1['x'] == pos2['x']) and (pos1['y'] == pos2['y']) )

	# Check whether a search node is in a list of search nodes (equivalence)
	def exists(self, searchNode, nodeList):
		for node in nodeList:
			if self.equalVGameboards(node.vgameboard, searchNode.vgameboard):
				return True
		return False

	# Check whether a position exists in a list of positions
	# where position is of the format:
	#		pos = { 'x': X, 'y': Y }
	def pointExists(self, givenPos, posList):
		for pos in posList:
			if self.equalPosition(pos, givenPos):
				return True
		return False

	# Check for equivalence between virtual gameboards
	def equalVGameboards(self, vgameboard1, vgameboard2):

		# Direction
		if vgameboard1.direction != vgameboard2.direction:
			return False

		# Current position
		if not self.equalPosition(vgameboard1.curr_position, vgameboard2.curr_position):
			return False

		# Goal position
		if not self.equalPosition(vgameboard1.goal_position, vgameboard2.goal_position):
			return False

		# Item list
		if not (set(vgameboard1.items) == set(vgameboard2.items)):
			return False
	
		# Gamemap
		if (len(vgameboard1.gamemap) != len(vgameboard2.gamemap)) or \
		   (len(vgameboard1.gamemap[0]) != len(vgameboard2.gamemap[0])):
			return False

		for i in range(0, len(vgameboard1.gamemap)):
			for j in range(0, len(vgameboard1.gamemap[i])):
				try:
					if (vgameboard1.gamemap[i][j] != vgameboard2.gamemap[i][j]):
						return False
				except IndexError:
					print "Error: Index i=%d j=%d not found." % (i,j)
		return True


# ----------------------------------
# SEARCH HELPER CLASSES
# ----------------------------------
# A simpler version of gameboard ie without starting position
# whose sole purpose is for nodes (to simulate the gameboard without changing the actual gameboard)
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

		# Check for any items lost
		# Case when tile in front is water, and we have a stepping stone
		#	 - Remove the stone
		if (self.getTile(newPos) == gs.TILE_WATER) and (gs.TILE_STEPPING_STONE in self.items):
			self.items.remove(gs.TILE_STEPPING_STONE)
	
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
	acc_cost = 0		# Accumulated cost to reach this node
	eval_cost = 0		# Heuristic + accumulated cost
	vgameboard = None	# Virtual gameboard
	prevNode = None
	
	# Constructor, given a virtual gameboard
	def __init__(self, vgameboard, action, prevNode):
		self.action = action				# A single char (if '0', init action)
		self.vgameboard = vgameboard			# Virtual gameboard
		self.prevNode = prevNode
		self.eval_cost = self.evaluateCost()		# Calculate the node cost based on gameboard

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

	# Calculate the heuristic value by analysing the gameboard's state
	# Currently based on:
	#	- Manhattan distance
	# 	- Whether agent should conduct any turns
	def getHeuristicValue(self):

		# Holds the final heuristic value
		finalHeuristicValue = 0

		# get details about goal and agent
		goalPos = self.vgameboard.goal_position
		agentPos = self.vgameboard.curr_position
		agentDir = self.vgameboard.direction

		# Prepare for the heuristic processing
		differenceX = agentPos['x'] - goalPos['x']
		differenceY = agentPos['y'] - goalPos['y']
	
		# Calculate manhattan distance
		manhatt_dist = abs(differenceX) + abs(differenceY)
		finalHeuristicValue += manhatt_dist

		# Check whether the agent needs to make at least 1 turn to reach the goal
		# ie make at least 1 turn if agent is in a different column AND row
		diffCol = not (abs(differenceX) == 0)
		diffRow = not (abs(differenceY) == 0)
		if (diffCol and diffRow):
			finalHeuristicValue += 1

		# Check whether the agent is facing in a 'general direction' to the goal.
		if (self.inGeneralDirection(goalPos, agentPos, agentDir)):

			# Check whether there is a wall / map edge in front of agent
			agentFrontPos = self.vgameboard.movePoint(agentPos, agentDir)
			if self.vgameboard.getTile(agentFrontPos) in [gs.TILE_WALL, gs.TILE_MAP_EDGE]:
				finalHeuristicValue += 1
		
		# Case when agent is not facing the 'general direction' to goal - need to turn at least once
		else:
			finalHeuristicValue += 1

		return finalHeuristicValue

	# Cost to reach this node based on the cost of the action itself
	# Accumulates on the previous node
	def getReachCost(self):
		if (self.prevNode == None):
			self.acc_cost = 0
			return 0
		else:
			return (self.prevNode.acc_cost + 1)

	# Determine whether an object is facing in a 'general direction' to a goal position
	# Returns 'True' or 'False'
	# By general direction, it means:
	#	* If goalPos is North East (NE) of object WHILE object is facing forward or right
	#	* If goalPos is North West (NW) of object WHILE object is facing forward or left
	#	* If goalPos is South East (SE) of object WHILE object is facing down or right
	#	* If goalPos is South West (SW) of object WHILE object is facing down or left
	# Note: both goalPos and objectPos are positions
	def inGeneralDirection(self, goalPos, objectPos, objectDir):

		# Get the difference in values of column (x) and row (y)
		differenceX = objectPos['x'] - goalPos['x']
		differenceY = objectPos['y'] - goalPos['y']

		# Case when goal is NE of agent
		if differenceX < 0 and differenceY > 0:
			if objectDir in [self.vgameboard.DIRECTION_UP, self.vgameboard.DIRECTION_RIGHT]:
				return True
			else:
				return False

		#Case when goal is NW of agent
		elif differenceX > 0 and differenceY > 0:
			if objectDir in [self.vgameboard.DIRECTION_UP, self.vgameboard.DIRECTION_LEFT]:
				return True
			else:
				return False

		#Case when goal is SE of agent
		elif differenceX < 0 and differenceY < 0:
			if objectDir in [self.vgameboard.DIRECTION_DOWN, self.vgameboard.DIRECTION_RIGHT]:
				return True
			else:
				return False

		#Case when goal is SW of agent
		elif differenceX > 0 and differenceY < 0:
			if objectDir in [self.vgameboard.DIRECTION_DOWN, self.vgameboard.DIRECTION_LEFT]:
				return True
			else:
				return False		
