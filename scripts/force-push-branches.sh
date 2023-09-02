#! /bin/bash
set -e

git checkout pfeifer-always-on-lateral
git push --force

git checkout pfeifer-current-max-speed
git push --force

git checkout pfeifer-experimental-mode-toggle
git push --force

git checkout pfeifer-fast-boot
git push --force

git checkout pfeifer-gap-adjust-control
git push --force

git checkout pfeifer-hkg-long-control-tune
git push --force

git checkout pfeifer-lane-detection
git push --force

git checkout pfeifer-nudgeless-lane-change
git push --force

git checkout pfeifer-speed-limit-control
git push --force

git checkout pfeifer-vtsc
git push --force

git checkout pfeifer-mapd
git push --force

git checkout pfeifer-button-manager
git push --force

git checkout pfeifer-gap-adjust-button
git push --force

git checkout pfeifer-opweb
git push --force

git checkout pfeifer-distance-based-curvature
git push --force

git checkout pfeifer-disable-registration
git push --force

git checkout pfeifer-tailscale
git push --force

git checkout pfeifer-high-bitrate
git push --force

git checkout pfeifer-sounds
git push --force


# Upstream Prs
git checkout cluster-based-max-speed
git push --force

git checkout wrong-direction-check
git push --force
