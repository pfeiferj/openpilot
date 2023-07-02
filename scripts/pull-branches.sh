#! /bin/bash
set -e

git checkout lag-adjusted-curvature-velocity
git pull

git checkout pfeifer-always-on-lateral
git pull

git checkout pfeifer-current-max-speed
git pull

git checkout pfeifer-experimental-mode-toggle
git pull

git checkout pfeifer-fast-boot
git pull

git checkout pfeifer-gap-adjust-control
git pull

git checkout pfeifer-hkg-long-control-tune
git pull

git checkout pfeifer-lane-detection
git pull

git checkout pfeifer-nudgeless-lane-change
git pull

git checkout pfeifer-speed-limit-control
git pull

git checkout pfeifer-vtsc
git pull

git checkout pfeifer-mapd
git pull

git checkout pfeifer-button-manager
git pull

git checkout pfeifer-gap-adjust-button
git pull
