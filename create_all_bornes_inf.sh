#!/bin/bash
 for file_name in 'ls ./InstancesInt' do
   python3 ./Etape1/borne_inf.py $file_name
 done
