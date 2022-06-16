# Code to plot zonal average SSTs for CMIP6 ensemble + observational data
# Author: Nathan Erickson
# Date: 3/20/2022
# Coded with Python 3.8.10

# Import necessary modules

import os
import glob
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import xarray as xr
import numpy as np
from datetime import datetime
from lib import zonal_avg_ens_calculator

# Set base directory, open data file

data_dir = '' #Fill these in with your local file paths
home_dir = ''
os.chdir(data_dir)
obs_ssts = xr.open_dataset('sst.mnmean.nc')

model_list = ["ACCESS-CM2", "ACCESS-ESM1-5", "AWI-CM-1-1-MR", "BCC-CSM2-MR", "CAMS-CSM1-0", "CanESM5", "CESM2", "CESM2-WACCM", "CMCC-CM2-SR5", 
              "CNRM-CM6-1", "CNRM-CM6-1-HR", "CNRM-ESM2-1", "EC-Earth3", "EC-Earth3-Veg", "FGOALS-f3-L", "FGOALS-g3", "GFDL-CM4", "GFDL-ESM4", 
              "GISS-E2-1-G", "HadGEM3-GC31-LL", "HadGEM3-GC31-MM", "INM-CM4-8", "INM-CM5-0", "IPSL-CM6A-LR", "MIROC6", "MIROC-ES2L",
              "MPI-ESM1-2-HR", "MPI-ESM1-2-LR", "MPI-ESM2-0", "NESM3", "NorESM2-LM", "NorESM2-MM", "TaiESM1"]
ens_size = range(len(model_list))

# Iterate over models in the ensemble; output to file
for model in ens_size:
    ens_data, model_run = zonal_avg_ens_calculator(model_list,model)
    os.chdir(data_dir)
    if os.path.isfile('ens_zonal_averages.nc'):
        ens_data.to_netcdf('ens_zonal_averages.nc',mode='a')
    else:
        ens_data.to_netcdf('ens_zonal_averages.nc',mode='w')
    print(f'Sent updated data with {model_run} included!')
