#! /bin/bash
set -e

git checkout pfeifer-always-on-lateral
git reset --hard origin/pfeifer-always-on-lateral

git checkout pfeifer-current-max-speed
git reset --hard origin/pfeifer-current-max-speed

git checkout pfeifer-experimental-mode-toggle
git reset --hard origin/pfeifer-experimental-mode-toggle

git checkout pfeifer-fast-boot
git reset --hard origin/pfeifer-fast-boot

git checkout pfeifer-gap-adjust-control
git reset --hard origin/pfeifer-gap-adjust-control

git checkout pfeifer-hkg-long-control-tune
git reset --hard origin/pfeifer-hkg-long-control-tune

git checkout pfeifer-lane-detection
git reset --hard origin/pfeifer-lane-detection

git checkout pfeifer-nudgeless-lane-change
git reset --hard origin/pfeifer-nudgeless-lane-change

git checkout pfeifer-speed-limit-control
git reset --hard origin/pfeifer-speed-limit-control

git checkout pfeifer-vtsc
git reset --hard origin/pfeifer-vtsc

git checkout pfeifer-mapd
git reset --hard origin/pfeifer-mapd

git checkout pfeifer-button-manager
git reset --hard origin/pfeifer-button-manager

git checkout pfeifer-gap-adjust-button
git reset --hard origin/pfeifer-gap-adjust-button

git checkout pfeifer-opweb
git reset --hard origin/pfeifer-opweb

git checkout pfeifer-distance-based-curvature
git reset --hard origin/pfeifer-distance-based-curvature

git checkout pfeifer-disable-registration
git reset --hard origin/pfeifer-disable-registration


# Upstream PRs
git checkout cluster-based-max-speed
git reset --hard origin/cluster-based-max-speed

git checkout wrong-direction-check
git reset --hard origin/wrong-direction-check
