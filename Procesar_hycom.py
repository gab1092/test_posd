from xarray import open_dataset
from netCDF4 import Dataset
import os
import numpy as np
import datetime as dt
import glob
from os import system

#Este código es para procesar datos del HYCOM-IOA para usarlos con pygnome, en corridas para generar escenarios de derrame
#parte del proyecto posdoctoral de GRC- 


years=np.arange(1993,2020) 
meses=np.arange(1,13)
    
for year in years:
    for mes in meses:
        
        files_hycom=glob.glob('/home/gaby.resendiz/HYCOM_IOA/Clim_Mensual/'+ '{:0>2}'.format(mes) +'_mes/3z/*archv.'+str(year)+'*')
        
        for file in files_hycom:
            
            ds=open_dataset(file)
            data_u = ds['u'][:, 0, :, :]
            
            data_u=data_u[:].fillna(0) 
            
            data_v= ds['v'][:, 0, :, :]
            
            data_v=data_v[:].fillna(0) 
            
            data_t= ds['water_temp'][:, 0, :, :]
            data_s= ds['salinity'][:, 0, :, :]
            data_lon = ds['Longitude'] 
            data_lat = ds['Latitude']
            time = ds['MT']
            
            timestamp = ((ds.MT.values - np.datetime64('1970-01-01T00:00:00'))/np.timedelta64(1,'s'))
            hours=timestamp/3600;
            hours = np.array(hours)
            fillValue = 1.267651e+300
            time=[]
            time.append(dt.datetime.fromtimestamp(0, dt.timezone.utc))
            t_units = time[0].strftime("hours since %Y-%m-%d %H:%M:%S UTC")
            
            base='/home/gaby.resendiz/HYCOM_REPROCESADO_0/'
            file_name = os.path.basename(file)
            filename2=base+file_name
            dataset=Dataset(filename2, 'w', format='NETCDF4_CLASSIC')
            dataset.createDimension('time',hours.shape[0])
            dataset.createDimension('lat', data_lat.shape[0])
            dataset.createDimension('lon', data_lon.shape[0])
            time = dataset.createVariable('time', np.float64, ('time',)) 
            lon = dataset.createVariable('lon', np.float32, ('lon', ))
            lat = dataset.createVariable('lat', np.float32, ('lat', ))
            
            
            u = dataset.createVariable('u', (np.float32), ('time', 'lat', 'lon'),fill_value=fillValue) 
            v = dataset.createVariable('v', (np.float32), ('time', 'lat', 'lon'),fill_value=fillValue)

            temp = dataset.createVariable('temp', (np.float32), ('time', 'lat', 'lon'), fill_value=fillValue)
            salt = dataset.createVariable('salt', (np.float32), ('time', 'lat', 'lon'), fill_value=fillValue)
            
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
            
            u.long_name = 'Eastward Current Velocity'
            u.standard_name = 'eastward_sea_water_velocity'
            u.units = 'm/s'
            
            v.long_name = 'Northward Current Velocity'
            v.standard_name = 'northward_sea_water_velocity'
            v.units = 'm/s'
            
            temp.long_name='Sea water temperature'
            temp.standard_name = 'sea_water_temperature'
            temp.units = 'degC'
            
            salt.long_name='Sea water salinity'
            salt.standard_name='sea_water_salinity'
            salt.units='psu'
            
            lat[:] = data_lat
            lon[:] = data_lon
            time[:] = hours
            
            u[:] = data_u
            v[:] = data_v
            temp[:] = data_t
            salt[:] = data_s

            system("clear")
            
            print('Se proceso y guardó: ' + filename2)
            
            

