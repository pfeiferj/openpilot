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

git checkout pfeifer-fast-boot
git pull --rebase origin master

git checkout pfeifer-hkg-long-control-tune
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

git checkout pfeifer-disable-registration
git pull --rebase origin master

git checkout pfeifer-high-bitrate
git pull --rebase origin master

git checkout pfeifer-sounds
git pull --rebase origin master

git checkout pfeifer-disable-dcam-upload
git pull --rebase origin master

git checkout pfeifer-opweb-go
git pull --rebase origin master

git checkout pfeifer-mtsc
git pull --rebase origin master

git checkout pfeifer-road-name
git pull --rebase origin master

git checkout pfeifer-ford-steering-hack
git pull --rebase origin master

git checkout pfeifer-ford-steering-data-radar
git pull --rebase origin master


# Upstream Prs
git checkout cluster-based-max-speed
git pull --rebase origin master
