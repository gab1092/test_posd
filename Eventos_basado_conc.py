import glob
import geopandas as gpd
import pandas as pd
import os
from datetime import datetime, timedelta
import numpy as np
import time
from pyogrio import read_dataframe


os.chdir('/home/gaby.resendiz/Concentraciones_30mil')  #carpeta para guardar los conteos para probabilidad y concentraciones


#'invierno','primavera','verano',

temporadas=['otonio','invierno','primavera','verano']

pozos=["AYATSIL-285","ARENQUE-18","TEEKIT-45","BALAM-3","ARENQUE-41","CAMATL-4","HOKCHI-9"]
##para mandar 1-7, uno para cada pozo
ID_SLURM=os.getenv('SLURM_ARRAY_TASK_ID') 

#ID_SLURM=1

anios=np.arange(1994,2020)

ind=int(ID_SLURM)

pozo=pozos[ind-1]
dias_segundos=np.arange(1,91)

fc=1000/256000000

for temporada in temporadas:

    oceano_costa=read_dataframe("/home/gaby.resendiz/Sensibilidad_regiones/Sensibilidad_region.shp")
    oceano_costa2=read_dataframe("/home/gaby.resendiz/Sensibilidad_regiones/Sensibilidad_region.shp")
    oceano_costa3=read_dataframe("/home/gaby.resendiz/Sensibilidad_regiones/Sensibilidad_region.shp")
    oceano_costa2['Contador']=0
    
    #print('La temporada es: ' + temporada)
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
        
        
        while fecha2 != fechaf:
            
            mes=fecha2.month
            dia=fecha2.day
            year3=fecha2.year
            #ruta salidas de las simulaciones de derrame
            #30 mil bls diarios /LUSTRE/CIGOM/DERRAMES_2024_pygnome/salidas30mil_90dias/
            #10 mil bls diarios /LUSTRE/CIGOM/DERRAMES_2024_pygnome/salidas2_90dias
            
            files=glob.glob('/LUSTRE/CIGOM/DERRAMES_2024_pygnome/salidas30mil_90dias/'+pozo+'/*_'+str(year3)+'_'+str(mes)+'_'+str(dia)+'.zip*')
            #files=glob.glob('/LUSTRE/CIGOM/DERRAMES_2024_pygnome/'+pozo+'/*_'+str(year3)+'_'+str(mes)+'_'+str(dia)+'.zip*')
            
            #print(files)
                
            if len(files)>0:
                    
                file_base=read_dataframe(files[0],columns=['Time','geometry','LE_id','Mass'])
                tiempo=datetime.strptime(np.min(file_base['Time']),'%Y-%m-%dT%H:%M:%S')
                tiempo=tiempo-timedelta(days=1)
                file_base=file_base.drop_duplicates(subset=['LE_id','geometry'])
                
                    
                for i in dias_segundos:
                  
                    col_name='Conc_' + str(i)
                    col_name2='Prob001_' + str(i)
                    col_name3='Prob10_' + str(i)
                        
                    if fecha2==fecha and year==1994:
                            
                        time=tiempo+timedelta(days=int(i))
                        #-timedelta(hours=6)
                        t2=datetime.strftime(time,'%Y-%m-%dT%H:%M:%S')
                        
                        Aux=file_base[file_base['Time']==t2].overlay(oceano_costa, how = 'intersection')
                        
                        Aux_masst = Aux.groupby('GRID_ID').sum('Mass')
                        Aux_masst[col_name]=(Aux_masst['Mass'].mul(fc)) ###Se convierte a concentración Masa (Kg)*1000 para pasar a gramos entre el área (m2) del hexagono
                        
                        Aux_masst.loc[(Aux_masst[col_name]>=0.01,[col_name2])]=1
                        Aux_masst.loc[(Aux_masst[col_name]<0.01,[col_name2])]=0
                    
        
                        oceano_costa2[col_name2] = oceano_costa2['GRID_ID'].map(Aux_masst[col_name2])
                        oceano_costa2[col_name2] = oceano_costa2[col_name2].fillna(0)

                        #oceano_costa2[col_name]= oceano_costa2['GRID_ID'].map(Aux_masst[col_name])

                        oceano_costa2[col_name]= oceano_costa2['GRID_ID'].map(Aux_masst[col_name])
                        oceano_costa2[col_name] = oceano_costa2[col_name].fillna(0)

                            
                        Aux_masst.loc[(Aux_masst[col_name]>=10,[col_name3])]=1
                        Aux_masst.loc[(Aux_masst[col_name]<10,[col_name3])]=0
                    
        
                        oceano_costa2[col_name3] = oceano_costa2['GRID_ID'].map(Aux_masst[col_name3])
                        oceano_costa2[col_name3] = oceano_costa2[col_name3].fillna(0)
                        
                        
                        oceano_costa2['Contador']=oceano_costa2['Contador']+1
        
                        #Aux_masst=[]
                       # Aux=[]
                            
                    else:
        
                        time=tiempo+timedelta(days=int(i))
                        t2=datetime.strftime(time,'%Y-%m-%dT%H:%M:%S')

                        particulas_conteo = Aux.groupby('GRID_ID').size()

                        Aux=file_base[file_base['Time']==t2].overlay(oceano_costa, how = 'intersection')
        
                        Aux_masst = Aux.groupby('GRID_ID').sum('Mass') ##revisar esto si esta funcionanado
                        Aux_masst[col_name]=(Aux_masst['Mass'].mul(fc))
                        
                        Aux_masst.loc[(Aux_masst[col_name]>=0.1,[col_name2])]=1
                        Aux_masst.loc[(Aux_masst[col_name]<0.1,[col_name2])]=0
                     
                        ##Conteo de eventos mayores a 0.1 para calcular el porcentaje después
                        oceano_costa3[col_name2] = oceano_costa3['GRID_ID'].map(Aux_masst[col_name2])
                        oceano_costa3[col_name2] = oceano_costa3[col_name2].fillna(0)
                        ##Concentraciones en g/m2
                        oceano_costa3[col_name]= oceano_costa3['GRID_ID'].map(Aux_masst[col_name])
                        oceano_costa3[col_name] = oceano_costa3[col_name].fillna(0)

                        Aux_masst.loc[(Aux_masst[col_name]>=10,[col_name3])]=1
                        Aux_masst.loc[(Aux_masst[col_name]<10,[col_name3])]=0
                    
        
                        oceano_costa3[col_name3] = oceano_costa3['GRID_ID'].map(Aux_masst[col_name3])
                        oceano_costa3[col_name3] = oceano_costa3[col_name3].fillna(0)
        
                        oceano_costa2[col_name3] = oceano_costa2[col_name3]+oceano_costa3[col_name3]
                        oceano_costa2[col_name2] = oceano_costa2[col_name2]+oceano_costa3[col_name2]
                        oceano_costa2[col_name] = oceano_costa2[col_name]+oceano_costa3[col_name]      ##concentracion (suma)                    
                        #oceano_costa2[col_name] = oceano_costa2[col_name].fillna(0)
                        oceano_costa2['Contador']=oceano_costa2['Contador']+1
                           

            fecha2=fecha2+timedelta(days=1)

    #columnas=np.arange(1,91)
    
    #for cont in columnas:
     #   columna='Prob_'+str(cont)
      #  col_name='Conc_' + str(cont)
       # oceano_costa2[col_name] = oceano_costa2[col_name]/np.max(oceano_costa2[columna])
        #oceano_costa2[columna]=((oceano_costa2[columna]/np.max(oceano_costa2[columna]))*100)

    ###guarda el archivo con todos los datos procesados, de toda la temporada de todos los años                         
    filename='Eventos_'+ pozo + '_' + temporada + ".shp.zip"
    oceano_costa2.to_file(filename,driver='ESRI Shapefile')
