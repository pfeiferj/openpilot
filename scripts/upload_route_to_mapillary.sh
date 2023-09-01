#!/bin/bash
for i in $(seq  2 15)
do
  python upload_to_mapillary.py $1--$i
done
