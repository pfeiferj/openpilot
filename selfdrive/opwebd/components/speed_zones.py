from flask import Flask, render_template
import os
from ..utils import SEGMENTS_DIR


def route_speed_zones(app: Flask):

  @app.route("/speed_zones")
  def speed_zones():
    return render_template('pages/speed_zones.html')
