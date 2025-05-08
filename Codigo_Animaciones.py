# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import contextily as cx
import geopandas
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib as mpl
from matplotlib.colors import Normalize, LogNorm, BoundaryNorm  # Needed for normalize colors
from matplotlib.cm import ScalarMappable # Needed for color maps
import matplotlib as mpl


datos_sim=geopandas.read_file('Salidas_conteos_c6horas/Conteo_BALAM-3_verano.shp.zip')


#fig, ax = plt.subplots(figsize=(10,10))

#datos_sim.plot(ax=ax,column = 'Conteo_1',scheme='natural_breaks', k=10, cmap = 'Spectral_r', legend = True, figsize= (10,10))
#cx.add_basemap(ax, crs=Balam_Invierno.crs, source=cx.providers.Esri.WorldTerrain)

#plt.savefig('Conteototal_P1.png')

datos_sim['Conteo_total']=datos_sim['Conteo_1']+datos_sim['Conteo_2']+datos_sim['Conteo_3']+datos_sim['Conteo_4']+datos_sim['Conteo_5']+datos_sim['Conteo_6']+datos_sim['Conteo_7']+datos_sim['Conteo_8']+datos_sim['Conteo_9']+datos_sim['Conteo_10']+datos_sim['Conteo_11']+datos_sim['Conteo_12']+datos_sim['Conteo_13']+datos_sim['Conteo_14']+datos_sim['Conteo_15']+datos_sim['Conteo_16']+datos_sim['Conteo_17']+datos_sim['Conteo_18']+datos_sim['Conteo_19']+datos_sim['Conteo_20']+datos_sim['Conteo_21']+datos_sim['Conteo_22']+datos_sim['Conteo_23']+datos_sim['Conteo_24']+datos_sim['Conteo_25']+datos_sim['Conteo_26']+datos_sim['Conteo_27']+datos_sim['Conteo_28']+datos_sim['Conteo_29']




dias=np.arange(1,90)
maximos=np.arange(1, 90)
minimos=np.arange(1,90)



for nn in dias:
    
    nombre='Conteo_'+str(nn)
    #datos_sim[nombre] = datos_sim[nombre].replace({'0':np.nan, 0:np.nan})
    datos_sim[nombre]=(datos_sim[nombre]/np.sum(datos_sim[nombre]))*100
    



for nn in dias:
    
    nombre='Conteo_'+str(nn)
    maximos[nn-1]=np.max(datos_sim[nombre])
    minimos[nn-1]=np.min(datos_sim[nombre])



maximo=np.max(maximos)
minimo=np.min(minimos)



fig, ax = plt.subplots(figsize=(12, 12))

cx.add_basemap(ax, crs=datos_sim.crs, source=cx.providers.Esri.WorldImagery)

#50, 60, 70, 80, 90,
#,scheme='NaturalBreaks'
#cmap = mpl.cm.ocean
cmap = (mpl.colors.ListedColormap(['lightgray','coral', 'lightcoral', 'indianred', 'salmon', 'tomato','chocolate','sandybrown','peru','darkorange','orange','gold','yellow','silver','grey','gray','lime']))

bounds = [0, 0.5, 1, 3, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100 ]
norm = BoundaryNorm(bounds, cmap.N, ) #extend='both')



#norm=Normalize(vmin=minimo,vmax=maximo)
#fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
 #            cax=ax, orientation='horizontal',
  #           label="Discrete intervals with extend='both' keyword")

i=118

def update_fig(i):

    #norm=Normalize(vmin=0,vmax=maximo)

    #norm=Normalize(vmin=1,vmax=maximo)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N,) # extend='both')

    ax.clear()
    #fig, ax = plt.subplots(figsize=(12, 12))
    name='Conteo_'+str(i+1)
    datos_sim.plot(ax=ax,column = name, cmap=cmap,linewidth=1,legend=False, norm=norm, vmin=0, vmax=maximo)
    cx.add_basemap(ax, crs=datos_sim.crs, source=cx.providers.Esri.WorldImagery)
    #fig.colorbar(ax.collections[0], ax=ax)
    
    

    #fig = ax.get_figure()
   # cax = fig.add_axes([0.9, 0.1, 0.03, 0.8])
    #sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=0, vmax=maximo),)
    # fake up the array of the scalar mappable. Urgh...
   # sm._A = []
   # fig.colorbar(sm, cax=cax)
    ax.xaxis.set_visible(True)
    ax.yaxis.set_visible(True)
    ax.axis('on')
    cont_dia=(i+1)*6
    # Title, lines and annotations
    ax.set_title(('No. partículas hora: ' + str(cont_dia)), fontsize=25, pad=30, weight='bold')
    
    #plt.savefig('Mapa_'+str(i))
    #plt.close()
    return ax

fig, ax = plt.subplots(figsize=(12, 12))

# Build the color bar norm=norm
cbar=fig.colorbar(mpl.cm.ScalarMappable(cmap=cmap,norm=norm), ax=ax, orientation='vertical',label='%')
cbar.FontSize=12


# Creatre a list with unique dates
from matplotlib.animation import FuncAnimation
ani= FuncAnimation(fig, update_fig, frames=119,interval=300,blit=False)
ani.save(filename="Conteo_BALAM-3_verano.gif", writer="pillow")


