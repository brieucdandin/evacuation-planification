#!/bin/bash
for file in ../InstancesInt/*.full; do
  extname=${file##*/}
  name=${extname%%.*}
  python3 borne_inf.py $name
done
