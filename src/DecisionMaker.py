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
		if len(todo_actions) == 0:
			self.determineActions()
		return todo_actions.pop(0)

	# determine the most appropriate action to perform next at any given time
	def determineActions(self):
		# determine our goal - find gold position
		# consult gameboard for the answer to the question of life

		# what is more important to look for/get
		for(i in range(0, self.gameboard.newRows())):
			for(j in range(0, self.gameboard.newRows())):
				currpoint = {"x" : i, "y" : j}
				# if self.gameblahblah == pq.head
				if(self.gameboard.getTile(currpoint) == GameSymbols.TILE_GOLD):
					return currpoint


		# when we lo gameboard gives us a way
		# determine a set of vaild actions we can perform to get to the gold position

		# determine a list of actions so we can look for a way to happiness


		#return self.IANISANOOBATLEAGUE

	# update the current list of items we have in the list
	def updateCurrItems(self, items):
		self.curr_items = items
