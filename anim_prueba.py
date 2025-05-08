import contextily as cx
import geopandas
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib as mpl
from matplotlib.colors import Normalize, LogNorm, BoundaryNorm  # Needed for normalize colors
from matplotlib.cm import ScalarMappable # Needed for color maps
import matplotlib as mpl

os.chdir('/home/gaby.resendiz/Probabilidad_90dias/Probabilidad')

datos_sim=geopandas.read_file('/home/gaby.resendiz/Probabilidad_90dias/Probabilidad/Prob_ARENQUE-18_primavera.shp.zip')



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
cmap = mpl.cm.rainbow
#cmap = (mpl.colors.ListedColormap(['lightgray','coral', 'lightcoral', 'indianred', 'salmon', 'tomato','chocolate','sandybrown','peru','darkorange','orange','gold','yellow','silver','grey','gray','lime']))

#bounds = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100 ]
#norm = BoundaryNorm(bounds, cmap.N, ) #extend='both')



i=89

def update_fig(i):

    #norm=Normalize(vmin=0,vmax=maximo)

    #norm=Normalize(vmin=1,vmax=maximo)

    ax.clear()
    #fig, ax = plt.subplots(figsize=(12, 12))
    name='Conteo_'+str(i+1)
    datos_sim.plot(ax=ax,column = name, cmap=cmap,linewidth=1,legend=False, vmin=0, vmax=maximo)
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
    ax.set_title(('Probabilidad dia: ' + str(cont_dia)), fontsize=25, pad=30, weight='bold')
    
    #plt.savefig('Mapa_'+str(i))
    #plt.close()
    return ax

fig, ax = plt.subplots(figsize=(12, 12))

# Build the color bar norm=norm
cbar=fig.colorbar(mpl.cm.ScalarMappable(cmap=cmap), ax=ax, orientation='horizontal',label='%')
cbar.FontSize=12


# Creatre a list with unique dates
from matplotlib.animation import FuncAnimation
ani= FuncAnimation(fig, update_fig, frames=90,interval=300,blit=False)
ani.save(filename="ARENQUE-18_primavera.gif", writer="pillow")