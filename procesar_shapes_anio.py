
import glob
import geopandas as gpd
import pandas as pd
import os
from datetime import datetime, timedelta
import numpy as np
import time

os.chdir('salidas_temporales')

temporadas=['invierno','primavera','verano','otonio']
pozos=["TEEKIT-45","CAMATL-4","HOKCHI-9","AYATSIL-285","BALAM-3","ARENQUE-18","ARENQUE-41"]


ID_SLURM=os.getenv('SLURM_ARRAY_TASK_ID')

anios=np.arange(1993,2020)

ind=int(ID_SLURM)

year=anios[ind]

print(str(year))

primavera=[datetime(year,3,20),datetime(year,6,20)]

verano=[datetime(year,6,21),datetime(year,9,22)]

otonio=[datetime(year,9,23),datetime(year,12,20)]

year2=year+1

invierno=[datetime(year,12,21),datetime(year2,3,19)]


for pozo in pozos:
    
    for temporada in temporadas:
        
        print('La temporada es: ' + temporada)
    
        file_i=[]
        files_pozo=[]
        file_i=[]
        
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
            
        while fecha != fechaf:
            
            print(fecha)
            mes=fecha.month
            dia=fecha.day
            year3=fecha.year
            file=glob.glob('/LUSTRE/CIGOM/DERRAMES_2024_pygnome/'+pozo+'/*_'+str(year3)+'_'+str(mes)+'_'+str(dia)+'.zip*')
            files_pozo=file_i+file
            file_i=files_pozo
            fecha=fecha+timedelta(days=1)
        files_pozo.sort()
        print(files_pozo)
        
        
        for file in files_pozo:
            
            if file==files_pozo[0]:
                file_base=gpd.read_file(file)
            
            else:
                file_sh=gpd.read_file(file)
                shape_new=pd.concat([file_base,file_sh])
                file_base=shape_new
                print('Sumando archivo')
                
        filename=pozo + str(year) + '_' + temporada + ".shp.zip"
        shape_new.to_file(filename,driver='ESRI Shapefile')
        print('Guarde un shape, revisalo')
    #time.sleep(5*60) 
