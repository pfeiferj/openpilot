import os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))

IS_AGNOS = os.path.exists("/AGNOS")
SEGMENTS_DIR = "/data/media/0/realdata"
if not IS_AGNOS:
  SEGMENTS_DIR = os.path.join(dir_path, "video")
  if not os.path.exists(SEGMENTS_DIR):
    os.mkdir(SEGMENTS_DIR)


def sortSegments(segment):
  return int(segment.split("--")[-1])

def dictMap(event):
  return event.to_dict()

def jsonMap(event):
  return  json.dumps(event, indent=2, default=lambda x: "")
