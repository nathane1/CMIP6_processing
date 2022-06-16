# CMIP6_processing
Python scripts for processing, postprocessing, and plotting CMIP6 data

December 2021 - Coming soon!

June 2022 - Version 1.0 of CMIP6 processing
 - Added the following mainline components for the processing routine:
   - Processing:
     - ELI.py - Computes the ENSO Longitude Index (ELI) based upon input SST data for a model in the CMIP6 ensemble; outputs monthly ELI to a CSV
     - niño3-4.py - Computes the Niño 3.4 Index based upon input SST data for a model in the CMIP6 ensemble; outputs monthly Niño 3.4 data to a CSV
     - zonal_averages.py - Calculates zonally-averaged SSTs for a given longitude and time period
   - Postprocessing/Utility:  
     - significance_testing.py - Calculates statistical significance of changes in ELI/Niño 3.4 over some predefined period
     - iterateCMIP6.sh - Iterates over selected list of models in the CMIP6 ensemble to perform ELI/Niño 3.4 calculations
   - Plotting:
     - boxplots.py - Creates boxplot figures based upon ensemble ELI/Niño 3.4 data
     - heatmaps.py - Creates heatmap figures based upon ensemble ELI/Niño 3.4 data
     - histograms.py - Creates histogram figures based upon ensemble ELI/Niño 3.4 data
   - Packages:
     - __init__.py - Initializes cmip6_processing.py
     - cmip6_processing.py - Contains functions for processing CMIP6 data; see file for more in-depth descriptions of each
   
