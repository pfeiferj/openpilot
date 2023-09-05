#!/bin/bash
mkdir -p output
range=$(seq ${3} ${4})

for i in $range
do
  mkdir output/$2--$i
  scp comma@$1:/data/media/0/realdata/$2--$i/rlog output/$2--$i/rlog
  scp comma@$1:/data/media/0/realdata/$2--$i/fcamera.hevc output/$2--$i/fcamera.hevc
done

for i in $range
do
  python upload_to_mapillary.py output/$2--$i
done
