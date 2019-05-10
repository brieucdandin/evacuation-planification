#!/bin/bash
for file in ../InstancesInt/*.full; do
  name=${file##*/}
  python3 borne_inf.py $name
done
