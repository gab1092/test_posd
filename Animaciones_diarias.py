
import contextily as cx
import geopandas
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib as mpl
from matplotlib.colors import Normalize, LogNorm# Needed for normalize colors
from matplotlib.cm import ScalarMappable # Needed for color maps
from matplotlib.patches import Patch # Needed for adding figures


datos_sim=geopandas.read_file('Conteos_2/Conteo_TEEKIT-45_invierno.shp.zip')


#fig, ax = plt.subplots(figsize=(10,10))

#datos_sim.plot(ax=ax,column = 'Conteo_1',scheme='natural_breaks', k=10, cmap = 'Spectral_r', legend = True, figsize= (10,10))
#cx.add_basemap(ax, crs=Balam_Invierno.crs, source=cx.providers.Esri.WorldTerrain)

#plt.savefig('Conteototal_P1.png')

datos_sim['Conteo_total']=datos_sim['Conteo_1']+datos_sim['Conteo_2']+datos_sim['Conteo_3']+datos_sim['Conteo_4']+datos_sim['Conteo_5']+datos_sim['Conteo_6']+datos_sim['Conteo_7']+datos_sim['Conteo_8']+datos_sim['Conteo_9']+datos_sim['Conteo_10']+datos_sim['Conteo_11']+datos_sim['Conteo_12']+datos_sim['Conteo_13']+datos_sim['Conteo_14']+datos_sim['Conteo_15']+datos_sim['Conteo_16']+datos_sim['Conteo_17']+datos_sim['Conteo_18']+datos_sim['Conteo_19']+datos_sim['Conteo_20']+datos_sim['Conteo_21']+datos_sim['Conteo_22']+datos_sim['Conteo_23']+datos_sim['Conteo_24']+datos_sim['Conteo_25']+datos_sim['Conteo_26']+datos_sim['Conteo_27']+datos_sim['Conteo_28']+datos_sim['Conteo_29']




dias=np.arange(1,31)
maximos=np.arange(1,31)



for nn in dias:
    
    nombre='Conteo_'+str(nn)
    datos_sim[nombre]=(datos_sim[nombre]/np.sum(datos_sim[nombre]))*100



for nn in dias:
    
    nombre='Conteo_'+str(nn)
    maximos[nn-1]=np.max(datos_sim[nombre])



maximo=np.max(maximos)

    


fig, ax = plt.subplots(figsize=(12, 12))

cx.add_basemap(ax, crs=datos_sim.crs, source=cx.providers.Esri.WorldTerrain)


#,scheme='NaturalBreaks'

norm=LogNorm(vmin=1,vmax=maximo)
i=29

def update_fig(i):
    
    norm=LogNorm(vmin=1,vmax=maximo)

    ax.clear()
    #fig, ax = plt.subplots(figsize=(12, 12))
    name='Conteo_'+str(i+1)
    datos_sim.plot(ax=ax,column = name, cmap='viridis_r',linewidth=1,legend=False, norm=norm, vmin=1, vmax=maximo)
    cx.add_basemap(ax, crs=datos_sim.crs, source=cx.providers.Esri.WorldTerrain)
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
    cont_dia=(i+1)
    # Title, lines and annotations
    ax.set_title(('No. partículas hora: ' + str(cont_dia)), fontsize=25, pad=30, weight='bold')
    
    #plt.savefig('Mapa_'+str(i))
    #plt.close()
    return ax

fig, ax = plt.subplots(figsize=(12, 12))

# Build the color bar
cbar=fig.colorbar(mpl.cm.ScalarMappable(cmap='rainbow',norm=norm),
            ax=ax, orientation='vertical', label='')
cbar.FontSize=12


# Creatre a list with unique dates
from matplotlib.animation import FuncAnimation
ani= FuncAnimation(fig, update_fig, frames=30,interval=300,blit=False)
ani.save(filename="Animacion_p1.gif", writer="pillow")