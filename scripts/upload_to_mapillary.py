#!python
import sys

import capnp
import os
from datetime import datetime
import subprocess
import math


def find_capnp():
    if os.path.exists("./log.capnp"):
        return "./log.capnp"
    if os.path.exists("./cereal/log.capnp"):
        return "./cereal/log.capnp"
    if os.path.exists("./scripts/cereal/log.capnp"):
        return "./scripts/cereal/log.capnp"
    if os.path.exists("../cereal/log.capnp"):
        return "../cereal/log.capnp"
    if os.path.exists("../openpilot/cereal/log.capnp"):
        return "../openpilot/cereal/log.capnp"
    if os.path.exists("../../openpilot/cereal/log.capnp"):
        return "../../openpilot/cereal/log.capnp"

    raise Exception("Could not find log.capnp")

def valid_location(event):
  return event["liveLocationKalman"]["positionGeodetic"]["valid"]

def mono_offset(clock):
  wall_time = clock["clocks"]["wallTimeNanos"]
  mono_time = clock["clocks"]["monotonicNanos"]
  return wall_time - mono_time

def mono_datetime_from_event(event, offset):
  mono_time = event["logMonoTime"]
  wall_time = mono_time + offset
  return datetime.fromtimestamp(wall_time/1000/1000/1000)

def mono_datetime(mono_time, offset):
  wall_time = mono_time + offset
  return datetime.fromtimestamp(wall_time/1000/1000/1000)

def gpx_point(point):
    return f"""<trkpt lat="{point["latitude"]}" lon="{point["longitude"]}">
        <ele>{point["elevation"]}</ele>
        <magvar>{point["bearing"]}</magvar>
        <time>{point["timestamp"]}</time>
      </trkpt>"""
def gpx_file(points):
    gpx_points = "\n".join([gpx_point(point) for point in points])

    return f"""<?xml version="1.0" encoding="UTF-8"?>
    <gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" version="1.1" creator="opweb -- https://github.com/pfeiferj/openpilot">
      <trk>
        <trkseg>
        {gpx_points}
        </trkseg>
      </trk>
    </gpx>"""

def make_point(event, offset):

  dt = mono_datetime_from_event(event, offset)
  bearing_rad = event["liveLocationKalman"]["calibratedOrientationNED"]["value"][2]
  return {
    "latitude": event["liveLocationKalman"]["positionGeodetic"]["value"][0],
    "longitude": event["liveLocationKalman"]["positionGeodetic"]["value"][1],
    "elevation": event["liveLocationKalman"]["positionGeodetic"]["value"][2],
    "bearing": math.degrees(bearing_rad),
    "timestamp": dt.isoformat() + "Z",
  }

def main():
    # Load capnp schema manually from file
    capnp.remove_import_hook()
    log = capnp.load(find_capnp())

    segment_path = sys.argv[-1]
    video_path = os.path.join(segment_path, "fcamera.hevc")

    full_path = os.path.join(segment_path, "rlog")
    file = open(full_path, "rb")
    events = log.Event.read_multiple(file)
    filtered_events = [e for e in events if 'liveLocationKalman' == e.which()]
    filtered_events = [e.to_dict() for e in filtered_events]
    filtered_events = [e for e in filtered_events if valid_location(e)]
    file.close()

    file = open(full_path, "rb")
    events = log.Event.read_multiple(file)
    events = [e for e in events]
    filtered_clocks = [e for e in events if 'clocks' == e.which()]
    clock = filtered_clocks[0].to_dict()
    offset = mono_offset(clock)
    file.close()

    file = open(full_path, "rb")
    events = log.Event.read_multiple(file)
    filtered_clocks = [e for e in events if 'clocks' == e.which()]
    clock = filtered_clocks[0].to_dict()
    offset = mono_offset(clock)
    file.close()

    points = [make_point(e, offset) for e in filtered_events]

    gpx_path = os.path.join(segment_path, "segment.gpx")
    file = open(gpx_path, "w+")
    file.write(gpx_file(points))
    file.close()

    file = open(full_path, "rb")
    events = log.Event.read_multiple(file)
    filtered_frames = [e for e in events if 'roadCameraState' == e.which()]
    first_frame = filtered_frames[0].to_dict()
    file.close()

    video_start = mono_datetime(first_frame["roadCameraState"]["timestampEof"], offset)
    video_start_string = video_start.strftime("%Y_%m_%d_%H_%M_%S_%f")[:-3]

    subprocess.run(["mapillary_tools", "video_process_and_upload", "--geotag_source", "gpx", "--geotag_source_path", gpx_path, "--video_sample_distance", "-1", "--video_sample_interval", "0.2", "--video_start_time", video_start_string, "--skip_process_errors", video_path])


if __name__ == "__main__":
    main()
