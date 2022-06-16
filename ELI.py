# Script for processing data from CMIP6 ensemble for senior thesis project
# Author: Nathan Erickson
# Date: 9/27/2021
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

filename = f.split('CMIP6')[1]
realization_file = filename.split(f'{model}/')[1]
realization = realization_file.split('.nc')[0]

# Print a couple of sanity checks to the screen

print('---------------------------------------')
print('Starting run for', model)
print('Model data to be used is', filename)
print('Land mask for file is', mask)
print('Realization is', realization)

# Import other important modules

import numpy as np
import pandas as pd
import xarray as xr
import warnings
from lib import calculate_eli

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

# Set data arrays

ts = data['ts']
if model != "MCM-UA-1-0":
    lon = data['lon']
    lat = data['lat']
else:
    lon = data['longitude']
    lat = data['latitude']

# Apply land mask

land_masked = ts.where(land_mask['sftlf'] != 100)

# Calculate ELI

calculate_eli(ts_tropics,ts_pac)

# Send output to CSV

eli_output = pd.read_csv('/home/nathane1/Thesis/eli_table.csv')
ELI_series = pd.Series(monthly_ELI, name=realization)
eli_output.insert(0,realization,ELI_series)
eli_output.to_csv('/home/nathane1/Thesis/eli_table.csv')

# Send a nice message to the screen

print("-------------------------------------------------")
print(f"Successfully output realization {realization} for {model}!")
print("-------------------------------------------------")