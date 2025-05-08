##Agosto 6: Este código ya funciona para corridas en el clúster. Hay que preparar los ciclos y las diferentes posiciones. 
##Corre con reanalisis wrf y HYCOM climatologia IOA

import os

from datetime import datetime, timedelta

import gnome.scripting as gs

from gnome.outputters import NetCDFOutput

from gnome.weatherers import Evaporation, NaturalDispersion, Emulsification, Biodegradation, Dissolution

from gnome.environment import Water, Waves

from gnome.movers import RandomMover3D, RiseVelocityMover

import numpy as np

import glob
import netCDF4 as nc4




lon=-97.51
lat=22.28


nombre='Arenque_Experimento1'

year=1994
duracion_sim=15
mes='01'
dia='05'
duracion_derrame=15

start_time = datetime(year, int(mes), int(dia), 12, 0) #Hora UTC
    ##cargando el archivo de costa 
mymap = gs.MapFromBNA('/home/gaby.resendiz/costa/Costa_Conabio.bna', refloat_halflife=1)

    ##cargando al modelo archivo de costa , viento etc
model = gs.Model(start_time=start_time, duration=timedelta(days=duracion_sim), time_step=gs.minutes(60),map=mymap)
    
    
files_hycom=glob.glob('/home/gaby.resendiz/HYCOM_REPROCESADO/'+'*archv.'+str(year)+'*')

 #HYCOM_IOA/Clim_Mensual/01_mes/3z/archv.2000_003_00_3z.nc
 
files_hycom.sort()

df=nc4.MFDataset(files_hycom,aggdim='time')

c_mover=gs.CurrentMover.from_netCDF(df)
model.movers += c_mover

#c_mover=gs.GridCurrent.from_netCDF(df)
    
#c_mover=gs.CurrentMover.from_netCDF(df)

#current = GridCurrent.from_netCDF(dataset=df)

#model.movers += c_mover

##opcion
#current = gs.GridCurrent.from_netCDF(file_list)
#py_current_mover = gs.CurrentMover(current=current)
#model.movers += py_current_mover

#files_wrf=glob.glob('/home/gaby.resendiz/WRF_PROCESADO/*wrfout_d01_'+str(year)+'-'+mes+'-'+dia+'*')
    
#files_wrf.sort()
    
#dw=nc4.MFDataset(files_wrf,aggdim='time')
##dw=nc4.MFDataset(files_wrf,aggdim='time')
##reanalisis wrf

#WRF_REANALISIS_PROC/wrfout_c1h_d01_1993-01-04_00:00:00.a1993

files_wrf=glob.glob('/home/gaby.resendiz/WRF_REANALISIS_PROC/wrfout_c1h_d01_'+str(year)+'-'+mes+'*')
files_wrf.sort()
dw=nc4.MFDataset(files_wrf,aggdim='time')


w_mover = gs.WindMover.from_netCDF(dw)

#w_mover = gs.WindMover.from_netCDF('/home/gaby.resendiz/WRF_PROCESADO/wrf_'+str(year))
#model.movers += c_mover

model.movers += w_mover


w_obj = gs.GridWind.from_netCDF(dw)
water = Water(temperature=300.0, salinity=35.0) #temperature in Kelvin, salinity in psu
waves = Waves(wind=w_obj,water=water)


model.environment += waves

model.weatherers += Evaporation(wind=w_obj,water=water)
model.weatherers += NaturalDispersion()
#model.weatherers += Emulsification(waves=waves)
#model.weatherers += Biodegradation(waves=waves)
#model.weatherers += Dissolution(waves,w_obj)


#%% DATOS DEL DERRAME

#substance=gs.GnomeOil(filename='/home/gaby.resendiz/maya-oil-and-gas_AD01906.json')


spill= gs.surface_point_line_spill(num_elements=1000, start_position=(lon,lat,0), release_time=start_time, end_release_time= start_time + gs.days(duracion_derrame), amount=10000, substance=gs.GnomeOil(filename='/home/gaby.resendiz/maya-2004_EC00643.json'), units='bbls', name='My Spill')
                                      

model.spills += spill



#%%para guardarlo Clúster


salida1='/home/gaby.resendiz/' + nombre + '_' + str(year)

cond=os.path.isdir(salida1)

if cond==True:
  print('El directorio ya existe, se va a sobreescribir')
  
else:
  os.mkdir('/home/gaby.resendiz/' + nombre + '_' + str(year))
  print('Nuevo directorio creado')
        
        
os.chdir(salida1)

#renderer = gs.Renderer(output_dir=salida1,
                       #map_filename=('/home/gaby.resendiz/costa/Costa_Conabio.bna'),
                       #output_timestep=gs.hours(1))
                       
#model.outputters += renderer

#Esta salida genera un shape para que pueda cargarse en un zip
shape_file = os.path.join(salida1 + '/'+ nombre + '_' + str(year) +'shape')

model.outputters += gs.ShapeOutput(shape_file,
                                zip_output=True,surface_conc='kde',
                                output_timestep=gs.hours(24))


##Esta salida genera un netcdf
#model.outputters += renderer

netcdf_file = os.path.join(salida1 + '/'+ nombre + '_' + str(year) + '.nc')
                           
gs.remove_netcdf(netcdf_file)
model.outputters += NetCDFOutput(netcdf_file,
                                     which_data='most',
                                     # output most of the data associated with the elements
                                     output_timestep=timedelta(hours=24))

model.outputters += gs.OilBudgetOutput()
model.outputters += gs.WeatheringOutput(os.path.join(salida1, 'WeatheringOutput'))


#%%Para correr el modelo
model.full_run()


##reanalisis wrf

#files_wrf=glob.glob('/home/gaby.resendiz/RESPALDO_V4/a'+str(year)+'/salidas/wrfout_c1h_d01_'+str(year)+'-'+mes+'*')
#files_wrf.sort()