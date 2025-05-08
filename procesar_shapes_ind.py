import glob
import geopandas as gpd
import pandas as pd
import os
from datetime import datetime, timedelta
import numpy as np
from os import system

temporadas=['primavera','verano','otonio','invierno']
pozos=["ARENQUE-18","ARENQUE-41","TEEKIT-45","CAMATL-4","HOKCHI-9","AYATSIL-285","BALAM-3"]

p_t=[["ARENQUE-18",'primavera'],["ARENQUE-18",'verano'],["ARENQUE-18",'otonio'],["ARENQUE-18",'invierno'],
     ["ARENQUE-41",'primavera'],["ARENQUE-41",'verano'],["ARENQUE-41",'otonio'],["ARENQUE-41",'invierno'],
      ["TEEKIT-45",'primavera'],["TEEKIT-45",'verano'],["TEEKIT-45",'otonio'],["TEEKIT-45",'invierno'],
      ["CAMATL-4",'primavera'],["CAMATL-4",'verano'],["CAMATL-4",'otonio'],["CAMATL-4",'invierno'],
      ["HOKCHI-9",'primavera'],["HOKCHI-9",'verano'],["HOKCHI-9",'otonio'],["HOKCHI-9",'invierno'],
      ["AYATSIL-285",'primavera'],["AYATSIL-285",'verano'],["AYATSIL-285",'otonio'],["AYATSIL-285",'invierno'],
      ["BALAM-3",'primavera'],["BALAM-3",'verano'],["BALAM-3",'otonio'],["BALAM-3",'invierno']]


lista_id=np.arange(0,28)


primavera=[datetime(2000,3,21),datetime(2000,6,20)]

verano=[datetime(2000,6,21),datetime(2000,9,22)]

otonio=[datetime(2000,9,23),datetime(2000,12,20)]

invierno=[datetime(2000,12,21),datetime(2001,3,20)]

#file_i=[]
 #   files_pozo=[]

for contador in lista_id:
    
    file_i=[]
    
    pozo=p_t[contador][0]
    temporada=p_t[contador][1]

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
        file=glob.glob('/LUSTRE/CIGOM/DERRAMES_2024_pygnome/'+pozo+'/*_'+str(mes)+'_'+str(dia)+'.zip*')
        files_pozo=file_i+file
        file_i=files_pozo
        fecha=fecha+timedelta(days=1)
        files_pozo.sort()
    
    for file in files_pozo:
        system("clear")

        if file==files_pozo[0]:
            file_base=gpd.read_file(file)
        else:
            file_sh=gpd.read_file(file)
            shape_new=pd.concat([file_base,file_sh])
            file_base=shape_new
            filename=pozo + "_"+ temporada + ".shp.zip"
            print('Estoy sumando un shape')
            
    os.chdir('salidas_temporadas')
    shape_new.to_file(filename)
    print('Guarde el archivo' + shape_new)
