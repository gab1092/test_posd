import glob
import geopandas as gpd
import pandas as pd
import os
from datetime import datetime, timedelta



temporadas=['primavera','verano','otonio','invierno']
pozos=["ARENQUE-18","ARENQUE-41","TEEKIT-45","CAMATL-4","HOKCHI-9","AYATSIL-285","BALAM-3"]


ID_SLURM=os.getenv('SLURM_ARRAY_TASK_ID')

contador=int(ID_SLURM)-1

primavera=datetime(2000,3,20)

verano=datetime(2000,6,21)

otonio=datetime(2000,9,23)

invierno=datetime(2000,12,21)


pozo='ARENQUE-18'

for temporada in temporadas:

     if temporada=='primavera':
        
        ndias2=int(ID_SLURM)*92
        ndias1=contador*92
        
        if contador >=1:
           ndias1=(contador*92)+1
           
        fecha=primavera+timedelta(days=ndias1)
        fechaf=fecha+timedelta(days=int(ndias2))
        
        print(temporada)
        print(str(fecha))
        print(str(fechaf))
        
     if temporada=='verano':
        
        ndias2=int(ID_SLURM)*93
        ndias1=contador*93
        
        if contador >=1:
           ndias1=(contador*93)+1
           
        fecha=verano+timedelta(days=ndias1)
        fechaf=fecha+timedelta(days=int(ndias2))
        print(temporada)
        print(str(fecha))
        print(str(fechaf))
        
        
     if temporada=='otonio':
       
        ndias2=int(ID_SLURM)*85
        ndias1=contador*85
        
        if contador >=1:
           ndias1=(contador*85)+1
           
        fecha=otonio+timedelta(days=ndias1)
        fechaf=fecha+timedelta(days=int(ndias2))
        print(temporada)
        print(str(fecha))
        print(str(fechaf))
             
     if temporada=='invierno':
        ndias2=int(ID_SLURM)*87
        ndias1=contador*87
        
        if contador >=1:
           ndias1=(contador*87)+1
           
        fecha=invierno+timedelta(days=ndias1)
        fechaf=fecha+timedelta(days=int(ndias2))
        print(temporada)
        print(str(fecha))
        print(str(fechaf))
     
     
     file_pozo=[]
     file_i=[]
     
     while fecha != fechaf:
        print(fecha)
        mes=fecha.month
        dia=fecha.day
        file=glob.glob('/LUSTRE/CIGOM/DERRAMES_2024_pygnome/'+pozo+'/*_'+str(mes)+'_'+str(dia)+'.zip*')
        files_pozo=file_i+file
        file_i=files_pozo
        fecha=fecha+timedelta(days=1)
        files_pozo.sort()
        
     for file in files_pozo:
         if file==files_pozo[0]:
            file_base=gpd.read_file(file)
         else:
            file_sh=gpd.read_file(file)
            shape_new=pd.concat([file_base,file_sh])
            file_base=shape_new
            
            
     filename=pozo + "_"+ temporada +"_"+ID_SLURM+ ".shp.zip"
     os.chdir('salidas_temporales')
     shape_new.to_file(filename)