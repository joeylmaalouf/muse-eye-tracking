from liblo import *
import sys
import time
import numpy as np


def smooth(y, box_pts):
  box = np.ones(box_pts) / box_pts
  return np.convolve(y, box, mode = "same")


class MuseServer(ServerThread):
  def __init__(self, port = 5001, mean = 850, deviation = 80, history_size = 5):
    ServerThread.__init__(self, port)
    self.mean = mean
    self.deviation = deviation
    self.history_size = history_size
    self.lag_time = int(history_size / 2.0) + 1
    self.le_data = [mean] * history_size
    self.lf_data = [mean] * history_size
    self.rf_data = [mean] * history_size
    self.re_data = [mean] * history_size

  @make_method("/muse/eeg", "ffff")
  def eeg_callback(self, path, args):
    (l_ear, l_forehead, r_forehead, r_ear) = args
    self.le_data = smooth(self.le_data[1:]+[l_ear], self.history_size)
    self.lf_data = smooth(self.lf_data[1:]+[l_forehead], self.history_size)
    self.rf_data = smooth(self.rf_data[1:]+[r_forehead], self.history_size)
    self.re_data = smooth(self.re_data[1:]+[r_ear], self.history_size)
    if self.re_data[-self.lag_time] < (self.mean - self.deviation):
      print("Up")
    elif self.re_data[-self.lag_time] > (self.mean + self.deviation):
      print("Down")
    else:
      print("Straight")


if __name__ == "__main__":
  try:
    server = MuseServer()
  except ServerError, err:
    print(str(err))
    sys.exit()

  server.start()
  time.sleep(30)
  server.stop()
