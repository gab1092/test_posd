#!/usr/bin/env python3
# -*- coding: utf-8 -*-



from glob import glob
import numpy as np
import xarray as xr

years=range(2019,2024)


for year in years:
    

    ds = xr.open_dataset(F'https://tds.hycom.org/thredds/dodsC/GOMu0.04/expt_90.1m000/data/hindcasts/'+ str(year) + '?depth[0],lat[0:1:345],lon[0:1:540],time')
    nt=len(ds.time[:])
    nt=nt-1
    cont1=0
    cont2=0;

    while cont2 < nt:
        cont1=cont1;
        cont2=cont1+31*24;
        
        if cont2 > nt:
            
            cont2=nt;
        else: 
            cont2=cont2;
            
        local = xr.Dataset()    
        ds = xr.open_dataset(F'https://tds.hycom.org/thredds/dodsC/GOMu0.04/expt_90.1m000/data/hindcasts/'+ str(year) + '?depth[0],lat[0:1:345],lon[0:1:540],time['+str(cont1)+':1:'+str(cont2)+'],water_u['+str(cont1)+':1:'+str(cont2)+'][0][0:1:345][0:1:540],water_v['+str(cont1)+':1:'+str(cont2)+'][0][0:1:345][0:1:540]')
        local =  xr.merge([local,ds])
        local.to_netcdf('/home/gaby.resendiz/HYCOM/hycom_'+str(year)+ str(cont2)+'.nc', mode='w', format='NETCDF4_CLASSIC')
        
        cont1=cont2+1;
