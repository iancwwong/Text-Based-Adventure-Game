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
import select
from sys import argv

# ---------------------------
# FUNCTIONS
# ---------------------------

# Obtain the data for the agent view
# by reading in data stream, and parsing
# into individual characters
def readView():
	viewI = []
	viewStr = []
	for i in range(0,5):
		viewJ = []
		for j in range(0,5):
			if (i != 2 or j != 2):
				viewJ.append(agentsocket.recv(1))
			else:
				viewJ.append('')	# agent
		viewI.append(viewJ)
	return viewI

# Format and print out the view (with some formatting)
# where view is a 5x5 list of lists
# (each list containing one character)
def displayView(view):
	viewStr = "+-----+\n"
	for i in range(0,len(view)):
		viewStr += "|"
		for j in range(0,len(view[i])):
			if (i == 2 and j == 2):
				viewStr += '^'	# agent always facing upwards on the agent's screen
			else:
				viewStr += view[i][j]
		viewStr += "|\n"
	viewStr += "+-----+\n"
	print viewStr

# Use select module to read from socket
def selectRecv(bufferSize):
	listen_sockets = [agentsocket]
	read_sockets, write_sockets, error_sockets = select.select(listen_sockets, [], [])
	for rs in read_sockets:
		if (rs == agentsocket):
			data = agentsocket.recv(bufferSize)
			return data

# ---------------------------
# MAIN
# ---------------------------

BUFFER_SIZE = 1024

# Extract arguments
script, portFlag, portnumString = argv
portnum = int(portnumString)			# Where game engine is listening

# Create the TCP socket
agentsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the game engine via localhost
print "Connecting to game engine..."
try:
	agentsocket.connect(('Localhost', portnum))
except socket.error, e:
	print "Error connecting to server: %s" % e
	exit()

# Obtain and print the view
displayView(readView())

# Exit
agentsocket.close()
exit()
