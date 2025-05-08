from xarray import open_dataset
from netCDF4 import Dataset
import os
import numpy as np
import datetime as dt
import re


years=np.arange(1993,2020)

ds2=open_dataset('/home/gaby.resendiz/RESPALDO_V4/a2019/salidas/wrfout_c15d_d01_2019-10-28_00:00:00.a2019')

for year in years:
    
    files_wrf=os.listdir('/home/gaby.resendiz/RESPALDO_V4/a'+ str(year)+'/salidas/')


        
    for file in files_wrf:
        
            pattern = re.compile(r'wrfout_c1h_d01_')
            
            if re.search(pattern, file):
                
                ds=open_dataset('/home/gaby.resendiz/RESPALDO_V4/a'+str(year)+'/salidas/'+file,decode_times=False)
                data_u = ds['U10'][:] 
                data_v = ds['V10'][:] 
                data_lat = ds2['XLAT'][0,:,0] 
                data_lon = ds2['XLONG'][0,0,:] 
                time = ds['XTIME'][:]
                secs = ds['Time'][:]
                time=np.array(time)
                hours=np.arange(0,24)
                cont=0


                for tt in time:
                    
                    timeaux=np.datetime64(str(year)+'-01-01T00:00:00')+np.timedelta64(np.int32(tt),'m')
                    timestamp= ((timeaux - np.datetime64('1970-01-01T00:00:00'))/np.timedelta64(1, 's'))
                    hours[cont]=timestamp/3600;
                    cont=cont+1
                
                hours = np.array(hours)
                fillValue = 1.267651e+300
                time=[]
                time.append(dt.datetime.fromtimestamp(secs[0].values, dt.timezone.utc))
                t_units = time[0].strftime("hours since %Y-%m-%d %H:%M:%S UTC")
                base='/home/gaby.resendiz/WRF_REANALISIS_PROC/'
                file_name = os.path.basename(file)
                filename2=base+file_name
                dataset=Dataset(filename2, 'w', format='NETCDF3_CLASSIC')
                dataset.createDimension('time', hours.shape[0]) 
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
                time.units = t_units 
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
                print('Se proceso y guardó: ' + file)
