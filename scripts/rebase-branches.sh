#! /bin/bash
set -e

git checkout pfeifer-always-on-lateral
git pull --rebase origin master

git checkout pfeifer-current-max-speed
git pull --rebase origin master

git checkout pfeifer-button-manager
git pull --rebase origin master

git checkout pfeifer-gap-adjust-button
git checkout -b pgab-tmp
git checkout pfeifer-gap-adjust-button
git reset --hard pfeifer-button-manager
git cherry-pick pgab-tmp
git branch -D pgab-tmp

git checkout pfeifer-experimental-mode-toggle
git checkout -b pemt-tmp
git checkout pfeifer-experimental-mode-toggle
git reset --hard pfeifer-gap-adjust-button
git cherry-pick pemt-tmp
git branch -D pemt-tmp

git checkout pfeifer-gap-adjust-control
git checkout -b pgac-tmp
git checkout pfeifer-gap-adjust-control
git reset --hard pfeifer-gap-adjust-button
git cherry-pick pgac-tmp
git branch -D pgac-tmp

git checkout pfeifer-fast-boot
git pull --rebase origin master

git checkout pfeifer-hkg-long-control-tune
git pull --rebase origin master

git checkout pfeifer-lane-detection
git pull --rebase origin master

git checkout pfeifer-nudgeless-lane-change
git pull --rebase origin master

git checkout pfeifer-speed-limit-control
git checkout -b pslc-tmp
git checkout pfeifer-speed-limit-control
git reset --hard pfeifer-gap-adjust-button
git cherry-pick pslc-tmp
git branch -D pslc-tmp

git checkout pfeifer-vtsc
git pull --rebase origin master

git checkout pfeifer-mapd
git pull --rebase origin master

git checkout pfeifer-opweb
git pull --rebase origin master

git checkout pfeifer-distance-based-curvature
git pull --rebase origin master

git checkout pfeifer-disable-registration
git pull --rebase origin master

git checkout pfeifer-tailscale
git pull --rebase origin master

git checkout pfeifer-high-bitrate
git pull --rebase origin master


# Upstream Prs
git checkout cluster-based-max-speed
git pull --rebase origin master

git checkout wrong-direction-check
git pull --rebase origin master
