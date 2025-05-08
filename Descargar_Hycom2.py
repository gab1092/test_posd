#!/usr/bin/env python3
# -*- coding: utf-8 -*-



from glob import glob
import numpy as np
import xarray as xr

years=range(2018,2019)


for year in years:

    ds = xr.open_dataset(F'http://tds.hycom.org/thredds/dodsC/GOMl0.04/expt_32.5/'+ str(year) + '/hrly?Depth[0],Latitude[0:1:384],Longitude[0:1:540],Date')
    nt=len(ds.Date[:])
    nt=nt-1
    cont1=0
    cont2=0

    while cont2 < nt:
        
        cont1=cont1;
        cont2=cont1+31*24;
        
        if cont2 > nt:
            
            cont2=nt;
        else: 
            cont2=cont2;
            
        local = xr.Dataset()    
        ds = xr.open_dataset(F'http://tds.hycom.org/thredds/dodsC/GOMl0.04/expt_32.5/'+ str(year) + '/hrly?Depth[0],Latitude[0:1:384],Longitude[0:1:540],Date['+str(cont1)+':1:'+str(cont2)+'],u['+str(cont1)+':1:'+str(cont2)+'][0][0:1:384][0:1:540],v['+str(cont1)+':1:'+str(cont2)+'][0][0:1:384][0:1:540]')
        local =  xr.merge([local,ds])
        local.to_netcdf('/home/gaby.resendiz/HYCOM/hycom_'+str(year)+ str(cont2)+'.nc', mode='w', format='netcdf4')
        
        cont1=cont2+1;
