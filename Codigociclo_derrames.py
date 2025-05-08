#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 10:46:03 2022

@author: Gabriela Reséndiz-Colorado
"""

##Código para correr la simulación de derrame con PyGnome considerando biodegradación, emulsificación, 
##dispersión natural y evaporación

 #%%


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

from os import system

duracion_derrame=30

duracion_sim=30

long=[-97.518074,-97.50473532,-93.0705731,-94.08910464,-93.35649955,-92.35024839,-91.9696528]
lati=[22.280349,22.23440974,18.61385211,18.30407584,18.63056913,19.66731777,19.5071589]

nombres=["ARENQUE-18","ARENQUE-41","TEEKIT-45","CAMATL-4","HOKCHI-9","AYATSIL-285","BALAM-3"]

years=range(1994,2020)

meses=range(1,13)

dia='01'


for year in years:
    
    files_hycom=glob.glob('/home/gaby.resendiz/HYCOM_REPROCESADO/'+'*archv.'+str(year)+'*')
    files_hycom.sort()
    df=nc4.MFDataset(files_hycom,aggdim='time')
   
    files_wrf=glob.glob('/home/gaby.resendiz/WRF_REANALISIS_PROC/wrfout_c1h_d01_'+str(year)+'*')
    files_wrf.sort()
    dw=nc4.MFDataset(files_wrf,aggdim='time')
    
    for mes in meses:

        if mes==12:
            
            
            year2=int(year)+1
            
            files_hycom1=glob.glob('/home/gaby.resendiz/HYCOM_REPROCESADO/'+'*archv.'+str(year)+'*')
            files_hycom2=glob.glob('/home/gaby.resendiz/HYCOM_REPROCESADO/'+'*archv.'+str(year2)+'*')
            files_hycom1.sort()
            files_hycom2.sort()
            files_hycom3=files_hycom1+files_hycom2
            df=nc4.MFDataset(files_hycom3,aggdim='time')
            
            files_wrf1=glob.glob('/home/gaby.resendiz/WRF_REANALISIS_PROC/wrfout_c1h_d01_'+str(year)+'*')
            files_wrf1.sort()
            files_wrf2=glob.glob('/home/gaby.resendiz/WRF_REANALISIS_PROC/wrfout_c1h_d01_'+str(year2)+'*')
            files_wrf2.sort()
            files_wrf3=files_wrf1+files_wrf2
            dw=nc4.MFDataset(files_wrf1,files_wrf2,aggdim='time')
            


            
        
        for nombre in nombres:
            if nombre=="BALAM-3":
                system("clear")
                lon=long[6]
                lat=lati[6]
            
           # if nombre=='AYATSIL-285':

              #  system("clear")
             #   lon=long[5]
             #   lat=lati[5]
            
            #if nombre=="ARENQUE-18":

              #  system("clear")
                
            #    lon=long[0]
            #    
             #   lat=lati[0]
                           
            
                    
                    
                
                
                nombre_file=nombre+'_'+str(year)+'_'+'{:0>2}'.format(mes)
                
                start_time = datetime(year, int(mes), int(dia), 18, 0) #Hora UTC
                
                ##cargando el archivo de costa 
                mymap = gs.MapFromBNA('/home/gaby.resendiz/costa/Costa_Conabio.bna', refloat_halflife=1)
                ##cargando al modelo archivo de costa , viento etc
                model = gs.Model(start_time=start_time, duration=timedelta(days=duracion_sim), time_step=gs.minutes(60),map=mymap)
                
                #cargando HYCOM-IOA

                c_mover=gs.CurrentMover.from_netCDF(df)
                model.movers += c_mover
                #+'-''{:0>2}'.format(mes)

                random_mover = gs.RandomMover(diffusion_coef=1e5)

                w_mover = gs.WindMover.from_netCDF(dw)
                model.movers += w_mover
                w_obj = gs.GridWind.from_netCDF(dw)
                water = Water(temperature=300.0, salinity=35.0) #temperature in Kelvin, salinity in psu
                waves = Waves(wind=w_obj,water=water)
                model.environment += waves
                model.weatherers += Evaporation(wind=w_obj,water=water)
                model.weatherers += NaturalDispersion()
                release=gs.PointLineRelease(num_elements=1000,release_time=start_time,start_position=(lon,lat,0),end_release_time= start_time + gs.days(duracion_derrame))
                substance=gs.GnomeOil(filename='/home/gaby.resendiz/isthmus-maya-blend_AD00579.json') 
                spill = gs.Spill(release=release,amount=5000,units='bbls',substance=substance)
                model.spills += spill

                
                 
                 
                 #%%para guardarlo Clúster
                 
                salida1='/home/gaby.resendiz/Salidas/' + nombre_file
                     
                cond=os.path.isdir(salida1)
                 
                if cond==True:
                    print('El directorio ya existe, se va a sobreescribir')
                else:
                     
                    os.mkdir('/home/gaby.resendiz/Salidas/' + nombre_file)
                    print('Nuevo directorio creado')
                    
                os.chdir(salida1)

                shape_file = os.path.join(salida1 + '/'+ nombre + '_' + str(year)+'_'+str(mes))
                          
                model.outputters += gs.ShapeOutput(shape_file,
                                zip_output=True,surface_conc='kde',
                                output_timestep=gs.hours(12))
               
                netcdf_file = os.path.join(salida1 + '/'+ nombre + '_' + str(year) + '.nc')
                gs.remove_netcdf(netcdf_file)
                
                model.outputters += NetCDFOutput(netcdf_file,
                                     which_data='most',
                                     # output most of the data associated with the elements
                                     output_timestep=timedelta(hours=24))
                           
                model.outputters += gs.OilBudgetOutput()
                #model.outputters += gs.WeatheringOutput(os.path.join(salida1, 'WeatheringOutput'))
                
                #%%Para correr el modelo
                model.full_run()


                




                