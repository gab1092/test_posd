#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sep 10 2024
Modificado Octubre 

@author: Gabriela Reséndiz-Colorado
"""

##Código para correr la simulación de derrame con PyGnome considerando biodegradación, emulsificación, 
##dispersión natural y evaporación, paralelizada en el clúster ometeotl ICAyCC-IOA

 #%%

import os
import sys

from datetime import datetime, timedelta

import gnome.scripting as gs

from gnome.outputters import NetCDFOutput, ShapeOutput

from gnome.weatherers import Evaporation, NaturalDispersion, Emulsification, Biodegradation, Dissolution

from gnome.environment import Water, Waves

from gnome.movers import RandomMover3D, RiseVelocityMover

import numpy as np

import glob

import netCDF4 as nc4

from os import system

duracion_derrame=90

duracion_sim=90

long=[-97.518074,-97.50473532,-93.0705731,-94.08910464,-93.35649955,-92.35024839,-91.9696528]
lati=[22.280349,22.23440974,18.61385211,18.30407584,18.63056913,19.66731777,19.5071589]


fecha_base=datetime(1993,12,31,18) #Hora UT

#dia=os.getenv('SLURM_ARRAY_TASK_ID')

dia=os.getenv('NUM_ARRAY')
#dia=sys.argv[1]
#print('El num_array es:' + str(dia))

start_time=fecha_base + timedelta(int(dia))
#print('fecha de modelacion ' + str(start_time))
#print('Array ID'+ str(dia))

year=start_time.year
mes=start_time.month
print(mes)
print(str(start_time))


if mes<10:

    
    files_hycom=glob.glob('/home/gaby.resendiz/HYCOM_REPROCESADO_0/'+'*archv.'+str(year)+'*')
    files_hycom.sort()
    df=nc4.MFDataset(files_hycom,aggdim='time')
    
    files_wrf=glob.glob('/home/gaby.resendiz/WRF_REANALISIS_PROC/wrfout_c1h_d01_'+str(year)+'*')
    files_wrf.sort()
    dw=nc4.MFDataset(files_wrf,aggdim='time')

 
if mes==10 or mes==11 or mes==12:

    
    year2=year+1
    print(year)

        
    files_hycom1=glob.glob('/home/gaby.resendiz/HYCOM_REPROCESADO_0/'+'*archv.'+str(year)+'*')
    files_hycom2=glob.glob('/home/gaby.resendiz/HYCOM_REPROCESADO_0/'+'*archv.'+str(year2)+'*')
    files_hycom1.sort()
    files_hycom2.sort()
    files_hycom3=files_hycom1+files_hycom2
    df=nc4.MFDataset(files_hycom3,aggdim='time')
    
    files_wrf1=glob.glob('/home/gaby.resendiz/WRF_REANALISIS_PROC/wrfout_c1h_d01_*'+str(year)+'*')
    files_wrf1.sort()
    files_wrf2=glob.glob('/home/gaby.resendiz/WRF_REANALISIS_PROC/wrfout_c1h_d01_*'+str(year2)+'*')
    files_wrf2.sort()
    files_wrf3=files_wrf1+files_wrf2
    dw=nc4.MFDataset(files_wrf3,aggdim='time')

    if year==2018:
        files_wrf3=files_wrf3[0:729]
        dw=nc4.MFDataset(files_wrf3,aggdim='time')
        
    if year==2019:
        print(year)
        dw=nc4.MFDataset(files_wrf1[0:365],aggdim='time')
        
        
        
    
nombres=["TEEKIT-45","ARENQUE-18","ARENQUE-41","CAMATL-4","HOKCHI-9","AYATSIL-285","BALAM-3"]
#nombres=['BALAM-3']

for nombre in nombres:
    if nombre=="ARENQUE-18":
        lon=long[0]
        lat=lati[0]
        #print('Pozo simulando:' + nombre)
    if nombre=="ARENQUE-41":
        lon=long[1]
        lat=lati[1]
        #print('Pozo simulando:' + nombre)
    if nombre=='TEEKIT-45':
        lon=long[2]
        lat=lati[2]
       # print('Pozo simulando:' + nombre)
    if nombre=='CAMATL-4':
        lon=long[3]
        lat=lati[3]
       # print('Pozo simulando:' + nombre)
            
    if nombre=='HOKCHI-9':
        lon=long[4]
        lat=lati[4]
       # print('Pozo simulando:' + nombre)
                
    if nombre=='AYATSIL-285':
        lon=long[5]
        lat=lati[5]
       # print('Pozo simulando:' + nombre)
    if nombre=="BALAM-3":
        lon=long[6]
        lat=lati[6]
       # print('Pozo simulando:' + nombre)
                
    mymap = gs.MapFromBNA('/home/gaby.resendiz/costa/Costa_Conabio.bna', refloat_halflife=-1)
            ##cargando al modelo archivo de costa , viento etc
    model = gs.Model(start_time=start_time, duration=timedelta(days=duracion_sim), time_step=gs.minutes(60),map=mymap)
                #cargando HYCOM-IOA
    c_mover=gs.CurrentMover.from_netCDF(df)
    model.movers += c_mover
                #+'-''{:0>2}'.format(mes)
    random_mover = gs.RandomMover(diffusion_coef=2e4)
    model.movers += random_mover
    #pygnome IOA 2e4 ##10 mil bls se corrió con 10e5, probando con 2e4
    w_mover = gs.WindMover.from_netCDF(dw)
    model.movers += w_mover
    w_obj = gs.GridWind.from_netCDF(dw)
    water = Water(temperature=300.0, salinity=36) #temperature in Kelvin, salinity in psu
    waves = Waves(wind=w_obj,water=water)
    model.environment += waves
    model.weatherers += Evaporation(wind=w_obj,water=water)
    model.weatherers += NaturalDispersion()  
    release=gs.PointLineRelease(num_elements=9000,release_time=start_time,start_position=(lon,lat,0),end_release_time=start_time+gs.days(duracion_derrame))
    substance=gs.GnomeOil(filename='/home/gaby.resendiz/isthmus-maya-blend_AD00579.json') 
    spill = gs.Spill(release=release,amount=2700000,units='bbls',substance=substance)
    #900000 salidas_2
    #900000 salidas_2 
    model.spills += spill
                #%%para guardarlo Clúster
    dia1=start_time.day 
    
    salida1='/LUSTRE/CIGOM/DERRAMES_2024_pygnome/salidas30mil_90dias/' + nombre
    ##
    cond=os.path.isdir(salida1)
                
    if cond==True:
        nombre
        
        #print('El directorio ya existe, no se hace nada ')
        
    if cond==False:
        os.mkdir('/LUSTRE/CIGOM/DERRAMES_2024_pygnome/salidas30mil_90dias/' + nombre)
       # print('Nuevo directorio creado')
       ## salidas30mil_90dias
           
    shape_file = os.path.join(salida1 + '/'+ nombre + '_' + str(year) + '_' +str(mes)+ '_' + str(dia1))
                          
    model.outputters += gs.ShapeOutput(shape_file,zip_output=True,output_timestep=gs.hours(24))
                #%%Para correr el modelo
    model.full_run()

#Salidas cortas hacerlas cada 6 horas, largas cada 12.
               
    #netcdf_file = os.path.join(salida1 + '/'+ nombre + '_' + str(year) + '_' +str(mes)+ '_' + str(dia1) + '.nc')
    
    #gs.remove_netcdf(netcdf_file)
    
    
   # model.outputters += NetCDFOutput(netcdf_file,which_data='most',output_timestep=timedelta(hours=3))
    

 

                




                
