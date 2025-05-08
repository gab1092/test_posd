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


years=range(2018,2024)


for year in years:
    
    files_wrf=glob.glob('/home/gaby.resendiz/WRF_PROCESADO/*wrfout_d01_'+str(year)+'*')
    
    files_wrf.sort()
    ds=xr.open_mfdataset(files_wrf,concat_dim='time',combine='nested')
    ds2=xr.Dataset.drop_duplicates(ds,dim='time',keep='last')
    
    timestamp = ((ds2.time.values - np.datetime64('1970-01-01T00:00:00'))/np.timedelta64(1, 's'))
    hours=timestamp/3600;
    hours = np.array(hours)
    fillValue = 1.267651e+300  
    time=[]
    time.append(dt.datetime.fromtimestamp(0, dt.timezone.utc))
    t_units = time[0].strftime("hours since %Y-%m-%d %H:%M:%S UTC")
    
    data_u = ds2['u'][:] 
    data_v = ds2['v'][:] 
    data_lat = ds2['lat'][:]
    data_lon = ds2['lon'][:]
    
    base='/home/gaby.resendiz/WRF_PROCESADO/wrf_' 
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
           
