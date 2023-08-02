from flask import Flask, render_template, request
from openpilot.common.params import Params

params = Params()
keys = params.all_keys()


def route_settings(app: Flask):

  @app.route("/settings")
  def settings_page():
    toggle_keys = [key.decode('utf-8') for key in keys if params.get(key) in [b'0', b'1']]
    toggle_keys = [key for key in toggle_keys if "Available" not in key and "Is" not in key and "Count" not in key]
    return render_template('pages/settings.html', keys=toggle_keys)

  @app.route("/params/toggle", methods=['GET', 'PUT'])
  def param_toggle():
    key = request.args.get('key', '')
    p = params
    val = p.get_bool(key)
    if request.method == 'PUT':
      p.put_bool(key, not val)
      val = not val
    bg = "bg-indigo-600" if val else "bg-gray-200"
    translate = "translate-x-5" if val else "translate-x-0"
    checked = str(val).lower()

    return render_template('settings/toggle.html', checked=checked, bg=bg, translate=translate, key=key)
