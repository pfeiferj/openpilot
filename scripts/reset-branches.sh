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

git checkout pfeifer-hkg-long-control-tune
git reset --hard origin/pfeifer-hkg-long-control-tune

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

git checkout pfeifer-disable-registration
git reset --hard origin/pfeifer-disable-registration

git checkout pfeifer-high-bitrate
git reset --hard origin/pfeifer-high-bitrate

git checkout pfeifer-sounds
git reset --hard origin/pfeifer-sounds

git checkout pfeifer-disable-dcam-upload
git reset --hard origin/pfeifer-disable-dcam-upload

git checkout pfeifer-opweb-go
git reset --hard origin/pfeifer-opweb-go

git checkout pfeifer-mtsc
git reset --hard origin/pfeifer-mtsc

git checkout pfeifer-road-name
git reset --hard origin/pfeifer-road-name

git checkout pfeifer-ford-steering-hack
git reset --hard origin/pfeifer-ford-steering-hack

git checkout pfeifer-ford-steering-data-radar
git reset --hard origin/pfeifer-ford-steering-data-radar


# Upstream PRs
git checkout cluster-based-max-speed
git reset --hard origin/cluster-based-max-speed
