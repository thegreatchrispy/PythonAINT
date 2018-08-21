import pygame, sys
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BARWIDTH = 100
BOXSIZE = 40
BOXMARGIN = 5
BOXNUMBERWIDTH = 2
COLORHEIGHT = WINDOWHEIGHT / 2
TOOLHEIGHT = WINDOWHEIGHT / 2

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHTBLUE = (25, 212, 255)

BGCOLOR = WHITE
BARCOLOR = GRAY

FILL = 'fill'
LINE = 'line'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, WHITE, BLACK)
ALLTOOLS = (FILL, LINE)
# These asserts may be temporary...
assert len(ALLCOLORS) % 2 == 0, 'Must have an even number of colors'
assert len(ALLTOOLS) % 2 == 0, 'Must have an even number of tools'


def main():
	global FPSCLOCK, DISPLAYSURF
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

	mousex = 0
	mousey = 0
	pygame.display.set_caption('Draw Window')
	selectedColor = generateSelectedBoxes(ALLCOLORS)
	selectedTool = generateSelectedBoxes(ALLTOOLS)
	selectedBoxes = [selectedColor, selectedTool]
	currentColor = WHITE
	DISPLAYSURF.fill(BGCOLOR)
	
	while True:
		DISPLAYSURF.fill(currentColor)
		mouseClicked = False
		drawColorBar()
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mousex, mousey = event.pos
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				mouseClicked = True

		boxx, boxy = getBoxAtPixel(mousex, mousey)

		if mousey < WINDOWHEIGHT / 2:
			selector = 0
		elif mousey >= WINDOWHEIGHT / 2:
			selector = 1

		if boxx != None and boxy != None:
			if not selectedBoxes[selector][boxx][boxy]:
				drawHighlightBox(boxx, boxy)

			if not selectedBoxes[selector][boxx][boxy] and mouseClicked:
				for col in selectedBoxes[selector]:
					for index, cell in enumerate(col):
						if cell == True:
							col[index] = False

				selectedBoxes[selector][boxx][boxy] = True
		elif boxx == None and boxy == None and mouseClicked:
			# currentColor = getCurrentSelection(selectedBoxes[0])
			# currentTool = getCurrentSelection(selectedBoxes[1])
			currentColor = RED
			currentTool = FILL

			if currentTool == FILL and mouseClicked:
				DISPLAYSURF.fill(currentColor)
				drawColorBar()
				pygame.display.update()

	pygame.display.update()
	FPSCLOCK.tick(FPS)

def leftTopCoordsOfBox(boxx, boxy):
	left = boxx * BOXSIZE + BOXMARGIN
	top = boxy * BOXSIZE + BOXMARGIN
	return (left, top)

def generateSelectedBoxes(tuple):
	selectedBoxes = []
	for i in range(BOXNUMBERWIDTH):
		selectedBoxes.append([False] * -(-len(tuple) // 2))
	selectedBoxes[0][0] = True
	return selectedBoxes

def getBoxAtPixel(x, y):
	for boxx in range(BOXNUMBERWIDTH):
		for boxy in range(-(-len(ALLCOLORS)//2)+(-(-len(ALLTOOLS)//2))):
			left, top = leftTopCoordsOfBox(boxx, boxy)
			boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
			if boxRect.collidepoint(x, y):
				return (boxx, boxy)
	return (None, None)

def drawColorBar():
	i = 0
	pygame.draw.rect(DISPLAYSURF, BARCOLOR, (0, 0, BARWIDTH, WINDOWHEIGHT))
	for boxx in range(BOXNUMBERWIDTH):
		for boxy in range(-(-len(ALLCOLORS)//2)):
			left, top = leftTopCoordsOfBox(boxx, boxy)
			pygame.draw.rect(DISPLAYSURF, ALLCOLORS[i], (left, top, BOXSIZE, BOXSIZE))
			i += 1

def drawHighlightBox(boxx, boxy):
	left, top = leftTopCoordsOfBox(boxx, boxy)
	pygame.draw.rect(DISPLAYSURF, LIGHTBLUE, (left - BOXMARGIN, top - BOXMARGIN, BOXSIZE + BOXMARGIN * 2, BOXSIZE + BOXMARGIN * 2))
	pygame.display.update()

if __name__ == '__main__':
	main()
