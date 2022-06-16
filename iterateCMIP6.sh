#!/bin/bash

#Bash script to calculate ENSO indices for the CMIP6 ensemble

#declare -a MemberList=("ACCESS-CM2" "ACCESS-ESM1-5" "AWI-CM-1-1-MR" "BCC-CSM2-MR" "CAMS-CSM1-0" "CanESM5" "CESM2" "CESM2-WACCM" "CMCC-CM2-SR5" "CNRM-CM6-1" "CNRM-CM6-1-HR" "CNRM-ESM2-1" "EC-Earth3" "EC-Earth3-Veg" "FGOALS-f3-L" "FGOALS-g3" "GFDL-CM4" "GFDL-ESM4" "GISS-E2-1-G" "HadGEM3-GC31-LL" "HadGEM3-GC31-MM" "INM-CM4-8" "INM-CM5-0" "IPSL-CM6A-LR" "MIROC6" "MIROC-ES2L" "MPI-ESM1-2-HR" "MPI-ESM1-2-LR" "MPI-ESM2-0" "NESM3" "NorESM2-LM" "NorESM2-MM" "TaiESM1")

for mem in ${MemberList[@]}; do    
  dir="/chinook2/nathane1/Thesis/CMIP6/$mem"
    for f in $dir/ts_Amon*.nc
      do
        declare -i TIME_LIMIT=1800
        declare -i INTERVAL=1
        mask=$dir/sftlf_fx*.nc
        python ELI.py $mem $f $mask #<- Uncomment me to calculate ELI for CMIP6
        #python niño3-4.py $mem $f $mask #<- Uncomment me to calculate Niño 3.4 for CMIP6
        if [ "$SECONDS" -gt "$TIME_LIMIT" ];
        then
            continue
        fi
      done
 done
 
 
