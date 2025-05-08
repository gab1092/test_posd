import glob
import geopandas as gpd
import pandas as pd
import os
from datetime import datetime, timedelta
import numpy as np
from pyogrio import read_dataframe


#oceano_costa=gpd.read_file('costayoceano/OceanoyCosta.shp')

oceano_costa=read_dataframe('costayoceano/OceanoyCosta.shp')

temporadas=['primavera','verano','otonio','invierno']
pozos=["TEEKIT-45","CAMATL-4","HOKCHI-9","AYATSIL-285","BALAM-3","ARENQUE-18","ARENQUE-41"]


anios=np.arange(1994,2020)
dias_segundos=np.arange(1,31)


for temporada in temporadas:
  
    for pozo in pozos:

        oceano_costa=read_dataframe('costayoceano/OceanoyCosta.shp')
              
        for year in anios:
            
            print('La temporada es: ' + temporada +' el anio es: ' + str (year))            
            
            files=glob.glob('salidas_temporales/' + pozo  + str(year) + '_'+ temporada + '.shp.zip*')
            
            if len(files)>0:
                
                file_base=read_dataframe(files[0],columns=['Time','lon','lat'])

            
                for i in dias_segundos:
                    ii=i-1
                    col_name='Conteo_' + str(i)
                    
                    if year==anios[0]:
                        time=(86400*dias_segundos[ii])
                        Aux=file_base[file_base['Age']<=time].overlay(oceano_costa, how = 'intersection')
                        particulas_conteo = Aux.groupby('GRID_ID').size()
                        oceano_costa[col_name] = oceano_costa['GRID_ID'].map(particulas_conteo)
                        oceano_costa[col_name] = oceano_costa[col_name].fillna(0)
                        Aux=[]
                    else: 
                        time=(86400*dias_segundos[ii])
                        Aux=file_base[file_base['Age']<=time].overlay(oceano_costa, how = 'intersection')
                        particulas_conteo = Aux.groupby('GRID_ID').size()
                        oceano_costa[col_name] = oceano_costa['GRID_ID'].map(particulas_conteo)+oceano_costa[col_name]
                        oceano_costa[col_name] = oceano_costa[col_name].fillna(0)
                        Aux=[]
            
        rutag='Salidas_conteos_temporadas'                            
        filename=rutag + '/' +'Conteo_'+ pozo + '_' + temporada + ".shp.zip"
        oceano_costa.to_file(filename,driver='ESRI Shapefile')
        print('Guarde el shape ' + filename + 'revisalo')
        


