# Code to calculate Niño 3.4 index for CMIP6 data
# Author: Nathan Erickson
# Date: 11/8/2021
# Coded with Python 3.8.10

# Initialize system variables

import sys

model = sys.argv[1]
f = sys.argv[2]
mask = sys.argv[3]

# Directory management

import os

dir = '/chinook2/nathane1/Thesis/CMIP6/'
path = dir + model
os.chdir(path)

# Manipulate file paths to maximize future usability

from cmip6_processing import model_formatter
filename = f.split('CMIP6')[1]
realization_file = filename.split(f'{model}/')[1]
realization = realization_file.split('.nc')[0]
format_realization = model_formatter(realization)

# Print a couple of sanity checks to the screen

print('---------------------------------------')
print('Starting run for', model)
print('Model data to be used is', filename)
print('Land mask for file is', mask)
print('Realization is', format_realization)

# Import other important modules

import numpy as np
import pandas as pd
import xarray as xr
import datetime
import warnings
from cmip6_processing import calculate_niño

warnings.simplefilter("ignore","SerializationWarning:")

# Read in files from working directory
# Read in model data

data = xr.open_dataset(f'{dir}{filename}')

# Read in land mask

try:
    land_mask = xr.open_dataset(f'{mask}')
except FileNotFoundError:
    print("------------------------------------------")
    print(f"Land mask doesn't exist for {model}; no appropriate reprojection can be done")
    print("------------------------------------------")

# Assign data arrays to variables; mask out land surfaces

ts = data['ts']
if model != "MCM-UA-1-0":
    lon = data['lon']
    lat = data['lat']
else:
    lon = data['longitude']
    lat = data['latitude']

land_masked = ts.where(land_mask['sftlf'] != 100)
        
sst_anomalies = calculate_niño(land_masked)
print(f"Successfully calculated Niño 3.4 index for {format_realization}!")

# Send output to CSV

niño_output = pd.read_csv('/home/nathane1/Thesis/output/niño_3.4_table.csv')
niño_series = pd.Series(sst_anomalies, name= format_realization)
niño_output.insert(0, format_realization, niño_series)
niño_output.to_csv('/home/nathane1/Thesis/output/niño_3.4_table.csv')

# Send a nice message to the screen

print("-------------------------------------------------")
print(f"Successfully output realization {format_realization} for {model}!")
print("-------------------------------------------------")