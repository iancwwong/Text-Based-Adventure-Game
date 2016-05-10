#!/usr/bin/python

# -------------------------------------------------------
#  agent.py
#  Agent for Text-Based Adventure Game
#  COMP3411 Artificial Intelligence
#  UNSW Session 1, 2016
#  Written by: Ian Wong
#  Date: 26/04/2016
# -------------------------------------------------------

import socket
from sys import argv
from Gameboard import Gameboard

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
	agentsocket	# Communicates with the game engine
	conn_alive	# Flag representing connection state

	view		# contains the 5x5 view from the agent's perspective
	direction	# tracks the agent's direction
	items		# tracks the agent's current possessed items
	gameboard	# Component that keeps track of the map known so far (built from views)
	decisionmaker 	# Component that makes decisions for the agent
	
	
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
		self.decisionmaker = DecisionMaker()
		
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
		self.gameboard.showMap()

		while (self.conn_alive):
			try:			
				# Read input
				userInput = raw_input('Enter Action(s): ')

				# Send the input
				self.submitDecision(userInput)
				print ""	# formatting

				# Obtain the view
				newView = self.readView()

				# Update the map if the view has changed
				# Also may be an indication that last action was successful
				if not self.equalViews(self.view, newView):

					# Add the decision to past decisions list
					self.decisionmaker.addPastAction(userInput)
		
					# Check for any items that have been obtained
					self.checkForObtainedItems(newView)
	
					# Update the view and gamemap
					self.view = newView
					self.gameboard.updateMap(self.view, userInput)

					# DEBUGGING
					print "Current items:"
					print self.items

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
					viewJ.append('^')	# agent
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

	# Examines the new view to see if the user has picked up any items
	# and Update the items list as appropriately
	# Condition for picking up an item: 
	#	1. An item existed in the tile in front of the player in the previous view
	#	2. The last action to be made was 'move forward' (assumes this was successful)
	def checkForObtainedItems(self):
		if (self.hasItem(self.view, (1,2))) and (self.decisionmaker.getLatestAction() == 'f'):
			
			# Obtain and append the item to item list
			self.items.append(self.view[1][2])

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

	# Check whether a particular position (supplied as a tuple) in a view contains an item
	# ie an axe ('a'), key ('k'), gold ('g'), or stepping stone ('o')
	def hasItem(self, view, pos):
		row, col = pos
		if (view[row][col] == 'a' or view[row][col] == 'k' or view[row][col] == 'g' or view[row][col] == 'o'):
			return True
		return False

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
