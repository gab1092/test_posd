import geopandas as gpd
import pandas as pd
import os
from pyogrio import read_dataframe
import glob
import numpy as np
import fiona

ndias=30

lista=glob.glob("/home/gaby.resendiz/Conc_prob_promedio30mil/*zip*")
#lista=glob.glob("/home/gaby.resendiz/Conc_prob_promedio/*zip*")
columnas=np.arange(1,91)
columnas2=np.arange(ndias+1,91)
columnas3=np.arange(1,ndias+1)




#df.loc[row_indexer, "col"] = values

for name in lista:
    
                 datos=read_dataframe(name)
                 datos2=datos.drop(columns=['Id','GRID_ID','X','Y','GRID_ID_1','geometry','Area_km','Región'])
                 #datos2["Indexes"]= datos2["xtupla"].str.find('cFish')
                 datos3=read_dataframe(name)
                 datos3=datos3.drop(columns= ['Id','GRID_ID','X','Y','GRID_ID_1','geometry','Area_km','ID_1','xtupla','region','Región','layer','path','nueti','Contador'])

    

                 for cont in columnas:
                     columna='Conc_'+str(cont)
                     datos2=datos2.drop(columns=[columna])
                     columna='Prob10_'+str(cont)
                     datos2=datos2.drop(columns=[columna])
                     columna='Prob001_'+str(cont)
                     datos3=datos3.drop(columns=[columna])
                     columna='Prob10_'+str(cont)
                     datos3=datos3.drop(columns=[columna])

                 for cont in columnas2:

                     columna='Prob001_'+str(cont)
                     datos2=datos2.drop(columns=[columna])
                     columna='Conc_'+str(cont)
                     datos3=datos3.drop(columns=[columna])

                 datos2['Porc_min']=0
                 datos2['Porc_min']=datos2['Porc_min'].astype(float)

                 #colum=np.arange(1,ndias+1)
                 for cont in columnas3: 
                     
                     columna='Prob001_'+str(cont)
                     
                     #datos2.loc[(datos2["Indexes"]>=0) & (datos2[columna]>=0)  & (datos2["Porc_min"]==0),["Dia"]]=cont.astype(int)
                     datos2.loc[(datos2[columna]>0)  & (datos2["Porc_min"]==0),["Dia"]]=cont.astype(int)
                     
                     datos2['Dia']=datos2['Dia'].fillna(0)
                     
                    # datos2.loc[(datos2["Indexes"]>=0) & (datos2[columna]>=0)  & (datos2["Porc_min"]==0),["Porc_min"]]=datos2[columna].loc[(datos2["Indexes"]>=0) & (datos2[columna]>=0.1)  & (datos2["Porc_min"]==0)].astype(float)}

                     datos2.loc[(datos2[columna]>0)  & (datos2["Porc_min"]==0),["Porc_min"]]=datos2[columna].loc[ (datos2[columna]>0)  & (datos2["Porc_min"]==0)]
                     datos2['Porc_min']=datos2['Porc_min'].fillna(0)
                     datos2=datos2.rename(columns={columna:int(cont)})
                     

                     

                 datos2=datos2.drop(columns=['ID_1','xtupla','region','layer','path','nueti','Contador'])

                 datos['Porc_Min']=datos2['Porc_min']

                 datos['Dia_min']=datos2['Dia']
    
                # datos2=datos2.drop(columns=['Dia','Indexes','Porc_min'])
                 datos2=datos2.drop(columns=['Dia','Porc_min'])   
    
                 datos['Porc_Max']=datos2.max(axis=1)
                 datos['Dia_max']=datos2.idxmax(axis=1)
    
                 datos.loc[(datos['Porc_Max']==0),['Dia_max']]=0
                 datos.loc[(datos['Porc_Min']==0),['Dia_min']]=0                 


                 datos3['Conc_max']=datos3.max(axis=1)
                 datos['Conc_max']=datos3['Conc_max']
    
                 Con_norm=(datos['Conc_max']/np.max(datos['Conc_max']))

                 datos3['Texp']=0
                 A=np.arange(0,len(datos3))
                 datos4=datos3.drop(columns='Conc_max')
                 for n in A:
                     p=datos4.iloc[n]>0
                     B=len(p[p==True])
                     datos3.loc[n, "Texp"] = B
                     
                 datos['Texp']=datos3['Texp']
                 
                 datos['Ind']=(datos['Porc_Min']+datos['Porc_Max']+(datos['Texp']/ndias)+Con_norm)/4
                # datos['Ind2']=datos['Porc_Max']*datos['Porc_Max']*(datos['Texp']/90)*Con_norm
                 # datos['Ind3']=(datos['Porc_Max']+(datos['Texp']/90)+Con_norm)/3

                 nombre=os.path.basename(name)
                 nombre=nombre[9:]
                 nombre2="/home/gaby.resendiz/Indice_30mil_30dias/Indice"+nombre
                 datos.to_file(filename=nombre2,driver='ESRI Shapefile')
                 datos=[]