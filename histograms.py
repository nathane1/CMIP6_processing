# Code to create histograms for CMIP6 ensemble + observational data
# Author: Nathan Erickson
# Date: 11/1/2021
# Coded with Python 3.8.10

# Module importing; directory management

import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

path = '/home/nathane1/Thesis/output'
if not os.getcwd().endswith('output'):
    os.chdir(path)

# Read in data, do some partitioning

data = pd.read_csv('ens_averages.csv', index_col = 'Datetimes')
ERSST = pd.read_csv('djf_ERSSTv5.csv', index_col='Unnamed: 0')
ERSST.index = ERSST.index.rename('Datetimes')


# Plot kernel density estimation for ELI

ens_palette = {}
for model in data:
    if np.mean(data[model]) < 160:
        ens_palette[model] = 'b'
    elif (np.mean(data[model]) > 160) & (np.mean(data[model]) < 165):
        ens_palette[model] = 'y'
    else:
        ens_palette[model] = 'r'
        
ens_zorder = {}
for model in data:
    ens_zorder[model] = -1 * np.mean(data[model])

ens_kde = sns.kdeplot(data = data, legend = False, palette = ens_palette)
for line_index,line in enumerate(ens_kde.lines):
    if line_index == len(data.T):
        break
    plt.setp(line, zorder = (-1 * np.median(data[data.columns[line_index]])))
ens_kde.axvline(x = np.median(ERSST['ERSST_v5']), label = 'ERSST_v5 Mean', color = 'k', zorder = 200)
ens_kde.set_title('Kernel Density Distribution of ELI for Ensemble Members')
ens_kde.set_xlabel('ELI (°E)')
ens_kde.set_ylabel('')
ens_kde.set_yticks([])
ens_kde.set_yticklabels([])

img_dir = '/home/nathane1/Thesis/images'
os.chdir(img_dir)
kde_fig = ens_kde.get_figure()
#kde_fig.savefig('ens_kde.jpg', bbox_inches = 'tight')

# Plot histogram of ELI distributions

ens_hist = sns.histplot(data = np.mean(data), kde = True)
ens_hist.set_title('Distribution of Mean ELI values for CMIP6 Ensemble')
ens_hist.axvline(label = 'ERSST_v5 Mean', x = np.mean(ERSST['ERSST_v5']), color = 'r')
ens_hist.set_xlabel('Mean ELI')

ens_fig = ens_hist.get_figure()
#ens_fig.savefig('ens_hist.jpg', bbox_inches = 'tight')