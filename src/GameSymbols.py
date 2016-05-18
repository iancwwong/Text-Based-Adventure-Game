# This file contains a list of all the symbols and characters used for the game
# Namely actions, and tile characters

# Tiles
TILE_WALL = '*'
TILE_MAP_EDGE = '.'
TILE_WATER = '~'
TILE_DOOR = '-'
TILE_TREE = 'T'
TILE_BLANK = ' '
TILE_AXE = 'a'
TILE_KEY = 'k'
TILE_STEPPING_STONE = 'o'
TILE_USED_STEPPING_STONE = 'O'
TILE_GOLD = 'g'
TILE_START_POS = 's'
TILE_UNKNOWN = '?'
item_list = [ TILE_AXE, TILE_KEY, TILE_STEPPING_STONE, TILE_GOLD ]
obstacle_tile_list = [ TILE_WALL, TILE_DOOR, TILE_TREE ]
death_tile_list = [ TILE_WATER ]

# Constants
ACTION_FORWARD = 'f'
ACTION_RIGHT = 'r'
ACTION_LEFT = 'l'
ACTION_CHOP = 'c'
ACTION_UNLOCK = 'u'
action_list = [ ACTION_FORWARD, ACTION_RIGHT, ACTION_LEFT, ACTION_CHOP, ACTION_UNLOCK ]

# Player icon
PLAYER_UP = '^'
PLAYER_RIGHT = '>'
PLAYER_DOWN = 'v'
PLAYER_LEFT = '<'
player_icons = [ PLAYER_UP, PLAYER_RIGHT, PLAYER_DOWN, PLAYER_LEFT ]