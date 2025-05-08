import contextily as cx
import geopandas
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib as mpl
from matplotlib.colors import Normalize, LogNorm, BoundaryNorm  # Needed for normalize colors
from matplotlib.cm import ScalarMappable # Needed for color maps
import matplotlib as mpl

file='/home/gaby.resendiz/Conc_prob_promedio30mil/Prom_conc_BALAM-3_invierno.shp.zip'
#os.chdir('/home/gaby.resendiz/Dia_afec/')
os.chdir('/home/gaby.resendiz/Conc_prob_promedio30mil')

#datos_sim=geopandas.read_file('/home/gaby.resendiz/Dia_afec/Dia_afec_AYATSIL-285_invierno.shp.zip')
datos_sim=geopandas.read_file(file)
datos_sim=datos_sim.drop(columns= ['Id','GRID_ID','X','Y','GRID_ID_1','geometry','Area_km','ID_1','xtupla','region','Región','layer','path','nueti','Contador'])


columnas=np.arange(1,91)
for cont in columnas:
    columna='Prob001_'+str(cont)
    datos_sim=datos_sim.drop(columns=[columna])
    columna='Prob10_'+str(cont)
    datos_sim=datos_sim.drop(columns=[columna])



maximo=np.max(datos_sim.max())
minimo=np.max(datos_sim.min())
##datos_sim.replace(0, np.nan, inplace=True)

datos_sim=geopandas.read_file(file)

fig, ax = plt.subplots(figsize=(12, 12))

cx.add_basemap(ax, crs=datos_sim.crs, source=cx.providers.Esri.WorldImagery)

#50, 60, 70, 80, 90,
#,scheme='NaturalBreaks'
cmap = mpl.cm.Reds
#jet
#rainbow



norm = mpl.colors.Normalize(vmin=0, vmax=maximo)

#cmap = (mpl.colors.ListedColormap(['lightgray','coral', 'lightcoral', 'indianred', 'salmon', 'tomato','chocolate','sandybrown','peru','darkorange','orange','gold','yellow','silver','grey','gray','lime']))



bounds =np.arange(0,maximo+0.2,0.2)
norm = BoundaryNorm(bounds, cmap.N, ) #extend='both')


i=89

def update_fig(i):

    #norm=Normalize(vmin=0,vmax=maximo)

   # norm=Normalize(vmin=0,vmax=maximo)

    ax.clear()
    #fig, ax = plt.subplots(figsize=(12, 12))
    name='Conc_'+str(i+1)
    datos_sim.plot(ax=ax,column = name, cmap=cmap,linewidth=1,legend=False, norm=norm,vmin=0, vmax=maximo)
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
    cont_dia=(i+1)
    # Title, lines and annotations
    ax.set_title(('Concentración dia: ' + str(cont_dia)), fontsize=25, pad=30, weight='bold')
    
    #plt.savefig('Mapa_'+str(i))
    #plt.close()
    return ax

fig, ax = plt.subplots(figsize=(12, 12))

# Build the color bar norm=norm

cbar=fig.colorbar(mpl.cm.ScalarMappable(cmap=cmap,norm=norm), ax=ax, orientation='horizontal',label='g/m\u00b2')
cbar.FontSize=12

#writervideo = animation.FFMpegWriter(fps=60) 
#anim.save(f, writer=writervideo)
# Creatre a list with unique dates

from matplotlib.animation import FuncAnimation

ani= FuncAnimation(fig, update_fig, frames=90,interval=500,blit=False)
ani.save(filename="Conc_BALAM_invierno.gif", writer= writer="pillow")