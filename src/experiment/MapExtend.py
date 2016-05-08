#! /usr/bin/python
import sys

def resetGamemap(gamemap):
	gamemap = [["c", "c", "c"],["d", "d", "d"],["e", "e", "e"]]
	return gamemap

def showGamemap(gamemap):
	print "+-----+"
	for i in range(0,len(gamemap)):
		sys.stdout.write("|")
		for j in range(0,len(gamemap[i])):
			sys.stdout.write(gamemap[i][j])
		print "|"
	print "+-----+"
def expandRight(gamemap):
	numRow = len(gamemap)
	for i in range(0,numRow):
		gamemap[i].append("?")

def expandLeft(gamemap):
	numRow = len(gamemap)
	for i in range(0,numRow):
		gamemap[i] = ["?"] + gamemap[i]

## [?] + [currentlist ... ]
def expandTop(gamemap):
	newYRow = []
	numCol = len(gamemap[0])
	for i in range(0,numCol):
		newYRow.append('?')
	gamemap.insert(0, newYRow)

def expandBottom(gamemap):
	newYRow = []
	numCol = len(gamemap[0])
	for i in range(0,numCol):
		newYRow.append('?')
	gamemap.append(newYRow)

if __name__ == '__main__':

	print "+++ original gamemap +++"
	gamemap = [["c", "c", "c"],["d", "d", "d"],["e", "e", "e"]]
	showGamemap(gamemap)

	print "+++ expandRight +++"
	expandRight(gamemap)
	showGamemap(gamemap)

	gamemap = [["c", "c", "c"],["d", "d", "d"],["e", "e", "e"]]
	print "+++ expandLeft +++"
	expandLeft(gamemap)
	showGamemap(gamemap)
	
	gamemap = [["c", "c", "c"],["d", "d", "d"],["e", "e", "e"]]
	print "+++ expandTop +++"
	expandTop(gamemap)
	showGamemap(gamemap)
	
	gamemap = [["c", "c", "c"],["d", "d", "d"],["e", "e", "e"]]
	print "+++ expandBottom +++"
	expandBottom(gamemap)
	showGamemap(gamemap)

	print "++++++++++++++++++++++"
	gamemap = [["c", "c", "c"],["d", "d", "d"],["e", "e", "e"]]
	print "+++ 2x expandRight +++"
	expandRight(gamemap)
	expandRight(gamemap)
	showGamemap(gamemap)

	gamemap = [["c", "c", "c"],["d", "d", "d"],["e", "e", "e"]]
	print "+++ 2x expandLeft +++"
	expandLeft(gamemap)
	expandLeft(gamemap)
	showGamemap(gamemap)
	
	gamemap = [["c", "c", "c"],["d", "d", "d"],["e", "e", "e"]]
	print "+++ 2x expandTop +++"
	expandTop(gamemap)
	expandTop(gamemap)
	showGamemap(gamemap)
	
	gamemap = [["c", "c", "c"],["d", "d", "d"],["e", "e", "e"]]
	print "+++ 2x expandBottom +++"
	expandBottom(gamemap)
	expandBottom(gamemap)
	showGamemap(gamemap)

	print "++++++++++++++++++++++"
	gamemap = [["c", "c", "c"],["d", "d", "d"],["e", "e", "e"]]
	print "+++ expandRightLeft +++"
	expandRight(gamemap)
	expandLeft(gamemap)
	showGamemap(gamemap)

	gamemap = [["c", "c", "c"],["d", "d", "d"],["e", "e", "e"]]
	print "+++ expandTopBottom +++"
	expandTop(gamemap)
	expandBottom(gamemap)
	showGamemap(gamemap)
	
	gamemap = [["c", "c", "c"],["d", "d", "d"],["e", "e", "e"]]
	print "+++ expandTopRight +++"
	expandTop(gamemap)
	expandRight(gamemap)
	showGamemap(gamemap)
	
	gamemap = [["c", "c", "c"],["d", "d", "d"],["e", "e", "e"]]
	print "+++ expandTopLeft +++"
	expandTop(gamemap)
	expandLeft(gamemap)
	showGamemap(gamemap)

	gamemap = [["c", "c", "c"],["d", "d", "d"],["e", "e", "e"]]
	print "+++ expandTopRight +++"
	expandTop(gamemap)
	expandRight(gamemap)
	showGamemap(gamemap)
	
	gamemap = [["c", "c", "c"],["d", "d", "d"],["e", "e", "e"]]
	print "+++ expandTopLeft +++"
	expandTop(gamemap)
	expandLeft(gamemap)
	showGamemap(gamemap)

	gamemap = [["c", "c", "c"],["d", "d", "d"],["e", "e", "e"]]
	print "+++ expandBottomRight +++"
	expandBottom(gamemap)
	expandRight(gamemap)
	showGamemap(gamemap)
	
	gamemap = [["c", "c", "c"],["d", "d", "d"],["e", "e", "e"]]
	print "+++ expandBottomLeft +++"
	expandBottom(gamemap)
	expandLeft(gamemap)
	showGamemap(gamemap)

	gamemap = [["c", "c", "c"],["d", "d", "d"],["e", "e", "e"]]
	print "+++ last test for ian +++"
	expandBottom(gamemap)
	expandLeft(gamemap)
	expandTop(gamemap)
	expandRight(gamemap)
	showGamemap(gamemap)
	exit(0)
