import glob
import geopandas as gpd
import pandas as pd
import os
from datetime import datetime, timedelta
import numpy as np
import time
from pyogrio import read_dataframe



os.chdir('Salidas_conteos_c6horas')

#"TEEKIT-45",
temporadas=['invierno','primavera','verano','otonio']
pozos=["AYATSIL-285","BALAM-3","ARENQUE-18","ARENQUE-41","CAMATL-4","HOKCHI-9"]
##para mandar 1-7, uno para cada pozo
ID_SLURM=os.getenv('SLURM_ARRAY_TASK_ID') 

#ID_SLURM=1

anios=np.arange(1994,2020)

ind=int(ID_SLURM)

pozo=pozos[ind-1]
#dias_segundos=np.arange(1,31)
dias_segundos=np.arange(1,120)

for temporada in temporadas:

    oceano_costa=read_dataframe('../costayoceano/OceanoyCosta.shp')
    oceano_costa2=read_dataframe('../costayoceano/OceanoyCosta.shp')
    
    print('La temporada es: ' + temporada)
    file_i=[]
    files_pozo=[]
    file_i=[]
    
    for year in anios:
        
        
        primavera=[datetime(year,3,20),datetime(year,6,20)]
        verano=[datetime(year,6,21),datetime(year,9,22)]
        otonio=[datetime(year,9,23),datetime(year,12,20)]
        year2=year+1
        invierno=[datetime(year,12,21),datetime(year2,3,19)]
        
        if temporada=='primavera':
            
            fecha=primavera[0]
            fechaf=primavera[1]
            
        if temporada=='verano':
            
            fecha=verano[0]
            fechaf=verano[1]
            
        if temporada=='otonio':
            
            fecha=otonio[0]
            fechaf=otonio[1]
            
        if temporada=='invierno':
            
            
            fecha=invierno[0]
            fechaf=invierno[1]
            
        fecha2=fecha
        print(fecha2)
        
        while fecha2 != fechaf:
            
            mes=fecha2.month
            dia=fecha2.day
            year3=fecha2.year
            files=glob.glob('/LUSTRE/CIGOM/DERRAMES_2024_pygnome/salidas_3/'+pozo+'/*_'+str(year3)+'_'+str(mes)+'_'+str(dia)+'.zip*')
            #files=glob.glob('/LUSTRE/CIGOM/DERRAMES_2024_pygnome/'+pozo+'/*_'+str(year3)+'_'+str(mes)+'_'+str(dia)+'.zip*')
           
            #print(files)
                
            if len(files)>0:
                    
                file_base=read_dataframe(files[0],columns=['Time','lon','lat'])
                tiempo=datetime.strptime(np.min(file_base['Time']),'%Y-%m-%dT%H:%M:%S')
               
                    
                for i in dias_segundos:
                    
                    col_name='Conteo_' + str(i)
                        
                    if fecha2==fecha and year==1994:
                            
                        time=tiempo+timedelta(hours=6)
                        t2=datetime.strftime(time,'%Y-%m-%dT%H:%M:%S')
                        Aux=file_base[file_base['Time']==t2].overlay(oceano_costa, how = 'intersection')
                        particulas_conteo = Aux.groupby('GRID_ID').size()
                        oceano_costa2[col_name] = oceano_costa2['GRID_ID'].map(particulas_conteo)
                        oceano_costa2[col_name] = oceano_costa2[col_name].fillna(0)
                        particulas_conteo=[]
                        Aux=[]
                        tiempo=time
                            
                    else:
                        time=tiempo+timedelta(hours=6)
                        t2=datetime.strftime(time,'%Y-%m-%dT%H:%M:%S')
                        Aux=file_base[file_base['Time']==t2].overlay(oceano_costa, how = 'intersection')
                        particulas_conteo = Aux.groupby('GRID_ID').size()
                        oceano_costa2[col_name] = oceano_costa2['GRID_ID'].map(particulas_conteo)+oceano_costa2[col_name]
                        oceano_costa2[col_name] = oceano_costa2[col_name].fillna(0)
                        particulas_conteo=[]
                        Aux=[]
                        tiempo=time
            fecha2=fecha2+timedelta(days=1)                        

                              
    filename='Conteo_'+ pozo + '_' + temporada + ".shp.zip"
    oceano_costa2.to_file(filename,driver='ESRI Shapefile')
    print('Guarde el shape ' + filename + 'revisalo')
