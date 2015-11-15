from grid_display import GridDisplay
from liblo import *
import sys
import time


class MuseServer(ServerThread):
  def __init__(self, port = 5001, mean = 850, deviation = 90, sleep_timer = 150):
    ServerThread.__init__(self, port)
    self.mean = mean
    self.deviation = deviation
    self.sleep_timer = sleep_timer
    self.sleep_counter = 0
    self.sleeping = False
    self.prev_re = mean
    self.x = 0
    self.y = 0
    self.exit = False

  @make_method("/muse/eeg", "ffff")
  def eeg_callback(self, path, args):
    (l_ear, l_forehead, r_forehead, r_ear) = args
    x_change = y_change = True

    if self.sleep_counter >= self.sleep_timer:
      self.sleep_counter = 0
      self.sleeping = False

    if not self.sleeping:
      if r_ear < (self.mean - self.deviation):
        if r_ear > self.prev_re:
          if r_ear < (self.mean - 2.75 * self.deviation):
            print "Blink", r_ear, self.mean - 2.75 * self.deviation
            self.exit = True
          else:
            print "Up", r_ear, self.mean - self.deviation
            self.y = -1
          self.sleeping = True
      elif r_ear > (self.mean + self.deviation):
        print "Down", r_ear, self.mean + self.deviation
        self.y = 1
        self.sleeping = True
      else:
        y_change = False
      if l_forehead < (self.mean - self.deviation):
        print "Right", l_forehead, self.mean - self.deviation
        self.x = 1
        self.sleeping = True
      elif l_forehead > (self.mean + self.deviation):
        print "Left", l_forehead, self.mean + self.deviation
        self.x = -1
        self.sleeping = True
      else:
        x_change = False
      if not (x_change or y_change):
        print "Center"
        self.x = self.y = 0
    else:
      self.sleep_counter += 1
    self.prev_re = r_ear


if __name__ == "__main__":
  try:
    server = MuseServer()
  except ServerError, err:
    print(str(err))
    sys.exit()

  gd = GridDisplay()
  server.start()
  while True:
    gd.update(server.x, server.y)
    gd.display()
    if server.exit:
      break
    time.sleep(0.05)
  server.stop()
  sys.exit()
