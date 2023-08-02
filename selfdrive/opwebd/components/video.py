import os
from flask import Flask, render_template, request, send_from_directory
import datetime
import subprocess
from ..utils import SEGMENTS_DIR, sortSegments


def route_video(app: Flask):
  @app.route("/videos")
  def video_page():
    dirs = ["--".join(dir.split("--")[:-1])
            for dir in os.listdir(SEGMENTS_DIR) if dir.find("--") >= 0]
    dirs = set(dirs)
    dirs = list(dirs)
    dirs.sort()
    dirs.reverse()
    return render_template('pages/videos.html', options=dirs)

  @app.route("/video/route")
  def route_partial():
    route = request.args.get('route', '')
    return render_template('video/route.html', route=route)

  @app.route("/video/<route>/playlist.m3u8")
  def playlist_partial(route):
    dirs = [dir for dir in os.listdir(SEGMENTS_DIR) if dir.startswith(route)]
    dirs.sort(key=sortSegments)
    idx = 0
    segments = []
    for dir in dirs:
      probe = os.popen(
          f'ffprobe -i {SEGMENTS_DIR}/{dir}/qcamera.ts -show_entries format=duration -v quiet -of csv="p=0"')
      duration = float(probe.read().strip())
      duration = "{:.3f}".format(duration)
      segments.append((idx, duration, f"/file/{dir}/qcamera.ts"))
      idx += 1
    return render_template('video/playlist.m3u8', segments=segments)

  @app.route("/video")
  def video_partial():
    route = request.args.get('route', '')
    return render_template('video/video.html', route=route)

  @app.route("/video/segments")
  def segments_partial():
    route = request.args.get('route', '')
    show_conversion = not request.args.get('hide_conversion', False)
    dirs = [dir for dir in os.listdir(SEGMENTS_DIR) if dir.startswith(route)]
    dirs.sort(key=sortSegments)
    idx = 0
    segments = []
    t = 0
    for dir in dirs:
      probe = os.popen(
          f'ffprobe -i {SEGMENTS_DIR}/{dir}/qcamera.ts -show_entries format=duration -v quiet -of csv="p=0"'
      )
      duration = float(probe.read().strip())
      all_links = os.listdir(os.path.join(SEGMENTS_DIR, dir))
      links = [(dir, link) for link in all_links if link.endswith("hevc") or link.endswith("ts")]
      converted_links = [(dir, link) for link in all_links if link.endswith("mp4")]
      segments.append({
          "name": dir,
          "time": str(datetime.timedelta(seconds=int(t))),
          "links": links,
          "converted_links": converted_links
      })
      t += duration
      idx += 1
    return render_template('video/segments.html', segments=segments, show_conversion=show_conversion)

  @app.route('/video-convert/<path:path>')
  def convert_video(path):
    input_path = os.path.join(SEGMENTS_DIR, path)
    output_path = os.path.join(SEGMENTS_DIR, path + ".mp4")
    subprocess.Popen(["ffmpeg", "-i", input_path, output_path])
    return "triggered"

  @app.route('/file/<path:path>')
  def send_report(path):
    return send_from_directory(SEGMENTS_DIR, path, as_attachment=True)
