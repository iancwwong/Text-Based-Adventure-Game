#!/usr/bin/python

# -------------------------------------------------------
#  agent.py
#  Agent for Text-Based Adventure Game
#  COMP3411 Artificial Intelligence
#  UNSW Session 1, 2016
#  Written by: Ian Wong and Jason Ng
#  Date: 26/04/2016
# -------------------------------------------------------

# The agent for this game is a game playing agent that uses a world model and decision making module to develop a strategy 
# to obtain the gold. The decision making module works based off goals - it determines goals (based off a basic decision making 
# flowchart involving different goal priorities such as getting the gold, and general exploration), and determines the list of 
# actions to reach that goal.

# Determining the goal involves the use of the 'flood fill' algorithm to determine reachable positions (considering the items). 
# Finding a path to the goal involves the use of 'A*' to find the series of actions that allows the agent to reach the goal, 
# which are submitted one by one to the game engine.
# We made a series of changes to the way the agent explores the map. Orginally, we attempted to use A* to check for reachability.
# However as the map became more complex, we found A* to be too slow. We then proceeded to use the flood-fill algorithm, which ended
# up being much more efficient. We also have a 'moveValidator', which is meant to be a general purpose (python) class that determines
# the validity of a move, given a particular map environment (to avoid recoding the rules in all other classes that may require move 
# validation).

import socket
from sys import argv
from Gameboard import Gameboard
from DecisionMaker import DecisionMaker
import GameSymbols as gs

# ---------------------------
# AGENT
# ---------------------------
class Agent(object):

	# Constants
	DIRECTION_UP = 1
	DIRECTION_DOWN = 2
	DIRECTION_LEFT = 3
	DIRECTION_LEFT = 4

	# Attributes
	agentsocket = None	# Communicates with the game engine
	conn_alive = False	# Flag representing connection state

	view = []		# contains the 5x5 view from the agent's perspective
	direction = 0		# tracks the agent's direction
	items = []		# tracks the agent's current possessed items
	gameboard = None	# Component that keeps track of the map known so far (built from views)
	decisionmaker = None 	# Component that makes decisions for the agent


	def __init__(self, portnum):
		# Create the TCP socket
		self.agentsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Connect to the game engine via localhost
		try:
			self.agentsocket.connect(('Localhost', portnum))
		except socket.error, e:
			print "Error connecting to server: %s" % e
			exit()

		self.conn_alive = True		# connection established with game engine

		# Prepare the view
		self.view = []

		# Set initial direction
		self.direction = self.DIRECTION_UP

		# Prepare item list
		self.items = []

		# Prepare the gameboard
		self.gameboard = Gameboard()

		# Prepare the decision maker
		self.decisionmaker = DecisionMaker(self.gameboard)

	# Run the main procedure of the agent
	def run(self):
		# Initialise the gameboard by reading in initial view

		# Obtain the view
		newView = self.readView()
		self.view = newView

		# Display the view
		self.displayView()

		# Update the map
		self.gameboard.updateMap(self.view, 'init')
		#self.gameboard.showMap()

		while (self.conn_alive):
			try:

				# DEBUG
				#user_action = raw_input('')

				# Generate an action
				action = self.decisionmaker.getAction()

				# Submit the action
				self.submitDecision(action)

				# Obtain the view
				newView = self.readView()

				# Update the map if action was successful
				if self.actionSuccessful(newView, action):

					# Add the decision to past decisions list
					self.decisionmaker.addPastAction(action)

					# Check for any items that have been obtained
					self.checkForObtainedItems()

					# Check for any items that have been used/discarded
					self.checkForUsedItems()

					# update the decisionmaker's current item list
					self.decisionmaker.updateCurrItems(self.items)

					# Update the view and gamemap
					self.view = newView
					self.gameboard.updateMap(self.view, action)

					# DEBUGGING
					print "Current items:"
					print self.items

					print "Actions taken:"
					print self.decisionmaker.getAllPastActions()

					print "Map:"
					self.gameboard.showMap()

				# Display the view
				print "View:"
				self.displayView()

			except socket.error:

				# Connection terminated. Exit
				self.agentsocket.close()
				self.conn_alive = False

	# Obtain the data for the agent view by reading in data stream, and parsing
	# into individual characters.
	def readView(self):
		viewI = []
		viewStr = []
		for i in range(0,5):
			viewJ = []
			for j in range(0,5):
				if (i != 2 or j != 2):
					ch = self.agentsocket.recv(1)
					if (ch == ''):
						# Connection terminated
						self.agentsocket.close()
						self.conn_alive = False
						exit()
					viewJ.append(ch)
				else:
					viewJ.append(gs.PLAYER_UP)	# agent as '^'
			viewI.append(viewJ)
		return viewI

	# Format and print out the view (with some formatting)
	# where view is a 5x5 list of lists
	# (each list containing one character)
	def displayView(self):
		viewStr = "+-----+\n"
		for i in range(0,len(self.view)):
			viewStr += "|"
			for j in range(0,len(self.view[i])):
				viewStr += self.view[i][j]
			viewStr += "|\n"
		viewStr += "+-----+"
		print viewStr

	# Check if the given (most recent) action was successful, meaning the environment has changed somehow.
	# An action is successful if:
	#	1. Action is a valid action (ie matches the specific action characters)
	#	2. The view has changed somehow (ie different)
	# OR	3. The action can be resolved by considering the rules of the game
	def actionSuccessful(self, newView, action):
		if (not self.actionValid(action)):
			return False
		elif (not self.equalViews(self.view, newView)):
			return True
		else:
			# Check whether the action changes the environment with its meaning to other tiles

			# Case when agent has walked into a wall
			if (self.hasWall(self.view, (1,2))) and (action == gs.ACTION_FORWARD):
				return False

			# Case when agent has walked into a tree
			elif (self.hasTree(self.view, (1,2))) and (action == gs.ACTION_FORWARD):
				return False

			# Case when agent has walked into a door
			elif (self.hasDoor(self.view, (1,2))) and (action == gs.ACTION_FORWARD):
				return False

			# Case when agent chops something OTHER than a tree
			elif (not self.hasTree(self.view, (1,2))) and (action == gs.ACTION_CHOP):
				return False

			# Case when agent unlocks something OTHER than a door
			elif (not self.hasDoor(self.view, (1,2))) and (action == gs.ACTION_UNLOCK):
				return False

			# Any other cases?
			# Otherwise, it should be a valid action
			else:
				return True


	# Examines the new view to see if the user has picked up any items
	# and Update the items list as appropriately
	# Condition for picking up an item:
	#	1. An item existed in the tile in front of the player in the previous view
	#	2. The last action to be made was 'move forward' (assumes this was successful)
	def checkForObtainedItems(self):
		if (self.hasItem(self.view, (1,2))) and (self.decisionmaker.getLatestAction() == gs.ACTION_FORWARD):

			# Obtain and append the item to item list
			self.items.append(self.view[1][2])

	# Examine for any items that have been used:
	# * Stepping stone
	def checkForUsedItems(self):

		# Discard stepping stone if we have moved forward into some water whilst having
		# a stepping stone in posession
		if (self.hasTile(self.view, (1,2), gs.TILE_WATER)) and \
		   (gs.TILE_STEPPING_STONE in self.items) and \
		   (self.decisionmaker.getLatestAction() == gs.ACTION_FORWARD):
			self.items.remove(gs.TILE_STEPPING_STONE)

	# ---------------------------
	# HELPER FUNCTIONS
	# ---------------------------

	# Compare two views for equivalence
	# Each view is a list of lists (5x5 2D array).
	# Returns true or false
	def equalViews(self, view1, view2):

		# Check if views are of 5x5, and that their lengths are equal
		if (len(view1) == 5) and (len(view2) == 5):
			for i in range(0,5):
				for j in range(0,5):
					if (view1[i][j] != view2[i][j]):
						return False
			return True
		else:
			return False

	# Sends the user input to game engine
	def submitDecision(self, userInput):
		# Send out the message
		try:
			self.agentsocket.send(userInput)
		except socket.error, e:
			print "Error sending: %s" % e
			self.conn_alive = False

	# Check if the action is defined
	def actionValid(self, action):
		return (action in gs.action_list)

	# Check whether a particular position (supplied as a tuple) in a view contains an item
	# ie an axe ('a'), key ('k'), gold ('g'), or stepping stone ('o')
	def hasItem(self, view, pos):
		row, col = pos
		if (view[row][col] == gs.TILE_AXE or view[row][col] == gs.TILE_KEY or \
		    view[row][col] == gs.TILE_GOLD or view[row][col] == gs.TILE_STEPPING_STONE):
			return True
		return False

	# Check whether a particular position (supplied as a tuple) in a view contains a wall
	def hasWall(self, view, pos):
		return (view[pos[0]][pos[1]] == gs.TILE_WALL)

	# Check whether a particular position (supplied as a tuple) in a view contains a tree
	def hasTree(self, view, pos):
		return (view[pos[0]][pos[1]] == gs.TILE_TREE)

	# Check whether a particular position (supplied as a tuple) in a view contains a door
	def hasDoor(self, view, pos):
		return (view[pos[0]][pos[1]] == gs.TILE_DOOR)

	def hasTile(self, view, pos, tile):
		return (view[pos[0]][pos[1]] == tile)

# ---------------------------
# MAIN
# ---------------------------

if __name__ == '__main__':
	BUFFER_SIZE = 1024

	# Extract arguments
	if (len(argv) < 3):
		print "Usage: python Agent.py -p [port number]"
		exit()
	script, portFlag, portnumString = argv
	portnum = int(portnumString)			# Where game engine is listening

	# Create and run the agent
	agent = Agent(portnum)
	agent.run()

	# Exit
	exit()
