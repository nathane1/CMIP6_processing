# Code to create boxplots for CMIP6 ensemble + observational data
# Author: Nathan Erickson
# Date: 11/1/2021
# Coded with Python 3.8.10

# Module importing; directory management

import os
import pandas as pd
import numpy as np
import seaborn as sns

path = '/home/nathane1/Thesis/output'
if not os.getcwd().endswith('output'):
    os.chdir(path)

# Read in data, do some partitioning into appropriate bins

data = pd.read_csv('ens_averages.csv', index_col = 'Datetimes')
ERSST = pd.read_csv('djf_ERSSTv5.csv', index_col='Unnamed: 0')
ERSST.index = ERSST.index.rename('Datetimes')

eli_nino_models = data.T.loc[[(np.mean(data[model]) > 165) for model in data]]
eli_neutral_models = data.T.loc[[(np.mean(data[model]) > 160) & (np.mean(data[model]) < 165) for model in data]]
eli_nina_models = data.T.loc[[(np.mean(data[model]) < 160) for model in data]]

eli_nino_models = eli_nino_models.append(ERSST.T)
eli_nina_models = eli_nina_models.append(ERSST.T)
#eli_neutral_models = eli_neutral_models.append(ERSST.T)

eli_nino_sortmodels = eli_nino_models.T[list(eli_nino_models.T.median().sort_values(ascending = False).index)]
eli_neutral_sortmodels = eli_neutral_models.T[list(eli_neutral_models.T.median().sort_values(ascending = False).index)].loc[:,~eli_neutral_models.T.columns.duplicated()]
eli_nina_sortmodels = eli_nina_models.T[list(eli_nina_models.T.median().sort_values(ascending = False).index)]

# Create boxplots of data based on different groups

la_nina_box = sns.boxplot(data = eli_nina_sortmodels, palette = 'winter_r')
la_nina_box.set_ybound(140,220)
la_nina_box.axhline(np.median(eli_nina_sortmodels['ERSST_v5']), ls = '--', color = 'k')
#la_nina_box.set_title('Distribution of ELI Values for La Niña-like Models compared with ERSST_v5', 
#                     size = 14, loc = 'center')
la_nina_box.set_title('ELI Distributions for La Niña-like Models', 
                     size = 14, loc = 'center')
la_nina_box.set_xticklabels(la_nina_box.get_xticklabels(),rotation = 69)
la_nina_box.set(xlabel = 'Models', ylabel = 'ELI (°E)')
ersst_box = la_nina_box.patches[len(eli_nina_sortmodels.T)-1]
ersst_box.set_facecolor('silver')

fig_dir = '/home/nathane1/Thesis/paper_images'
os.chdir(fig_dir)

la_nina_fig = la_nina_box.get_figure()
#la_nina_fig.savefig('la_nina_boxplot.jpg', bbox_inches = 'tight')


el_nino_box = sns.boxplot(data = eli_nino_sortmodels, palette = 'hot')
el_nino_box.set_ybound(140,220)
el_nino_box.axhline(np.median(eli_nino_sortmodels['ERSST_v5']), ls = '--', color = 'k')
#el_nino_box.set_title('Distribution of ELI Values for El Niño-like Models compared with ERSST_v5', 
#                     size = 14, loc = 'center')
el_nino_box.set_title('ELI Distributions for El Niño-like Models', 
                     size = 14, loc = 'center')
el_nino_box.set_xticklabels(el_nino_box.get_xticklabels(),rotation = 90)
el_nino_box.set(xlabel = 'Models', ylabel = 'ELI (°E)')
ersst_box = el_nino_box.patches[len(eli_nino_sortmodels.T)-1]
ersst_box.set_facecolor('silver')

os.chdir(fig_dir)

el_nino_fig = el_nino_box.get_figure()
#el_nino_fig.savefig('el_nino_boxplot.jpg', bbox_inches = 'tight')


neutral_box = sns.boxplot(data = eli_neutral_sortmodels, palette = 'YlGn')
neutral_box.set_ybound(140,220)
neutral_box.axhline(np.median(eli_neutral_sortmodels['ERSST_v5']), ls = '--', color = 'k')
neutral_box.set_title('Distribution of ELI Values for Neutral ENSO Models compared with ERSST_v5', 
                     size = 14, loc = 'center')
neutral_box.set_xticklabels(neutral_box.get_xticklabels(),rotation = 69)
neutral_box.set(xlabel = 'Models', ylabel = 'ELI (°E)')
ersst_box = neutral_box.patches[len(eli_neutral_sortmodels.T)-1]
ersst_box.set_facecolor('silver')

os.chdir(fig_dir)

neutral_fig = neutral_box.get_figure()
#neutral_fig.savefig('neutral_boxplot.jpg', bbox_inches = 'tight')

# Read in, sort data for Niño 3.4

os.chdir('/home/nathane1/Thesis')
niño_table = pd.read_csv('output/monthly_niño_averaged.csv', index_col = 'Unnamed: 0')
ERSST_niño = pd.read_csv('output/monthly_ERSST_niño.csv', index_col = 'Unnamed: 0')
niño_table = niño_table[4:171].join(ERSST_niño)

el_nino_models = niño_table.T.loc[[model for model in (eli_nino_sortmodels.columns & niño_table.columns)]]
la_nina_models = niño_table.T.loc[[model for model in (eli_nina_sortmodels.columns & niño_table.columns)]]
neutral_models = niño_table.T.loc[[model for model in (eli_neutral_sortmodels.columns & niño_table.columns)]]

la_nina_models = la_nina_models.sort_index(ascending=False).T

# Make boxplots for Niño 3.4

nino_en_box = sns.boxplot(data = el_nino_models.T, palette = 'hot')
nino_en_box.set_ybound(-1.25,1.25)
nino_en_box.axhline(np.nanmedian(el_nino_models.T['ERSST_v5']), ls = '--', color = 'k')
#nino_en_box.set_title('Distribution of Niño-3.4 Values for El Niño-like Models compared with ERSST_v5', 
#                     size = 14, loc = 'center')
nino_en_box.set_title('Niño-3.4 Distributions for El Niño-like Models', 
                     size = 14, loc = 'center')
nino_en_box.set_xticklabels(nino_en_box.get_xticklabels(),rotation = 90)
nino_en_box.set(xlabel = 'Models', ylabel = 'Niño-3.4 (°C)')
ersst_box = nino_en_box.artists[len(el_nino_models)-1]
ersst_box.set_facecolor('silver')

os.chdir(fig_dir)

nino_en_fig = nino_en_box.get_figure()
#nino_en_fig.savefig('nino_en_boxplot.jpg', bbox_inches = 'tight')

nino_ln_box = sns.boxplot(data = la_nina_models, palette = 'winter_r')
nino_ln_box.set_ybound(-1.25,1.25)
nino_ln_box.axhline(np.nanmedian(la_nina_models['ERSST_v5']), ls = '--', color = 'k')
nino_ln_box.set_title('Distribution of Niño-3.4 Values for La Niña-like Models compared with ERSST_v5', 
                     size = 14, loc = 'center')
nino_ln_box.set_xticklabels(nino_ln_box.get_xticklabels(),rotation = 69)
nino_ln_box.set(xlabel = 'Models', ylabel = 'Niño-3.4')
ersst_box = nino_ln_box.artists[len(la_nina_models.T)-1]
ersst_box.set_facecolor('silver')

os.chdir(fig_dir)

nino_ln_fig = nino_ln_box.get_figure()
#nino_ln_fig.savefig('nino_ln_boxplot.jpg', bbox_inches = 'tight')


nino_neutral_box = sns.boxplot(data = neutral_models.T, palette = 'YlGn')
nino_neutral_box.set_ybound(-1.25,1.25)
nino_neutral_box.axhline(np.nanmedian(neutral_models.T['ERSST_v5']), ls = '--', color = 'k')
nino_neutral_box.set_title('Distribution of Niño-3.4 Values for Neutral ENSO Models compared with ERSST_v5', 
                     size = 14, loc = 'center')
nino_neutral_box.set_xticklabels(nino_neutral_box.get_xticklabels(),rotation = 69)
nino_neutral_box.set(xlabel = 'Models', ylabel = 'Niño-3.4')
ersst_box = nino_neutral_box.artists[len(neutral_models)-1]
ersst_box.set_facecolor('silver')

os.chdir(fig_dir)

nino_neutral_fig = nino_neutral_box.get_figure()
#nino_neutral_fig.savefig('nino_neutral_boxplot.jpg', bbox_inches = 'tight')