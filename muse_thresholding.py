from liblo import *
import sys
import time


class MuseServer(ServerThread):
  def __init__(self, port = 5001, mean = 850, deviation = 80, sleep_timer = 200):
    ServerThread.__init__(self, port)
    self.mean = mean
    self.deviation = deviation
    self.sleep_timer = sleep_timer
    self.sleep_counter = 0
    self.sleeping = False

  @make_method("/muse/eeg", "ffff")
  def eeg_callback(self, path, args):
    (l_ear, l_forehead, r_forehead, r_ear) = args

    if self.sleep_counter >= self.sleep_timer:
      self.sleep_counter = 0
      self.sleeping = False

    if not self.sleeping:
      if r_ear < (self.mean - self.deviation):
        print("Up")
        self.sleeping = True
      elif r_ear > (self.mean + self.deviation):
        print("Down")
        self.sleeping = True
      if l_forehead < (self.mean - self.deviation):
        print("Right")
        self.sleeping = True
      elif l_forehead > (self.mean + self.deviation):
        print("Left")
        self.sleeping = True
    else:
      self.sleep_counter += 1


if __name__ == "__main__":
  try:
    server = MuseServer()
  except ServerError, err:
    print(str(err))
    sys.exit()

  server.start()
  time.sleep(30)
  server.stop()
