# muse-eye-tracking
Analyzing Muse headband sensor data to track eye motion. Comes with demo software (a basic joystick simulator, as well as a more advanced maze game to navigate) in order to show how easy it is to interact with your computer using nothing but your eyes, the Muse headband, and our software.

Done for the Codestellation Nov. 14-15 hackathon.

We won! Codestellation listed its overall category winners, of which we were one, but we know we also came in first overall, since we recieved the bonus prizes!

### Requirements
* [pyliblo module](http://das.nasophon.de/pyliblo/)
  * `sudo apt-get install liblo`
  * `sudo pip install pyliblo`
* [Muse SDK](https://sites.google.com/a/interaxon.ca/muse-developer-site/download)
  * download the [installer](http://storage.googleapis.com/ix_downloads/musesdk-3.4.1/musesdk-3.4.1-linux-installer.run)
  * `cd ~/Downloads/`
  * `chmod +x musesdk-3.4.1-linux-installer.run`
  * `./musesdk-3.4.1-linux-installer.run`
* [Muse headband](http://www.choosemuse.com/)
  * connect via Bluetooth
  * `muse-io --osc osc.udp://localhost:5001,osc.udp://localhost:5002`

### Usage
* `git clone https://github.com/joeylmaalouf/muse-eye-tracking.git`
* `cd muse-eye-tracking`
* `python muse_thresholding.py`
