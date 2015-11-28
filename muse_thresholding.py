#Created by Joey Maalouf pair programming with Gabriel Butterick 
#Takes in data from the Muse headset and compares it to thresholds determined by the callibration code.
# from grid_display import GridDisplay
from muse_calibration import MuseCalibrationServer
from Maze.MazeGui import MazeGUI
from liblo import *
import sys
import time


class MuseControlServer(ServerThread):
  #Data gathering setup
  def __init__(self, port = 5002, mean = 850, deviation = 80, sleep_timer = 150):
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
  #Sets up the particular sensors we use
  def eeg_callback(self, path, args):
    (l_ear, l_forehead, r_forehead, r_ear) = args
    x_change = y_change = True
#Resets sleep mode to be inactive. Sleep mode is used to keep the program from reacting too quickly to inputs
    if self.sleep_counter >= self.sleep_timer:
      self.sleep_counter = 0
      self.sleeping = False
#Determines the direction the user is looking
    if not self.sleeping:
      if r_ear < (self.mean - self.deviation):
        if r_ear > self.prev_re:
          if r_ear < (self.mean - 2.75 * self.deviation):
            self.exit = True # blink
          else:
            self.y = -1 # up
          self.sleeping = True
      elif r_ear > (self.mean + self.deviation):
        self.y = 1 # down
        self.sleeping = True
      else:
        y_change = False
      if l_forehead < (self.mean - self.deviation):
        self.x = 1 # right
        self.sleeping = True
      elif l_forehead > (self.mean + self.deviation):
        self.x = -1 # left
        self.sleeping = True
      else:
        x_change = False
      if not (x_change or y_change):
        self.x = self.y = 0 # center
    else:
      self.sleep_counter += 1
    self.prev_re = r_ear


if __name__ == "__main__":
  calib_server = MuseCalibrationServer()
  calib_server.start()
  calib_server.calibrate()
  calib_server.stop()
  print("Calibrated to {}, {}".format(calib_server.mean, calib_server.deviation))

  control_server = MuseControlServer(mean = calib_server.mean, deviation = calib_server.deviation)
  # gd = GridDisplay()
 #Initiates the test maze
  mg = MazeGUI()
  control_server.start()
  while True:
    # gd.update(control_server.x, control_server.y)
    mg.get_muse_input(control_server.x, control_server.y, control_server.exit)
    # gd.display()
    mg.display()
    if control_server.exit:
      break
    time.sleep(0.25)
  control_server.stop()
  sys.exit()
