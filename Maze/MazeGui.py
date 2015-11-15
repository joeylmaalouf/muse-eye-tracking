import pygame
from pygame.locals import *
import WilsonsAlgorithm
from time import sleep


class MazeGUI(object):
  def __init__(self):
    super(MazeGUI, self).__init__()
    self.FILEPATH = "/".join(__file__.split("/")[:-1])
    self.width = 5
    self.height = 5
    self.scale = 75
    self.N, self.S, self.E, self.W = 1, 2, 4, 8 # Flags for encoding connection
    self.DX =       {self.E:1,      self.W:-1,     self.N:0,      self.S:0}
    self.DY =       {self.E:0,      self.W:0,      self.N:-1,     self.S:1}
    self.OPPOSITE = {self.E:self.W, self.W:self.E, self.N:self.S, self.S:self.N}
    self.screen = pygame.display.set_mode((self.width*self.scale, self.height*self.scale))

  def checkExit(self, events):
    for event in events:
      if event.type == pygame.QUIT:
        return True
      elif event.type == KEYDOWN and event.key == K_ESCAPE:
        return True
    return False

  def loadTiles(self):
    tiles = []
    for i in range(16):
      tile = pygame.transform.scale(pygame.image.load(self.FILEPATH+"/maze-tiles/" + str(i) + ".png"), (self.scale, self.scale))
      tiles.append(tile)
    return tiles

  def loadLines(self):
    lines = [1, 2, 4, 5, 8, 9, 3, 6, 10, 12]
    linepics = {}
    for i in lines:
      linepics[i] = pygame.transform.scale(pygame.image.load(self.FILEPATH+"/maze-tiles/line" + str(i) + ".png"), (self.scale, self.scale))
    return linepics

  def mainLoop(self):
    maze = WilsonsAlgorithm.generate_maze(self.width, self.height)
    WilsonsAlgorithm.print_maze(maze)
    exiting = False
    tiles = self.loadTiles()
    lines = self.loadLines()
    x, y = 0, 0
    path = []
    while not exiting:
      self.display_maze(maze, tiles)
      events = pygame.event.get()
      path, x, y = self.get_key_input(path,x,y,maze,events)
      self.display_path(path, lines)
      pygame.display.flip()
      if x == self.width-1 and y == self.height-1:
        wintext = pygame.image.load(self.FILEPATH+"/maze-tiles/wintext.png")
        wintext = pygame.transform.scale(wintext, (self.width*self.scale, int(self.height*self.scale*((self.width*self.scale)/374.0))))
        self.screen.blit(wintext, (0,(self.height-int(self.height*((self.width*self.scale)/374.0)))/2))
        pygame.display.flip()
        sleep(3)
        break
      exiting = self.checkExit(events)

  def display_maze(self, maze, tiles):
    for i in range(len(maze)):
      for j in range(len(maze[i])):
        self.screen.blit(tiles[maze[i][j]], pygame.Rect(i*self.scale, j*self.scale, self.scale, self.scale))

  def get_key_input(self, path, x, y, maze, events):
    for event in events:
      if event.type == pygame.KEYDOWN:
        # print "Key_pressed"
        if event.key == pygame.K_LEFT and self.check_input(x,y,self.W,maze):
          x = x + self.DX[self.W]
          path.append(self.W)
          # print "Left"
        elif event.key == pygame.K_RIGHT and self.check_input(x,y,self.E,maze):
          x = x + self.DX[self.E]
          path.append(self.E)
          # print "Right"
        elif event.key == pygame.K_DOWN and self.check_input(x,y,self.S,maze):
          y = y + self.DY[self.S]
          path.append(self.S)
          # print "Down"
        elif event.key == pygame.K_UP and self.check_input(x,y,self.N,maze):
          y = y + self.DY[self.N]
          path.append(self.N)
          # print "Up"
    return path, x, y

  def check_input(self, x, y, move, maze):
    possible = False
    if move == self.W and maze[x][y]>=8:
      possible = True
    elif move == self.E and maze[x][y]%8>=4:
      possible = True
    elif move == self.S and maze[x][y]%8%4>=2:
      possible = True
    elif move == self.N and maze[x][y]%8%4%2==1:
      possible = True
    return possible

  def display_path(self, path, lines):
    x, y = 0, 0
    ball = pygame.transform.scale(pygame.image.load(self.FILEPATH+"/maze-tiles/current_pos.png"), (self.scale, self.scale))
    for i, move in enumerate(path):
      if i == 0:
        self.screen.blit(lines[move], (0,0))
        x, y = x + self.DX[move], y + self.DY[move]
      # elif i == (len(path)):
      #   screen.blit(OPPOSITE[lines[move]], (x*scale, y*scale))
      else:
        if move == self.OPPOSITE[path[i-1]]:
          self.screen.blit(lines[move], (x*self.scale, y*self.scale))
        else:
          self.screen.blit(lines[move + self.OPPOSITE[path[i-1]]], (x*self.scale, y*self.scale))
        x, y = x + self.DX[move], y + self.DY[move]
    if len(path) > 0:
      self.screen.blit(lines[self.OPPOSITE[path[len(path)-1]]], (x*self.scale, y*self.scale))
    self.screen.blit(ball, (x*self.scale,y*self.scale))

    ball = pygame.transform.scale(pygame.image.load(self.FILEPATH+"/maze-tiles/Ball.png"), (self.scale, self.scale))
    self.screen.blit(ball, (0, 0))
    self.screen.blit(ball, (self.width*self.scale-self.scale, self.height*self.scale-self.scale))


if __name__ == "__main__":
  mg = MazeGUI()
  mg.mainLoop()
