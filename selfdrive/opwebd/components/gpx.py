from flask import Flask, render_template, Response
from openpilot.common.params import Params
from cereal import log
from ..utils import SEGMENTS_DIR, sortSegments, dictMap
import os
from datetime import datetime
import math
from itertools import chain

params = Params()
keys = params.all_keys()

def llkFilter(event):
  return event.which() == 'liveLocationKalman'

def countFilter(enumEvent):
  i, e = enumEvent
  return i % 10 == 0

def valid_location(enumEvent):
  i, e = enumEvent
  return e.liveLocationKalman.positionGeodetic.valid

def enumEventDictMap(enumEvent):
  i, e = enumEvent
  return e.to_dict()

def make_point(event, offset):
  dt = mono_datetime(event, offset)
  bearing_rad = event["liveLocationKalman"]["calibratedOrientationNED"]["value"][2]
  return {
    "latitude": event["liveLocationKalman"]["positionGeodetic"]["value"][0],
    "longitude": event["liveLocationKalman"]["positionGeodetic"]["value"][1],
    "elevation": event["liveLocationKalman"]["positionGeodetic"]["value"][2],
    "bearing": math.degrees(bearing_rad),
    "timestamp": dt.isoformat() + "Z",
  }

def mono_offset(clock):
  wall_time = clock["clocks"]["wallTimeNanos"]
  mono_time = clock["clocks"]["monotonicNanos"]
  return wall_time - mono_time

def mono_datetime(event, offset):
  mono_time = event["logMonoTime"]
  wall_time = mono_time + offset
  return datetime.fromtimestamp(wall_time/1000/1000/1000)

def route_gpx(app: Flask):

  @app.route("/gpx/<segment>.gpx")
  def gpx_file(segment):
    full_path = os.path.join(SEGMENTS_DIR, segment, "rlog")
    file = open(full_path, "rb")
    events = log.Event.read_multiple(file)
    filtered_events = [e for e in events if 'liveLocationKalman' == e.which()]
    filtered_events = [e.to_dict() for e in filtered_events]
    filtered_events = [e for e in filtered_events if valid_location(e)]
    file.close()

    file = open(full_path, "rb")
    events = log.Event.read_multiple(file)
    filtered_clocks = [e for e in events if 'clocks' == e.which()]
    clock = filtered_clocks[0].to_dict()
    offset = mono_offset(clock)
    file.close()

    points = [make_point(e, offset) for e in filtered_events]
    return Response(render_template('gpx/segment.gpx', points=points), mimetype='application/octet-stream')

  @app.route("/gpx/route/<route>.gpx")
  def gpx_route_file(route):
    dirs = [d for d in os.listdir(SEGMENTS_DIR) if d.startswith(route)]
    dirs.sort(key=sortSegments)

    all_points = []
    for d in dirs:
      full_path = os.path.join(SEGMENTS_DIR, d, "rlog")
      file = open(full_path, "rb")
      events = log.Event.read_multiple(file)
      filtered_events = [e for e in events if 'liveLocationKalman' == e.which()]
      filtered_events = [e.to_dict() for e in filtered_events]
      filtered_events = [e for e in filtered_events if valid_location(e)]
      file.close()

      file = open(full_path, "rb")
      events = log.Event.read_multiple(file)
      filtered_clocks = [e for e in events if 'clocks' == e.which()]
      clock = filtered_clocks[0].to_dict()
      offset = mono_offset(clock)
      file.close()

      points = [make_point(e, offset) for e in filtered_events]
      all_points += points
    return Response(render_template('gpx/segment.gpx', points=all_points), mimetype='application/octet-stream')

  @app.route("/gpx/route/lite/<route>.gpx")
  def gpx_lite_route_file(route):
    dirs = [d for d in os.listdir(SEGMENTS_DIR) if d.startswith(route)]
    dirs.sort(key=sortSegments)

    file_descriptors = []
    point_generators = []
    for d in dirs:
      full_path = os.path.join(SEGMENTS_DIR, d, "qlog")
      file = open(full_path, "rb")
      events = log.Event.read_multiple(file)
      filtered_events = enumerate(filter(llkFilter, events))
      filtered_events = filter(countFilter, filtered_events)
      filtered_events = filter(valid_location, filtered_events)
      filtered_events = map(enumEventDictMap, filtered_events)

      file2 = open(full_path, "rb")
      events = log.Event.read_multiple(file2)
      clock = next(e for e in events if 'clocks' == e.which())
      clock = clock.to_dict()
      offset = mono_offset(clock)

      def map_points(event, offset = offset):
        dt = mono_datetime(event, offset)
        bearing_rad = event["liveLocationKalman"]["calibratedOrientationNED"]["value"][2]
        return {
          "latitude": event["liveLocationKalman"]["positionGeodetic"]["value"][0],
          "longitude": event["liveLocationKalman"]["positionGeodetic"]["value"][1],
          "elevation": event["liveLocationKalman"]["positionGeodetic"]["value"][2],
          "bearing": math.degrees(bearing_rad),
          "timestamp": dt.isoformat() + "Z",
        }

      points = map(map_points, filtered_events)
      point_generators.append(points)
      file_descriptors.append(file)
      file_descriptors.append(file2)

    all_points = list(chain(*point_generators))

    for file in file_descriptors:
      file.close()

    return Response(render_template('gpx/segment.gpx', points=all_points), mimetype='application/octet-stream')
