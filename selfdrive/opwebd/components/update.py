from flask import Flask, render_template
from openpilot.common.params import Params
import os
import subprocess

params = Params()


def route_update(app: Flask):
  @app.route("/update")
  def update_page():
    return render_template('pages/update.html')

  @app.post('/update/install')
  def install_update():
    if os.path.exists("/data/openpilot/prebuilt"):
      os.remove("/data/openpilot/prebuilt")
    params.put_bool("DoReboot", True)
    return "triggered"

  @app.post('/update/check')
  def check_for_update():
    subprocess.run(["pkill", "-SIGUSR1", "-f", "selfdrive.updated"])
    return "triggered"

  @app.post('/update/download')
  def download_update():
    subprocess.run(["pkill", "-SIGHUP", "-f", "selfdrive.updated"])
    return "triggered"

  @app.route('/update/status')
  def update_status():
    updater_state = (params.get("UpdaterState") or b'').decode()
    if updater_state != "idle":
      return updater_state

    update_failed_count = int((params.get("UpdateFailedCount") or "0").decode())
    if update_failed_count > 0:
      return "failed"
    if params.get_bool("UpdaterFetchAvailable"):
      return "available"

    return (params.get("LastUpdateTime") or "").decode()

  @app.route('/update/update_card')
  def update_card():
    button_text = "Check For Update"
    button_link = "/update/check"
    if params.get_bool("UpdaterFetchAvailable"):
      button_text = "Download Update"
      button_link = "/update/download"

    downloaded = params.get_bool("UpdateAvailable")

    version = (params.get("UpdaterNewDescription") or b'').decode()
    branch = (params.get("UpdaterTargetBranch") or b'').decode()
    state = (params.get("UpdaterState") or b'').decode()
    last_check = (params.get("LastUpdateTime") or b'').decode()
    release_notes = (params.get("UpdaterNewReleaseNotes") or b'').decode()
    update_failed_count = (params.get("UpdateFailedCount") or b"0").decode()

    return render_template(
      'update/update_card.html',
      button_text=button_text,
      button_link=button_link,
      install_button=downloaded,
      version=version,
      branch=branch,
      state=state,
      last_check=last_check,
      release_notes=release_notes,
      failure_count=update_failed_count,
    )

  @app.route('/update/version_card')
  def version_card():
    version = (params.get("UpdaterCurrentDescription") or b'').decode()
    repo = (params.get("GitRemote") or b'').decode()
    branch = (params.get("GitBranch") or b'').decode()
    install_date = (params.get("InstallDate") or b'').decode()
    release_notes = (params.get("UpdaterCurrentReleaseNotes") or b'').decode()
    commit = (params.get("GitCommit") or b'').decode()

    return render_template(
      'update/version_card.html',
      version=version,
      repo=repo,
      branch=branch,
      install_date=install_date,
      release_notes=release_notes,
      commit=commit
    )
