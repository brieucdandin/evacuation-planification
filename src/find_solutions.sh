#!/bin/bash
for file in ../InstancesInt/*.full; do
  extname=${file##*/}
  name=${extname%%.*}
  python3 recherche_locale.py $extname /SupTaux/$name-sol_sup
done
