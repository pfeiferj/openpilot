from flask import Flask, render_template
import os
from ..utils import SEGMENTS_DIR


def route_home(app: Flask):

  @app.route("/")
  def index():
    dirs = ["--".join(dir.split("--")[:-1])
            for dir in os.listdir(SEGMENTS_DIR) if dir.find("--") >= 0]
    dirs = set(dirs)
    dirs = list(dirs)
    dirs.sort()
    dirs.reverse()
    return render_template('pages/index.html', route=dirs[0])
