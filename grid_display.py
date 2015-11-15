import numpy as np
import pygame
import sys


class GridDisplay(object):
  def __init__(self, size = 640):
    super(GridDisplay, self).__init__()
    pygame.init()
    self.size = size
    self.screen = pygame.display.set_mode((self.size, self.size))
    self.grid = np.zeros((3, 3), dtype = bool)

  def update(self, x, y):
    self.grid[np.nonzero(self.grid)] = False # reset grid
    self.grid[x+1, y+1] = True # translate inputs of -1, 0, 1 to 0, 1, 2 for indices

  def display(self):
    for i, row in enumerate(self.grid):
      for j, val in enumerate(row):
        self.screen.fill(
          pygame.Color(0, 255 if val else 0, 0),
          pygame.Rect(j*self.size/3, i*self.size/3, self.size/3, self.size/3)
        )
    pygame.display.flip()


def process_keys():
  x = y = 0
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        sys.exit()
      elif event.key == pygame.K_w: x = -1
      elif event.key == pygame.K_s: x =  1
      elif event.key == pygame.K_a: y = -1
      elif event.key == pygame.K_d: y =  1
  return x, y


if __name__ == "__main__":
  import time
  gd = GridDisplay()
  while True:
    x, y = process_keys()
    gd.update(x, y)
    gd.display()
    time.sleep(0.1)
