# PFEIFER - OPWEBGO
import os
import subprocess
import urllib.request
from openpilot.common.realtime import Ratekeeper
import stat

VERSION = 'v1.2.1'
URL = f"https://github.com/pfeiferj/opweb/releases/download/{VERSION}/opwebd"
OPWEBD_PATH = '/data/media/0/opwebd'
VERSION_PATH = '/data/media/0/opwebd_version'

def download():
  opwebd_dir = os.path.dirname(OPWEBD_PATH)
  if not os.path.exists(opwebd_dir):
    os.makedirs(opwebd_dir)
  with urllib.request.urlopen(URL) as f:
    with open(OPWEBD_PATH, 'wb') as output:
      output.write(f.read())
      os.fsync(output)
      current_permissions = stat.S_IMODE(os.lstat(OPWEBD_PATH).st_mode) # <-- preserve permissions
      os.chmod(OPWEBD_PATH, current_permissions | stat.S_IEXEC) # <-- preserve permissions
    with open(VERSION_PATH, 'w') as output:
      output.write(VERSION)
      os.fsync(output)

def opwebd_thread(sm=None, pm=None):
  rk = Ratekeeper(0.05, print_delay_threshold=None)

  while True:
    try:
      if not os.path.exists(OPWEBD_PATH):
        download()
        continue
      if not os.path.exists(VERSION_PATH):
        download()
        continue
      with open(VERSION_PATH) as f:
        content = f.read()
        if content != VERSION:
          download()
          continue

      process = subprocess.Popen(OPWEBD_PATH)
      process.wait()
    except Exception as e:
      print(e)

    rk.keep_time()


def main(sm=None, pm=None):
  opwebd_thread(sm, pm)

if __name__ == "__main__":
  main()
