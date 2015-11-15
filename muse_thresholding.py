from liblo import *
import sys
import time


class MuseServer(ServerThread):
  def __init__(self, port = 5001, mean = 850, deviation = 80):
    ServerThread.__init__(self, port)
    self.mean = mean
    self.deviation = deviation

  @make_method("/muse/eeg", "ffff")
  def eeg_callback(self, path, args):
    (l_ear, l_forehead, r_forehead, r_ear) = args
    if r_ear < (self.mean - self.deviation):
      print("Up")
    elif r_ear > (self.mean + self.deviation):
      print("Down")
    if l_forehead < (self.mean - self.deviation):
      print("Right")
    elif l_forehead > (self.mean + self.deviation):
      print("Left")


if __name__ == "__main__":
  try:
    server = MuseServer()
  except ServerError, err:
    print(str(err))
    sys.exit()

  server.start()
  time.sleep(30)
  server.stop()
