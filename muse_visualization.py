from liblo import *
import sys
import time
import matplotlib.pyplot as plt
import numpy as np


class MuseServer(ServerThread):
  def __init__(self):
    ServerThread.__init__(self, 5001)
    self.n_events = 0
    self.l_ear = []
    self.l_forehead = []
    self.r_forehead = []
    self.r_ear = []

  @make_method("/muse/eeg", "ffff")
  def eeg_callback(self, path, args):
    (l_ear, l_forehead, r_forehead, r_ear) = args
    self.n_events += 1
    self.l_ear.append(l_ear)
    self.l_forehead.append(l_forehead)
    self.r_forehead.append(r_forehead)
    self.r_ear.append(r_ear)


def smooth(y, box_pts):
  box = np.ones(box_pts) / box_pts
  return np.convolve(y, box, mode = "same")


if __name__ == "__main__":
  try:
    server = MuseServer()
  except ServerError, err:
    print(str(err))
    sys.exit()

  server.start()
  time.sleep(4)
  server.stop()

  smoothing_window = 5
  points_used_up = int(smoothing_window / 2.0)
  events = range(server.n_events)[:-points_used_up]
  smooth_l_ear = smooth(server.l_ear, smoothing_window)[:-points_used_up]
  smooth_l_forehead = smooth(server.l_forehead, smoothing_window)[:-points_used_up]
  smooth_r_forehead = smooth(server.r_forehead, smoothing_window)[:-points_used_up]
  smooth_r_ear = smooth(server.r_ear, smoothing_window)[:-points_used_up]
  f, axes = plt.subplots(4, sharex = True)
  axes[0].set_title("Left Ear Sensor")
  axes[0].plot(events, smooth_l_ear, "blue")
  axes[1].set_title("Left Forehead Sensor")
  axes[1].plot(events, smooth_l_forehead, "blue")
  axes[2].set_title("Right Forehead Sensor")
  axes[2].plot(events, smooth_r_forehead, "blue")
  axes[3].set_title("Right Ear Sensor")
  axes[3].plot(events, smooth_r_ear, "blue")
  plt.show()
