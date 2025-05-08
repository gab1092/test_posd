#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 13:42:48 2024

@author: gresendiz
Basado y adaptado de hycom_download/download.py de ma-robles
Código para procesar datos de WRF-IOA para usarlos como insumos en corridas
de Pygnome y Opendrift
"""

import xarray as xr

from netCDF4 import Dataset

import glob

import numpy as np

import datetime as dt


years=range(1993,2019)


for year in years:
    
    #files_wrf=glob.glob('/home/gaby.resendiz/WRF_REANALISIS_PROC/*wrfout_d01_'+str(year)+'*')
    
    files_wrf=glob.glob('/home/gaby.resendiz/RESPALDO_V4/a'+str(year)+'/salidas/wrfout_c1h_d01_'+str(year)+'*')
    files_wrf.sort()
    
    ds=xr.open_mfdataset(files_wrf,concat_dim='Times',combine='nested') #revisar si la dimensión es time
    ds3=xr.open_dataset('/home/gaby.resendiz/RESPALDO_V4/a2019/salidas/wrfout_c15d_d01_2019-10-28_00:00:00.a2019')

    #REVISAR como viene el tiempo y como debe ir en esta sección:
    timestamp = ((ds.time.values - np.datetime64('1970-01-01T00:00:00'))/np.timedelta64(1, 's'))
    hours=timestamp/3600;
    hours = np.array(hours)
    fillValue = 1.267651e+300  
    time=[]
    time.append(dt.datetime.fromtimestamp(0, dt.timezone.utc))
    t_units = time[0].strftime("hours since %Y-%m-%d %H:%M:%S UTC")

    #variables u y v horarias. Variables lon y lat vienen del archivo grid, dia 15
    data_u = ds2['U10'][:] 
    data_v = ds2['V10'][:] 
    data_lat = ds3['lat'][:]
    data_lon = ds3['lon'][:]
    
    base='/home/gaby.resendiz/WRF_REANALISIS_PROC/wrf_' 
    filename2=base+str(year) 
    dataset=Dataset(filename2, 'w', format='NETCDF4_CLASSIC')
    
    dataset.createDimension('time',hours.shape[0])
    dataset.createDimension('lat', data_lat.shape[0]) 
    dataset.createDimension('lon', data_lon.shape[0])
    time = dataset.createVariable('time', np.float64, ('time', )) 
    lon = dataset.createVariable('lon', np.float32, ('lon', )) 
    lat = dataset.createVariable('lat', np.float32, ('lat', )) 
    u = dataset.createVariable('u', (np.float32), ('time', 'lat', 'lon'), fill_value=fillValue) 
    v = dataset.createVariable('v', (np.float32), ('time', 'lat', 'lon'), fill_value=fillValue) 
    dataset.grid_type = 'REGULAR'
    lat.long_name = 'Latitude'
    lat.units = 'degrees_north' 
    lat.standard_name = 'latitude' 
    lon.long_name = 'Longitude' 
    lon.units = 'degrees_east' 
    lon.standard_name = 'longitude'
    time.long_name = 'Time'
    time.units =t_units
    time.standard_name = 'time' 
    u.long_name = 'Eastward Air Velocity'
    u.standard_name = 'eastward_wind'
    u.units = 'm/s'
    v.long_name = 'Northward Air Velocity'
    v.standard_name = 'northward_wind'
    v.units = 'm/s' 
    lat[:] = data_lat
    lon[:] = data_lon
    time[:] = hours
    u[:] = data_u
    v[:] = data_v
    print('Se proceso y guardó: ' + filename2)
           
