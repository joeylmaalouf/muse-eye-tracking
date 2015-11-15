import pygame
from pygame.locals import *
import WilsonsAlgorithm
from time import sleep


class MazeGUI(object):
  def __init__(self):
    super(MazeGUI, self).__init__()
    self.FILEPATH = "/".join(__file__.split("/")[:-1])
    self.width = 4
    self.height = 4
    self.scale = 100
    self.N, self.S, self.E, self.W = 1, 2, 4, 8 # Flags for encoding connection
    self.DX =       {self.E:1,      self.W:-1,     self.N:0,      self.S:0}
    self.DY =       {self.E:0,      self.W:0,      self.N:-1,     self.S:1}
    self.OPPOSITE = {self.E:self.W, self.W:self.E, self.N:self.S, self.S:self.N}
    self.screen = pygame.display.set_mode((self.width*self.scale, self.height*self.scale))
    self.maze = WilsonsAlgorithm.generate_maze(self.width, self.height)
    # WilsonsAlgorithm.print_maze(self.maze)
    self.exiting = False
    self.tiles = self.loadTiles()
    self.lines = self.loadLines()
    self.path = []
    self.playerx = 0
    self.playery = 0

  def display(self):
    self.display_maze()
    self.display_path()
    pygame.display.flip()
    if self.playerx == self.width-1 and self.playery == self.height-1:
      wintext = pygame.image.load(self.FILEPATH+"/maze-tiles/wintext.png")
      wintext = pygame.transform.scale(wintext, (self.width*self.scale, int(self.height*self.scale*((self.width*self.scale)/374.0))))
      self.screen.blit(wintext, (0,(self.height-int(self.height*((self.width*self.scale)/374.0)))/2))
      pygame.display.flip()
      sleep(3)
      self.exiting = True
    
  def checkExit(self, events):
    for event in events:
      if event.type == pygame.QUIT:
        self.exiting = True
      elif event.type == KEYDOWN and event.key == K_ESCAPE:
        self.exiting = True

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

  def display_maze(self):
    for i in range(len(self.maze)):
      for j in range(len(self.maze[i])):
        self.screen.blit(self.tiles[self.maze[i][j]], pygame.Rect(i*self.scale, j*self.scale, self.scale, self.scale))

  def get_key_input(self, events):
    for event in events:
      if event.type == pygame.KEYDOWN:
        # print "Key_pressed"
        if event.key == pygame.K_LEFT and self.check_input(self.playerx, self.playery, self.W):
          self.playerx += self.DX[self.W]
          self.path.append(self.W)
          # print "Left"
        elif event.key == pygame.K_RIGHT and self.check_input(self.playerx, self.playery, self.E):
          self.playerx += self.DX[self.E]
          self.path.append(self.E)
          # print "Right"
        elif event.key == pygame.K_DOWN and self.check_input(self.playerx, self.playery, self.S):
          self.playery += self.DY[self.S]
          self.path.append(self.S)
          # print "Down"
        elif event.key == pygame.K_UP and self.check_input(self.playerx, self.playery, self.N):
          self.playery += self.DY[self.N]
          self.path.append(self.N)
          # print "Up"

  def get_muse_input(self, dx, dy, exit = False):
    if (dx, dy) == (0, -1)and self.check_input(self.playerx, self.playery, self.N): # up
      self.playery += self.DY[self.N]
      self.path.append(self.N)
    elif (dx, dy) == (0, 1) and self.check_input(self.playerx, self.playery, self.S): # down
      self.playery += self.DY[self.S]
      self.path.append(self.S)
    elif (dx, dy) == (-1, 0) and self.check_input(self.playerx, self.playery, self.W): # left
      self.playerx += self.DX[self.W]
      self.path.append(self.W)
    elif (dx, dy) == (1, 0) and self.check_input(self.playerx, self.playery, self.E): # right
      self.playerx += self.DX[self.E]
      self.path.append(self.E)
    if exit:
      self.exiting = True

  def check_input(self, x, y, move):
    possible = False
    if move == self.W and self.maze[x][y]>=8:
      possible = True
    elif move == self.E and self.maze[x][y]%8>=4:
      possible = True
    elif move == self.S and self.maze[x][y]%8%4>=2:
      possible = True
    elif move == self.N and self.maze[x][y]%8%4%2==1:
      possible = True
    return possible

  def display_path(self):
    x, y = 0, 0
    ball = pygame.transform.scale(pygame.image.load(self.FILEPATH+"/maze-tiles/current_pos.png"), (self.scale, self.scale))
    for i, move in enumerate(self.path):
      if i == 0:
        self.screen.blit(self.lines[move], (0, 0))
        x, y = x + self.DX[move], y + self.DY[move]
      else:
        if move == self.OPPOSITE[self.path[i-1]]:
          self.screen.blit(self.lines[move], (x*self.scale, y*self.scale))
        else:
          self.screen.blit(self.lines[move + self.OPPOSITE[self.path[i-1]]], (x*self.scale, y*self.scale))
        x, y = x + self.DX[move], y + self.DY[move]
    if len(self.path) > 0:
      self.screen.blit(self.lines[self.OPPOSITE[self.path[len(self.path)-1]]], (x*self.scale, y*self.scale))
    self.screen.blit(ball, (x*self.scale,y*self.scale))

    ball = pygame.transform.scale(pygame.image.load(self.FILEPATH+"/maze-tiles/Ball.png"), (self.scale, self.scale))
    self.screen.blit(ball, (0, 0))
    self.screen.blit(ball, (self.width*self.scale-self.scale, self.height*self.scale-self.scale))


if __name__ == "__main__":
  mg = MazeGUI()
  while not mg.exiting:
    events = pygame.event.get()
    mg.get_key_input(events)
    mg.display()
    mg.checkExit(events)
