def calculate_eli(ssts):
    # Calculates ELI for given input datasets
    # Inputs:
    #  ssts: Global SST data, to be subsetted for ELI calculation
    # Returns:
    #  monthly_ELI: Monthly ELI values over the time period available in the input datasets
    
    # Import necessary modules
    import numpy as np
    
    # Set up empty lists for monthly average SSTs and monthly ELI values
    monthly_averages = []
    monthly_ELI = []
    
    # Slice data to include only between 5 S & 5 N and only equatorial Pacific
    ts_pac = ssts.sel(lon=slice(115,290),lat=slice(-5,5))
    ts_tropics = ssts.sel(lat=slice(-5,5))
    
    # Calculate ELI over the time range of the input dataset
    for t in range(0,len(sst_pac)):
        threshold_temp = np.nanmean(tropic_avg[t])
        monthly_averages.append(threshold_temp)# Find average SST of all points
        ELI_points = ts_pac[t]['lon'].where(ts_pac[t]>threshold_temp)
        ELI = np.nanmean(ELI_points)
        monthly_ELI.append(ELI)
        
        return monthly_ELI
    
def calculate_niño(ssts): 
    # Calculates the Niño 3.4 index over DJF for given input datasets
    # NOTE: Climatological mean interval is set to 5 by default, can be changed if desired!
    # Inputs:
    #  ssts: Global SST data, to be subsetted for ELI calculation
    # Returns:
    #  sst_anomalies: A list of monthly anomalies for DJF over the period of interest
    
    # Import necessary modules
    import numpy as np
    import datetime
    
    # Set up an empty list for monthly SST anomalies
    sst_anomalies= []
    
    # Select Niño 3.4 region
    ts_nino = ssts.sel(lon=slice(120,170),lat=slice(-5,5)) # <- Make sure to change me when switching between obs/model runs
    average_ts = ts_nino.mean(['lat','lon'])
    
    # Establish a background climatology to use for Niño 3.4 calculation
    avg_timesteps = 5 # Need to generalize the amount of timesteps
    
    try:
        average_jan = average_ts.loc[[np.datetime_as_string(average_ts['time'].values)[time][5:7]  == '01' for time in range(len(average_ts['time'].values))]]
        average_feb = average_ts.loc[[np.datetime_as_string(average_ts['time'].values)[time][5:7]  == '02' for time in range(len(average_ts['time'].values))]]
        average_dec = average_ts.loc[[np.datetime_as_string(average_ts['time'].values)[time][5:7]  == '12' for time in range(len(average_ts['time'].values))]]
    except TypeError:
        print("Looks like those aren't numpy datetimes, let's try a more general datetime approach.")
        pass
        try: 
            date_format = '%Y-%m-%d %H:%M:%S'
            average_jan = average_ts.loc[[datetime.datetime.strptime(str(data['time'][time].values), date_format).strftime(date_format)[5:7] == '01' for time in range(len(average_ts['time'].values))]]
            average_feb = average_ts.loc[[datetime.datetime.strptime(str(data['time'][time].values), date_format).strftime(date_format)[5:7] == '02' for time in range(len(average_ts['time'].values))]]
            average_dec = average_ts.loc[[datetime.datetime.strptime(str(data['time'][time].values), date_format).strftime(date_format)[5:7] == '12' for time in range(len(average_ts['time'].values))]]
        except TypeError:
            print("These datetimes are a real mess and need to be handled singularly in new code.")
                     
    clima_jan = average_jan.rolling(time = avg_timesteps, center = True).mean()
    clima_feb = average_feb.rolling(time = avg_timesteps, center = True).mean()
    clima_dec = average_dec.rolling(time = avg_timesteps, center = True).mean()

    clima_jan[0:15] = clima_jan[0:15].fillna(value = clima_jan[16])
    clima_jan[-15:] = clima_jan[-15:].fillna(value = clima_jan[-16])
    clima_feb[0:15] = clima_feb[0:15].fillna(value = clima_feb[16])
    clima_feb[-15:] = clima_feb[-15:].fillna(value = clima_feb[-16])
    clima_dec[0:15] = clima_dec[0:15].fillna(value = clima_dec[16])
    clima_dec[-15:] = clima_dec[-15:].fillna(value = clima_dec[-16])
    
    # Calculate Niño 3.4 index for the dataset
    for t in range(0,len(ts_nino)):
        try:
            jan_anom = float((average_jan[t] - clima_jan[t]).values)
            feb_anom = float((average_feb[t] - clima_feb[t]).values)
            dec_anom = float((average_dec[t] - clima_dec[t]).values)
            sst_anomalies.append(jan_anom)
            sst_anomalies.append(feb_anom)
            sst_anomalies.append(dec_anom)
        except:
            break
            print("Calculation failed :(")
    
    return sst_anomalies

def format_names(in_table):
    # Formats file names to be more easily interpretable for end users
    # Inputs:
    #  in_table: An input table of CMIP6 data (preferably in pandas format) with column names to be converted
    # Returns:
    #  out_table: An output table with more nicely formatted column names corresponding to each realization
    
    # Transpose input table to required shape if necessary
    if in_table.columns[0][0] != 't':
        in_table = in_table.T
        
    # Set up empty list for formatted simulation names    
    format_sim_names = []
    
    # Format simulation names into a more readable format, based on their file names
    for sim in range(len(in_table.T.index)):
        format_name = in_table.columns[sim].split('_')[2] + ': Realization ' + in_table.columns[sim].split('_r')[1][0] + ', Initialization ' + in_table.columns[sim].split('_r')[1].split('i')[1][0] + ', Physics ' + in_table.columns[sim].split('_r')[1].split('p')[1][0] + ', Forcing ' + in_table.columns[sim].split('_r')[1].split('f')[1][0]
        format_sim_names.append(format_name)
    in_table.columns = format_sim_names
    out_table = in_table.T
    
    return out_table

def djf_averages(eli_file, start_year, end_year):
    # Calculates DJF average values of ELI from a monthly means dataset
    # Inputs:
    #  eli_file: File containing monthly ELI values
    #  start_year: The year corresponding to the start of the averaging period
    #  end_year: The year corresponding to the end of the averaging period
    # Returns:
    #  djf_averages: ELI values averaged over successive DJF seasons
    #  djf_datetime: Formatted index of datetimes corresponding to the period of interest
    
    # Import necessary modules
    import numpy as np
    import pandas as pd
    
    # Select only ELI rows from DJF
    eli_table = pd.read_csv(eli_file)
    djf_table = eli_table.loc[[(pd.Index(eli_table.index)[time][5:] == '12') or (pd.Index(eli_table.index)[time][5:] == '01') or (pd.Index(eli_table.index)[time][5:] == '02') for time in range(len(eli_table.index))]]
    djf_listed = []
    for model in djf_table.columns[range(len(djf_table.T))]:
        djf_listed.append(model)

    # Take means of sequential DJF seasons
    mean_list = []
    for model in djf_table.columns[range(len(djf_table.T))]:
        for month in range(len(djf_table)):
            mean_list.append(np.mean(djf_table[model][month:month+3]))

    # Remove final element from each model list to avoid bad averages at end of period
    djf_naiveaverages = mean_list[2::3]
    # Line below is not appropriately generalized
    djf_averages = [djf_naiveaverages[x:x+251] for x in range(0,len(djf_naiveaverages),251)] 
    for lonely_december in djf_averages:
            del lonely_december[len(lonely_december)-1]

    # Create a new datetime-like index for a finalized dataframe with only DJF data
    djf_dates_start = pd.date_range(start=f'{start_year}',periods=len(djf_averages[0]),freq='Y')
    djf_dates_end = pd.date_range(start=f'{end_year}',periods=len(djf_averages[0]),freq='Y')
    djf_datetime = []
    for date in range(len(djf_dates)):
        djf_datetime.append(f'{str(djf_dates_start[date])[0:4]}-{str(djf_dates_end[date])[0:4]}')
        
    return djf_averages
    return djf_datetime

def model_formatter(realization):
    # Formats model names to be used in code
    # Inputs:
    #  realization: File name denoting a specific realization from one particular model
    # Returns:
    #  format_realization: A formatted name specific to the input realization
    
    # Subset the string for only the parts relevant for the formatted name
    format_realization = realization.split('1850')[0][8:-4]
    
    return format_realization

def sst_bias_ens_calculator(model, model_list):
    # Calculates average SST biases for a given model in CMIP6; can be iterated over to calculate for the entire ensemble
    # Inputs:
    #  model: The model for which bias calculations will be performed
    #  model_list: List of model names
    # Returns:
    #  model_run: The name of the model, for convenience purposes
    #  Sends file output to 'composite_bias.nc' (can be used to perform ensemble bias calculations)
    
    # Import necessary modules
    import os
    import glob
    import xarray as xr
    import numpy as np
    from datetime import datetime
    
    # Open observational SST dataset
    data_dir = '/chinook2/nathane1/Thesis/'
    os.chdir(data_dir)
    obs_ssts = xr.open_dataset('sst.mnmean.nc')
    
    # Get model simulations, combine them into one variable
    model_run = model_list[model]
    model_dir = data_dir + 'CMIP6/' + model_run
    os.chdir(model_dir)
    model_filename = f'ts_Amon_{model_run}*.nc'
    model_file = glob.glob(model_filename)
    model_ssts = [xr.open_dataset(f'{model_dir}/{model_file[file]}') for file in range(len(model_file))]
    
    # Time/dimension formatting options
    sims = range(len(model_file))
    if model_ssts[0]['time'].dtype != '<M8[ns]': # <M8[ns] = datetime data type
        for sim in sims:
            model_ssts[sim]['time'] = model_ssts[sim].indexes['time'].to_datetimeindex()
    if 'EC-Earth3' in model_run:
        for sim in sims:
            model_ssts[sim] = model_ssts[sim].sel(time = slice('1850-01-16T12:00:00.000000000','2100-12-16T12:00:00.000000000'), lat = slice(-20,20))
            
    # Get averages across all simulations for model
    for sim in sims:
        if 'model_sims' in locals():
            model_sims += model_ssts[sim].ts
        else:
            model_sims = model_ssts[0].ts
    model_avg = model_sims / len(sims)
    
    # Get land mask
    os.chdir(model_dir)
    mask_filename = f'sftlf_fx_{model_run}*.nc'
    mask_file = glob.glob(mask_filename)
    land_mask = xr.open_dataset(mask_file[0])
    land_mask = land_mask.interp_like(obs_ssts.lon).interp_like(obs_ssts.lat)
    
    # Interpolate to common grid to prepare cross-model averages
    comb_ssts = model_avg.interp_like(obs_ssts.sst)
    
    # Convert SSTs to Kelvin; calculate bias
    sst_bias = comb_ssts - (obs_ssts.sst + 273.15) # Need to add in a Celsius/Kelvin correction
    
    # Select only those records from DJF
    djf_bias = sst_bias.loc[[(np.datetime_as_string(sst_bias['time'].values)[time][5:7]  == '01') or
              (np.datetime_as_string(sst_bias['time'].values)[time][5:7]  == '02') or
              (np.datetime_as_string(sst_bias['time'].values)[time][5:7]  == '12') for time in range(len(sst_bias['time'].values))]]
    
    # Calculate cumulative bias over time
    period_djf_bias = djf_bias.groupby("lat").mean("time")
    #print(period_djf_bias)
    if land_mask['sftlf'].max() == 10:
        period_djf_bias = period_djf_bias.where(land_mask['sftlf'] <= 10)
    else:
        period_djf_bias = period_djf_bias.where(land_mask['sftlf'] != land_mask['sftlf'].max().values) # <- This is an imperfect check that could use some work
    
    # Run check for extraneous variables
    try:
        period_djf_bias = period_djf_bias.drop_vars('type')
    except ValueError:
        pass
    
    # Average together across all models
    os.chdir(data_dir)
    try:
        period_djf_bias.to_dataset(name=f'{model_run}-ts').to_netcdf('composite_bias.nc',mode = 'a')
    except FileNotFoundError:
        period_djf_bias.to_dataset(name = f'{model_run}-ts').to_netcdf('composite_bias.nc',mode = 'w')

    # Do some variable cleanup
    del model_ssts, model_sims, model_avg, land_mask, comb_ssts, sst_bias, djf_bias, period_djf_bias
    try:
        del intermediate, model_composite
    except UnboundLocalError:
        pass

    return model_run

def sst_change_ens_calculator(model, model_list):
    # Calculates average SST change for a given model in CMIP6; can be iterated over to calculate for the entire ensemble
    # Inputs:
    #  model: The model for which bias calculations will be performed
    #  model_list: List of model names
    # Returns:
    #  model_run: The name of the model, for convenience purposes
    #  Sends file output to 'composite_bias.nc' (can be used to perform ensemble bias calculations)
    
    # Import necessary modules
    import os
    import glob
    import xarray as xr
    import numpy as np
    from datetime import datetime
    
    # Open observational SST dataset
    data_dir = '/chinook2/nathane1/Thesis/'
    os.chdir(data_dir)
    obs_ssts = xr.open_dataset('sst.mnmean.nc')
    
    # Get model simulations, combine them into one variable
    model_run = model_list[model]
    model_dir = data_dir + 'CMIP6/' + model_run
    os.chdir(model_dir)
    model_filename = f'ts_Amon_{model_run}*.nc'
    model_file = glob.glob(model_filename)
    model_ssts = [xr.open_dataset(f'{model_dir}/{model_file[file]}') for file in range(len(model_file))]
    
    # Time/dimension formatting options
    sims = range(len(model_file))
    if model_ssts[0]['time'].dtype != '<M8[ns]': # <M8[ns] = datetime data type
        for sim in sims:
            model_ssts[sim]['time'] = model_ssts[sim].indexes['time'].to_datetimeindex()
    if 'EC-Earth3' in model_run:
        for sim in sims:
            model_ssts[sim] = model_ssts[sim].sel(time = slice('1850-01-16T12:00:00.000000000','2100-12-16T12:00:00.000000000'), lat = slice(-20,20))
    
    # Get averages across all simulations for model
    for sim in sims:
        if 'model_sims' in locals():
            model_sims += model_ssts[sim].ts
        else:
            model_sims = model_ssts[0].ts
    model_avg = model_sims / len(sims)
    
    # Get land mask
    os.chdir(model_dir)
    mask_filename = f'sftlf_fx_{model_run}*.nc'
    mask_file = glob.glob(mask_filename)
    land_mask = xr.open_dataset(mask_file[0])
    land_mask = land_mask.interp_like(obs_ssts.lon).interp_like(obs_ssts.lat)
    
    # Interpolate to common grid to prepare cross-model averages
    comb_ssts = model_avg.interp_like(obs_ssts.lon).interp_like(obs_ssts.lat)
    
    # Select only those records from DJF
    djf_change = comb_ssts.loc[[(np.datetime_as_string(comb_ssts['time'].values)[time][5:7]  == '01') or
              (np.datetime_as_string(comb_ssts['time'].values)[time][5:7]  == '02') or
              (np.datetime_as_string(comb_ssts['time'].values)[time][5:7]  == '12') for time in range(len(comb_ssts['time'].values))]]
    
    # Establish bounds to use from the historical and future periods
    future_start = np.datetime64(np.datetime64('2050-02-16T12:00:00.000000000'))
    future_data = djf_change.sel(time=slice('2050-02-16T12:00:00.000000000','2101-01-01T12:00:00.000000000'))
    historical_data = djf_change.sel(time=slice('1850-01-01T12:00:00.000000000','1900-01-01T12:00:00.000000000'))
    
    # Average the data over time
    future_avg = future_data.groupby("lat").mean("time")
    historical_avg = historical_data.groupby("lat").mean("time")
    
    # Calculate the change between the future and historical periods
    sst_change = future_avg - historical_avg
    if land_mask['sftlf'].max() == 10:
        sst_change = sst_change.where(land_mask['sftlf'] <= 10)
    else:
        sst_change = sst_change.where(land_mask['sftlf'] != land_mask['sftlf'].max().values) # <- This is an imperfect check that could use some work
        
    # Run check for extraneous variables
    try:
        sst_change = sst_change.drop_vars('type')
    except ValueError:
        pass
    
    # Send to composite dataset
    os.chdir(data_dir)
    try:
        sst_change.to_dataset(name=f'{model_run}-ts').to_netcdf('composite_change.nc',mode = 'a')
    except FileNotFoundError:
        sst_change.to_dataset(name = f'{model_run}-ts').to_netcdf('composite_change.nc',mode = 'w')

    # Do some variable cleanup
    del obs_ssts, model_ssts, model_sims, model_avg, land_mask, comb_ssts, future_data, historical_data
    del future_avg, historical_avg, sst_change, djf_change
    try:
        del intermediate, model_composite
    except UnboundLocalError:
        pass
    return model_run
    
def zonal_avg_ens_calculator(model, time_option, lon_bounds, lat_bounds):
    # Calculates zonally averaged SST biases for a given model in CMIP6; can be iterated over to calculate for the entire ensemble
    # Inputs:
    #  model: The model for which bias calculations will be performed
    #  time_option: Used to specify annual zonal averages or only DJF (can be modified further to incorporate any season)
    #  lon_bounds: Longitudinal bounds to subset the input dataset appropriately
    #  lat_bounds: Latitudinal bounds to subset the input dataset appropriately
    # Returns:
    #  model_run: The name of the model, for convenience purposes
    #  Sends file output to 'djf_zonal_averages.nc' (can be used to perform ensemble bias calculations)
    
    # Import necessary modules
    import os
    import glob
    import xarray as xr
    import numpy as np
    from datetime import datetime
    
    # Get model simulations, combine them into one variable
    model_run = model_list[model]
    model_dir = data_dir + 'CMIP6/' + model_run
    os.chdir(model_dir)
    model_filename = f'ts_Amon_{model_run}*.nc'
    model_file = glob.glob(model_filename)
    model_ssts = [xr.open_dataset(f'{model_dir}/{model_file[file]}') for file in range(len(model_file))]
    
    # Time/dimension formatting options
    sims = range(len(model_file))
    if model_ssts[0]['time'].dtype != '<M8[ns]': # <M8[ns] = datetime data type
        for sim in sims:
            model_ssts[sim]['time'] = model_ssts[sim].indexes['time'].to_datetimeindex()
    if 'EC-Earth3' in model_run:
        for sim in sims:
            model_ssts[sim] = model_ssts[sim].sel(time = slice('1850-01-16T12:00:00.000000000','2100-12-16T12:00:00.000000000'), lat = slice(5,-5))
            
    # Get averages across all simulations for model
    for sim in sims:
        if 'model_sims' in locals():
            model_sims += model_ssts[sim].ts
        else:
            model_sims = model_ssts[0].ts
    model_avg = model_sims / len(sims)
    
    # Select only DJF data if desired
    if time_option == 'year':
        pass
    elif time_option == ('djf' or 'DJF'):
        model_avg = model_avg.loc[[(np.datetime_as_string(model_avg['time'].values)[time][5:7]  == '01') or
              (np.datetime_as_string(model_avg['time'].values)[time][5:7]  == '02') or
              (np.datetime_as_string(model_avg['time'].values)[time][5:7]  == '12') for time in range(len(model_avg['time'].values))]]
    else:
        raise ValueError('Please input "year" to keep whole year or "DJF" to subset for DJF') 
        
    # Get land mask
    os.chdir(model_dir)
    mask_filename = f'sftlf_fx_{model_run}*.nc'
    mask_file = glob.glob(mask_filename)
    land_mask = xr.open_dataset(mask_file[0])
    
    # Interpolate to obs grid
    comb_ssts = model_avg.interp_like(obs_ssts.sst)
    
    # Convert SSTs to Kelvin
    conv_ssts = comb_ssts - 273.15
    
    # Average over latitude and time
    sst_tropics = conv_ssts.sel(lat=slice(lat_bounds[0],lat_bounds[1]), lon=slice(lon_bounds[0],lon_bounds[1]))
    zonal_avg = sst_tropics.groupby("time").mean("lat")
    zonal_period_avg = zonal_avg.groupby("lon").mean("time")
    
    # Send to temp. dataset, clear initial dataset
    dummy_dataset = zonal_period_avg
    dummy_dataset = dummy_dataset.to_dataset()
    if 'temp_dataset' not in locals():
        temp_dataset = dummy_dataset.rename_vars({'ts':f'{model_run}-ts'})
    else:
        temp_dataset = xr.merge([temp_dataset,dummy_dataset.ts])
        temp_dataset = temp_dataset.rename_vars({'ts':f'{model_run}-ts'})
        
    # Save results to outfile
    os.chdir(data_dir)
    out_file = 'djf_zonal_averages.nc'
    if os.path.isfile(out_file) == True:
        temp_dataset.to_netcdf('djf_zonal_averages.nc',mode='a')
    else:
        temp_dataset.to_netcdf('djf_zonal_averages.nc',mode='w')
    del model_ssts, model_sims, land_mask, comb_ssts, conv_ssts, sst_tropics, zonal_avg, zonal_period_avg, dummy_dataset, temp_dataset
    return model_run

def zonal_diff_ens_calculator(model, time_option, period, lon_bounds, lat_bounds):
    # Calculates zonally averaged SST biases for a given model in CMIP6; can be iterated over to calculate for the entire ensemble
    # Inputs:
    #  model: The model for which bias calculations will be performed
    #  time_option: Used to specify annual zonal averages or only DJF (can be modified further to incorporate any season)
    #  period: Can specify 'hist+future' for historical (1851-1900) and future (2051-2100) comparisons; can also be modified for different periods
    #  lon_bounds: Longitudinal bounds to subset the input dataset appropriately
    #  lat_bounds: Latitudinal bounds to subset the input dataset appropriately
    # Returns:
    #  model_run: The name of the model, for convenience purposes
    #  Sends file output to 'hist_zonal_averages.nc' and 'future_zonal_averages.nc' (can be used to perform ensemble bias calculations)
    
    # Import necessary modules
    import os
    import glob
    import xarray as xr
    import numpy as np
    from datetime import datetime
    
    # Get model simulations, combine them into one variable
    model_run = model_list[model]
    model_dir = data_dir + 'CMIP6/' + model_run
    os.chdir(model_dir)
    model_filename = f'ts_Amon_{model_run}*.nc'
    model_file = glob.glob(model_filename)
    model_ssts = [xr.open_dataset(f'{model_dir}/{model_file[file]}') for file in range(len(model_file))]
    
    # Get land mask
    os.chdir(model_dir)
    mask_filename = f'sftlf_fx_{model_run}*.nc'
    mask_file = glob.glob(mask_filename)
    land_mask = xr.open_dataset(mask_file[0])
    
    # Time/dimension formatting options
    sims = range(len(model_file))
    if model_ssts[0]['time'].dtype != '<M8[ns]': # <M8[ns] = datetime data type
        for sim in sims:
            model_ssts[sim]['time'] = model_ssts[sim].indexes['time'].to_datetimeindex()
    if 'EC-Earth3' in model_run:
        for sim in sims:
            model_ssts[sim] = model_ssts[sim].sel(time = slice('1850-01-16T12:00:00.000000000','2100-12-16T12:00:00.000000000'), lat = slice(5,-5))
            
    # Get averages across all simulations for model
    for sim in sims:
        if 'model_sims' in locals():
            model_sims += model_ssts[sim].ts
        else:
            model_sims = model_ssts[0].ts
    model_avg = model_sims / len(sims)
    
    # Perform data subsetting if desired
    if time_option == ('djf' or 'DJF'):
        model_avg = model_avg.loc[[(np.datetime_as_string(model_avg['time'].values)[time][5:7]  == '01') or
              (np.datetime_as_string(model_avg['time'].values)[time][5:7]  == '02') or
              (np.datetime_as_string(model_avg['time'].values)[time][5:7]  == '12') for time in range(len(model_avg['time'].values))]]
    else:
        pass
    if period == ('hist+future'):
        historical_ssts = model_avg.loc[dict(time=slice('1851-01-01','1900-12-01'))]
        future_ssts = model_avg.loc[dict(time=slice('2051-01-01','2100-12-01'))]
    else:
        pass
    
    # Interpolate to common grid
    interp_hist = historical_ssts.interp_like(obs_ssts.sst)
    interp_future = future_ssts.interp_like(obs_ssts.lon).interp_like(obs_ssts.lat)
    
    # Convert SSTs to Kelvin
    conv_hist = interp_hist - 273.15
    conv_future = interp_future - 273.15
    
    # Average over latitude and time
    hist_tropics = conv_hist.sel(lat=slice(lat_bounds[0],lat_bounds[1]), lon=slice(lon_bounds[0],lon_bounds[1]))
    hist_avg = hist_tropics.groupby("time").mean("lat")
    zonal_hist_avg = hist_avg.groupby("lon").mean("time")
    
    future_tropics = conv_future.sel(lat=slice(lat_bounds[0],lat_bounds[1]), lon=slice(lon_bounds[0],lon_bounds[1]))
    future_avg = future_tropics.groupby("time").mean("lat")
    zonal_future_avg = future_avg.groupby("lon").mean("time")
    
    # Send to temp. dataset, clear initial dataset
    dummy_1 = zonal_hist_avg
    dummy_1 = dummy_1.to_dataset()
    
    dummy_2 = zonal_future_avg
    dummy_2 = dummy_2.to_dataset()
    if 'temp_dataset' not in locals():
        temp_dataset_hist = dummy_1.rename_vars({'ts':f'{model_run}-ts'})
    else:
        temp_dataset_hist = xr.merge([temp_dataset_hist,dummy_1.ts])
        temp_dataset_hist = temp_dataset_hist.rename_vars({'ts':f'{model_run}-ts'})
    if 'temp_dataset1' not in locals():
        temp_dataset_fut = dummy_2.rename_vars({'ts':f'{model_run}-ts'})
    else:
        temp_dataset_fut = xr.merge([temp_dataset_fut,dummy_2.ts])
        temp_dataset_fut = temp_dataset_fut.rename_vars({'ts':f'{model_run}-ts'})
    # Save results to outfile
    os.chdir(data_dir)
    out_files = ['hist_zonal_averages.nc','future_zonal_averages.nc']      
    if os.path.isfile(out_files[0]) == True: #This code right here sucks, generalize this
        temp_dataset_hist.to_netcdf(out_files[0],mode='a')
        temp_dataset_fut.to_netcdf(out_files[1],mode='a')
    else:
        temp_dataset_hist.to_netcdf(out_files[0],mode='w')
        temp_dataset_fut.to_netcdf(out_files[1],mode='w')
    del model_ssts, model_sims, land_mask, model_avg, historical_ssts, future_ssts 
    del interp_hist, interp_future, conv_hist, conv_future, hist_tropics, hist_avg, zonal_hist_avg
    del future_tropics, future_avg, zonal_future_avg, temp_dataset_hist, temp_dataset_fut
    del dummy_1, dummy_2, out_files
    return model_run