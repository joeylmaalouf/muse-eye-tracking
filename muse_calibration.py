#Created by Joey Maalouf pair programming with Gabriel Butterick
from liblo import *
import numpy as np
import sys
import time


class MuseCalibrationServer(ServerThread):
  def __init__(self, port = 5001):
    ServerThread.__init__(self, port)
    self.STATES = {
      "ERROR":      -1,
      "CALIB_MEAN":  0,
      "CALIB_UP":    1,
      "CALIB_DOWN":  2,
      "CALIB_LEFT":  3,
      "CALIB_RIGHT": 4,
      "FINISHED":    5
    }
    self.state = None
    self.mean = None
    self.deviation = 30
    self.deviations = []
    self.history = np.asarray([])

  def calibrate(self):
    time.sleep(2)
    print("Please look directly at the screen.")
    self.state = self.STATES["CALIB_MEAN"]
    time.sleep(2)
    if self.state == self.STATES["ERROR"]:
      print("Unusual mean value detected.\nPlease make sure the Muse headband is on properly and re-run this program.")
      self.stop()
      sys.exit()
    print("Please look up briefly and return to center.")
    time.sleep(2)
    print("Please look down briefly and return to center.")
    time.sleep(2)
    print("Please look left briefly and return to center.")
    time.sleep(2)
    print("Please look right briefly and return to center.")
    time.sleep(2)
    if self.state == self.STATES["ERROR"]:
      print("Unusual deviation value detected.\nPlease make sure the Muse headband is on properly and re-run this program.")
      self.stop()
      sys.exit()
    else:
      print("Thank you!")

  @make_method("/muse/eeg", "ffff")
  def eeg_callback(self, path, args):
    (l_ear, l_forehead, r_forehead, r_ear) = args

    if self.state == self.STATES["CALIB_MEAN"]:
      if self.history.any():
        self.history = np.append(self.history, [args], axis = 0)
      else:
        self.history = np.asarray([args])

      if self.history.shape[0] >= 10:
        self.mean = np.mean(self.history)
        if self.mean > 1000 or self.mean < 600:
          self.state = self.STATES["ERROR"]
        else:
          self.history = []
          self.state = self.STATES["CALIB_UP"]

    elif self.state == self.STATES["CALIB_UP"]:
      self.history.append(r_ear)
      if r_ear < (self.mean - self.deviation):
        if self.history[-1] >= self.history[-2]:
          self.deviations.append(abs(self.mean - self.history[-2]))
          self.history = []
          self.state = self.STATES["CALIB_DOWN"]

    elif self.state == self.STATES["CALIB_DOWN"]:
      self.history.append(r_ear)
      if r_ear > (self.mean + self.deviation):
        if self.history[-1] <= self.history[-2]:
          self.deviations.append(abs(self.mean - self.history[-2]))
          self.history = []
          self.state = self.STATES["CALIB_LEFT"]

    elif self.state == self.STATES["CALIB_LEFT"]:
      self.history.append(l_forehead)
      if l_forehead > (self.mean + self.deviation):
        if self.history[-1] <= self.history[-2]:
          self.deviations.append(abs(self.mean - self.history[-2]))
          self.history = []
          self.state = self.STATES["CALIB_RIGHT"]

    elif self.state == self.STATES["CALIB_RIGHT"]:
      self.history.append(l_forehead)
      if l_forehead < (self.mean - self.deviation):
        if self.history[-1] >= self.history[-2]:
          self.deviations.append(abs(self.mean - self.history[-2]))
          self.history = []
          self.deviation = sum(self.deviations) / len(self.deviations)
          if self.deviation > 150 or self.deviation < 10:
            self.state = self.STATES["ERROR"]
          else:
            self.state = self.STATES["FINISHED"]


if __name__ == "__main__":
  server = MuseCalibrationServer()
  server.start()
  server.calibrate()
  server.stop()
  print("Mean: {}\nDeviation: {}".format(server.mean, server.deviation))
  sys.exit()
