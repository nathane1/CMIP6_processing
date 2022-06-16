# Code to create heatmaps for CMIP6 ensemble + observational data
# Author: Nathan Erickson
# Date: 10/26/2021
# Coded with Python 3.8.10

# Directory management; module importation

import os
import pandas as pd
import seaborn as sns

path = '/output'
if not os.getcwd().endswith('output'):
    os.chdir(path)
print(os.getcwd())

# Read in data for plotting

data = pd.read_csv('djf_data.csv', index_col = 'Unnamed: 0')

# Plot heatmap of ELI data

djf_heatmap = sns.heatmap(data.T.rolling(7).mean().T, cmap = 'RdBu_r', vmax = 180,
                         xticklabels = 40, cbar_kws = {'label':'ELI (°E)'})
djf_heatmap.set(yticklabels=[])
djf_heatmap.set_title('ELI Trend of Model Simulations from CMIP6', size = 16)
djf_heatmap.set_ylabel('CMIP6 Models', size = 12)
djf_heatmap.set_xticklabels(djf_heatmap.get_xticklabels(), rotation = 75)
djf_heatmap.set_xlabel('Time', size = 12)

heat_fig = djf_heatmap.get_figure()
img_dir = '/images'
os.chdir(img_dir)
#heat_fig.savefig('full_ens_heatmap.jpg', bbox_inches = 'tight')

# Plot heatmap of Niño 3.4 data

sim_heatmap = sns.heatmap(sim_data.rolling(7, center = True).mean().T.drop(columns = sim_data.T.columns[-15:]), cmap = 'RdBu_r',
                          vmax = 0.4, vmin = -0.4, xticklabels = 40, yticklabels = '', cbar_kws = {'label':'Niño-3.4 (°C)'})
sim_heatmap.set_title('Niño-3.4 Trend of Model Simulations from CMIP6')
sim_heatmap.set_xlabel('Time')
sim_heatmap.set_xticklabels(sim_heatmap.get_xticklabels(), rotation = 75)
sim_heatmap.set_ylabel('CMIP6 Models')

os.chdir(img_dir)
sim_fig = sim_heatmap.get_figure()
#sim_fig.savefig('full_ens_niño_heatmap.jpg', bbox_inches = 'tight')
