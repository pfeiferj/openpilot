from flask import Flask, render_template, request, Response
import json
import os
from cereal import log
from ..utils import SEGMENTS_DIR, sortSegments, dictMap, jsonMap


def route_log(app: Flask):

  @app.route("/log")
  def log_page():
    path = request.args.get('path', '')
    event_types = list(log.Event.schema.union_fields)
    event_types.sort()
    return render_template('pages/log.html', path=path, options=event_types)

  @app.route("/log/<segment>/<log_file>/type")
  def log_type(segment, log_file):
    event_type = request.args.get('event_type', '')
    page = int(request.args.get('page', '1'))
    full_path = os.path.join(SEGMENTS_DIR, segment, log_file)
    file = open(full_path, "rb")
    events = log.Event.read_multiple(file)
    filtered_events = [e for e in events if event_type == e.which()]
    events_slice = filtered_events[page*10-10:page*10]
    str_events = [json.dumps(e.to_dict(), indent=2, default=lambda ev : ev.hex()) for e in events_slice]
    file.close()

    next_page=None
    if len(str_events) == 10:
      next_page = f"/log/{segment}/{log_file}/type?event_type={event_type}&page={page+1}"

    return render_template('log/log_type.html', events=str_events, next_page=next_page)

  @app.route("/logs")
  def logs_page():
    dirs = ["--".join(dir.split("--")[:-1])
            for dir in os.listdir(SEGMENTS_DIR) if dir.find("--") >= 0]
    dirs = set(dirs)
    dirs = list(dirs)
    dirs.sort()
    dirs.reverse()
    return render_template('pages/logs.html', options=dirs)

  @app.route("/logs/segments")
  def logs_table():
    route = request.args.get('route', '')
    dirs = [dir for dir in os.listdir(SEGMENTS_DIR) if dir.startswith(route)]
    dirs.sort(key=sortSegments)
    return render_template('log/logs.html', segments=dirs)

  @app.route("/logs/json")
  def json_logs():
    log_file = request.args.get('log', '')
    filename = log_file.replace("/", "-") + ".json"
    # TODO: this isn't really safe, but good enough for now because we aren't serving to the internet
    file = open(os.path.join(SEGMENTS_DIR, log_file), "rb")
    events = log.Event.read_multiple(file)
    events = map(dictMap, events)
    events = '\n'.join(map(jsonMap, events))
    file.close()
    return Response(events,
                    mimetype="text/json",
                    headers={"Content-Disposition":
                             "attachment;filename=" + filename})
