import os
from flask import Flask, render_template, request
from openpilot.common.params import Params

MAX_MEM_PARAMS_CHECKS = 5
_mem_params_checks = 0
_has_mem_params = False

params = Params()
# temporarily set mem_params as params. We will change this later if we detect
# a mem params path
mem_params = params
keys = params.all_keys()

IS_AGNOS = os.path.exists("/AGNOS")
if not IS_AGNOS:
    _has_mem_params = True
    mem_params = Params("/dev/shm/params")


def has_mem_params() -> bool:
  # I know, I know, globals... I promise it's fine
  global _has_mem_params
  global _mem_params_checks
  global mem_params

  if _has_mem_params:
    return True

  if _mem_params_checks < MAX_MEM_PARAMS_CHECKS:
    _mem_params_checks += 1
    _has_mem_params = os.path.exists("/dev/shm/params")

  if _has_mem_params:
    mem_params = Params("/dev/shm/params")
  return _has_mem_params


def route_params(app: Flask):

  @app.route("/params")
  def params_page():
    location = request.args.get('location', 'data')

    p = params
    if location == 'mem':
      p = mem_params

    parameters = [(key.decode('utf-8'), str(p.get(key))) for key in keys]

    return render_template('pages/params.html', params=parameters, location=location, has_mem_params=has_mem_params())
