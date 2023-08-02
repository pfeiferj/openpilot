from flask import Flask
from .components.home import route_home
from .components.log import route_log
from .components.params import route_params
from .components.settings import route_settings
from .components.update import route_update
from .components.video import route_video
from .components.gpx import route_gpx


app = Flask(__name__)

route_home(app)
route_log(app)
route_params(app)
route_settings(app)
route_update(app)
route_video(app)
route_gpx(app)


def main():
  app.run(host="0.0.0.0", port=5050)


if __name__ == '__main__':
  main()
