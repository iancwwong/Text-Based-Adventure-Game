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

# ---------------------------
# AGENT
# ---------------------------

class Agent(object):
	
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

	# Run the main procedure of the agent
	def run(self):
		while (self.conn_alive):
			try:
				# Obtain the view
				self.readView()
		
				# Display the view
				self.displayView()
			
				# Read input
				userInput = raw_input('Enter Action(s): ')

				# Send the input
				self.processInput(userInput)

				print ""	# formatting

			except socket.error:

				# Connection terminated. Exit
				self.agentsocket.close()
				self.conn_alive = False

	# Obtain the data for the agent view
	# by reading in data stream, and parsing
	# into individual characters
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
		self.view = viewI

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

	# Sends the user input to game engine
	def processInput(self, userInput):
		# Send out the message
		try:
			self.agentsocket.send(userInput)
		except socket.error, e:
			print "Error sending: %s" % e
			self.conn_alive = False

# ---------------------------
# MAIN
# ---------------------------

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
