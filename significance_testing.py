# Code to perform significance testing on CMIP6 ensemble + observational data
# Author: Nathan Erickson
# Date: 10/26/2021
# Coded with Python 3.8.10

# Directory management

import os
path = '/home/nathane1/Thesis/output'
if not os.getcwd().endswith('output'):
    os.chdir(path)

# Read in data for significance testing

import pandas as pd
from scipy import stats

data = pd.read_csv('djf_data.csv', index_col = 'Unnamed: 0')
#data = pd.read_csv('monthly_niño.csv', index_col = 'Unnamed: 0')
if '1851' in data.index[0]:
    data = data.T
#print(data)

# Select future/historical data
future_data = data.T.loc[[(int(data.columns[datetime][:4]) >= 2050) 
                              for datetime in range(len(data.columns))]]
historical_data = data.T.loc[[(int(data.columns[datetime][:4]) > 1850) &
                              (int(data.columns[datetime][:4]) <= 1900)
                              for datetime in range(len(data.columns))]]

# Calculate T-scores (future_magnitude) and P-values (significance_future) for the dataset
future_magnitude = []
significance_future = []
for model in future_data.columns:
    future_magnitude.append(stats.ttest_ind(future_data[model].dropna(), historical_data[model].dropna()).statistic)
    significance_future.append(stats.ttest_ind(future_data[model].dropna(), historical_data[model].dropna()).pvalue)
    
significant_future = pd.DataFrame(data = significance_future, index = future_data.columns, 
                                  columns = ['Significant Differences in Future vs. Historical'])
significant_future = significant_future.dropna()

# Set up hue information for plotting
sig_hue = {}
for sindex,sim in enumerate(significant_future.index):
    if future_magnitude[sindex] > 0:
        sig_hue[sim] = 'r'
    if future_magnitude[sindex] < 0:
        sig_hue[sim] = 'b'
#significant_future.insert(0,'Significant Shading',sig_hue) #<- What's this for?

warming = dict((model,color) for model,color in sig_hue.items() if  color == 'r')
cooling = dict((model,color) for model,color in sig_hue.items() if  color == 'b')

# Plot significance values

import seaborn as sns   
import matplotlib.pyplot as plt
import numpy as np
        
sig_plot = sns.catplot(data = significant_future.T, kind = 'strip', palette = sig_hue, aspect = 2.0) 
sig_plot.refline(y=0.05, color = 'k', linestyle = '-', zorder = 100)
sig_plot.set(yticks = np.arange(0,1.1,0.1))
sig_plot.set_xticklabels([])
sig_plot.set_xlabels('Significant Differences between Historical and Future Climates', loc = 'center')
sig_plot.set(xticks=[])
sig_plot.set_ylabels('P-values')
sig_plot.fig.suptitle('ELI P-values for Differences between Historical and Future Climates', y = 1.05)
sig_plot.set(xmargin = 0.05)

fig_dir = os.path.join(path,'images/')
#sig_fig = sig_plot.get_figure()
if (os.getcwd().endswith('images') == False):
    os.chdir(fig_dir)
#sig_fig.savefig('sig_hf_paper_strip_plot_colored_sig.jpg', bbox_inches = 'tight')