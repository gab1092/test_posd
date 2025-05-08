#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Jan 15 2025

@author: Gabriela Reséndiz-Colorado
"""

##Código para calcular la probabilidad por día de afectación de un hexágono.

 #%%

import geopandas as gpd
import pandas as pd
import os
from pyogrio import read_dataframe
import glob
import numpy as np
import fiona

#
temporadas=['invierno','primavera','verano','otonio']
#contador=0
#totales=[2136,2208,2418,2225] ##revisar conteo otonio##

for temporada in temporadas:
    
    lista=glob.glob("Concentraciones_30mil/*"+ temporada +"*")
    columnas=np.arange(1,91)
    
    for name in lista:
       
        datos=read_dataframe(name)
        
        for cont in columnas:
            
            columna='Conc_'+str(cont)

            
            datos[columna]=datos[columna]/(datos['Contador']/90)
            

            columna2='Prob001_'+str(cont)
            #Prob001_
            datos[columna2]=(datos[columna2]/(datos['Contador']/90))


            columna3='Prob10_'+str(cont)
            #Prob10_90
            datos[columna3]=(datos[columna3]/(datos['Contador']/90))
            
            
        nombre=os.path.basename(name)
        nombre=nombre[8:]
        #ruta 30 mil: Conc_prob_promedio30mil
        #ruta 10 mil: Concentraciones_30mil
        nombre2="/home/gaby.resendiz/Conc_prob_promedio30mil/Prom_conc_"+nombre
        datos.to_file(filename=nombre2,driver='ESRI Shapefile')
        datos=[]
            
   # contador=contador+1