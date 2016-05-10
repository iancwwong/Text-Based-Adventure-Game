# This is the class that represents the decision making component of the agent

#! /usr/bin/python

import GameSymbols as gs
import Gameboard

class DecisionMaker(object):


	# # Constants
	# ACTION_FORWARD = 'f'
	# ACTION_RIGHT = 'r'
	# ACTION_LEFT = 'l'
	# ACTION_CHOP = 'c'
	# ACTION_UNLOCK = 'u'

	# Attributes
	past_actions = []		# a list of past actions (consisting of single chars)
	todo_actions = []		# a list of actions to perform
	curr_items = []			# a list of items we currently possess
	gameboard = None

	# Constructor
	def __init__(self, gameboard):
		self.past_actions = []
		self.gameboard = gameboard


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
		return gs.ACTION_FORWARD
