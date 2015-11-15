import pygame
from pygame.locals import *
import WilsonsAlgorithm
from time import sleep

width = 5
height = 5
scale = 75

N, S, E, W = 1, 2, 4, 8 #Flags for encoding connection
DX =       {E:1, W:-1, N:0, S:0}
DY =       {E:0, W:0, N:-1, S:1}
OPPOSITE = {E:W, W:E, N:S, S:N}

screen = pygame.display.set_mode((width*scale, height*scale))
#screen = pygame.display.set_mode((300, 100))
clock = pygame.time.Clock()
BACKGROUND = (0,0,0)

def checkExit(events):
    for event in events:
        if event.type == pygame.QUIT:
            return True
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            return True
    return False

def loadTiles():
	tiles = []
	for i in range(16):
		tile = pygame.transform.scale(pygame.image.load("./maze-tiles/" + str(i) + ".png"), (scale,scale))
		tiles.append(tile)
	return tiles

def loadLines():
	lines = [1, 2, 4, 5, 8, 9, 3, 6, 10, 12]
	linepics = {}
	for i in lines:
		linepics[i] = pygame.transform.scale(pygame.image.load("./maze-tiles/line" + str(i) + ".png"), (scale,scale))
	return linepics

def mainLoop():
	maze = WilsonsAlgorithm.generate_maze(width, height)
	WilsonsAlgorithm.print_maze(maze)
	exiting = False
	tiles = loadTiles()
	lines = loadLines()
	x, y = 0, 0
	path = []
	while not exiting:
		#screen.fill(BACKGROUND)
		display_maze(maze, tiles)
		events = pygame.event.get()
		path, x, y = get_key_input(path,x,y,maze,events)
		display_path(path, lines)
		pygame.display.flip()
		print x, y
		if x == width-1 and y == height-1:
			print "exiting"
			wintext = pygame.image.load("./maze-tiles/wintext.png")
			print 374.0/(width*scale)
			wintext = pygame.transform.scale(wintext, (width*scale, int(height*scale*((width*scale)/374.0))))
			screen.blit(wintext, (0,(height-int(height*((width*scale)/374.0)))/2))
			pygame.display.flip()
			sleep(3)
			break
		exiting = checkExit(events)

def gameOver():
  start_time = pygame.time.get_ticks()
  delay = 3*1000 #Number of seconds, times 1000, because the program returns in miliseconds
  endText = game_over_font.render("You Win!", 1, (0,0,0))
  while pygame.time.get_ticks() < (start_time + delay):
    display.blit(endText, (470, 100))
    pygame.display.flip()
    clock.tick(60)


def display_maze(maze, tiles):
	for i in range(len(maze)):
			for j in range(len(maze[i])):
				screen.blit(tiles[maze[i][j]], pygame.Rect(i*scale, j*scale, scale, scale))

def get_key_input(path, x, y, maze, events):
	''' Takes in 'path' as a list of values: each one of which
		is 1,2,4, or 8, corresponding to Up, Down, Right, Left
	'''
	for event in events:
		if event.type == pygame.KEYDOWN:
			print "Key_pressed"
			if event.key == pygame.K_LEFT and check_input(x,y,W,maze):
				x = x + DX[W]
				path.append(W)
				print "Left"
			elif event.key == pygame.K_RIGHT and check_input(x,y,E,maze):
				x = x + DX[E]
				path.append(E)
				print "Right"
			elif event.key == pygame.K_DOWN and check_input(x,y,S,maze):
				y = y + DY[S]
				path.append(S)
				print "Down"
			elif event.key == pygame.K_UP and check_input(x,y,N,maze):
				y = y + DY[N]
				path.append(N)
				print "Up"
	return path, x, y

def check_input(x, y, move, maze):
	possible = False
	if move == W and maze[x][y]>=8:
		possible = True
	elif move == E and maze[x][y]%8>=4:
		possible = True
	elif move == S and maze[x][y]%8%4>=2:
		possible = True
	elif move == N and maze[x][y]%8%4%2==1:
		possible = True
	return possible

def display_path(path, lines):
	x, y = 0, 0
	ball = pygame.transform.scale(pygame.image.load("./maze-tiles/current_pos.png"), (scale,scale))
	for i, move in enumerate(path):
		if i == 0:
			screen.blit(lines[move], (0,0))
			x, y = x + DX[move], y + DY[move]
		# elif i == (len(path)):
		# 	screen.blit(OPPOSITE[lines[move]], (x*scale, y*scale))
		else:
			if move == OPPOSITE[path[i-1]]:
				screen.blit(lines[move], (x*scale, y*scale))
			else:
				screen.blit(lines[move + OPPOSITE[path[i-1]]], (x*scale,y*scale))
			x, y = x + DX[move], y + DY[move]
	if len(path) > 0:
		screen.blit(lines[OPPOSITE[path[len(path)-1]]], (x*scale, y*scale))
	screen.blit(ball, (x*scale,y*scale))


	ball = pygame.transform.scale(pygame.image.load("./maze-tiles/Ball.png"), (scale,scale))
	screen.blit(ball, (0,0))
	screen.blit(ball, (width*scale-scale, height*scale-scale))

mainLoop()