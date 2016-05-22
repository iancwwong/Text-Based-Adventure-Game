# This class represents a node when using the flood fill algorithm

class FloodFillNode(object):

	# Attributes
	pos = {}			# Position of node in the format {'x': X, 'y': Y}
	items = []		# List of items possessed at this node

	def __init__(self, nodePos, itemlist):
		self.pos = nodePos
		self.items = itemlist