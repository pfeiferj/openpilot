#! /bin/bash
set -e

git checkout pfeifer-always-on-lateral
git pull

git checkout pfeifer-current-max-speed
git pull

git checkout pfeifer-experimental-mode-toggle
git pull

git checkout pfeifer-fast-boot
git pull

git checkout pfeifer-hkg-long-control-tune
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

git checkout pfeifer-disable-registration
git pull

git checkout pfeifer-high-bitrate
git pull

git checkout pfeifer-sounds
git pull

git checkout pfeifer-disable-dcam-upload
git pull

git checkout pfeifer-opweb-go
git pull

git checkout pfeifer-mtsc
git pull

git checkout pfeifer-road-name
git pull

git checkout pfeifer-ford-steering-hack
git pull


# Upstream Prs
git checkout cluster-based-max-speed
git pull
