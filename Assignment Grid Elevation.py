# Basic scatter plot, log scale
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
import numpy as np
#from pyproj import Proj, transform
from pyproj import Transformer

#print(reproject_wgs_to_itm(-7.748108, 53.431628))
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

# viridis takes a number between 0 and 1 and returns a colour
viridis = cm.get_cmap('viridis', 8)

seqe=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
#for s in seqe:
    #print(viridis(s))

#print(viridis(0.66))

filename="MerEireann Results with elevation and LL.txt"
grDat=pd.read_csv(filename)
filename1="Met Eireann Min T.txt"
grDatMin=pd.read_csv(filename1)

grDat_new=grDat.merge(grDatMin, on=["east","north"], how="left")
print(grDat)
##############################
# try the above using the scatter plat and the "c" method to colour the points by temp
# see https://matplotlib.org/stable/tutorials/colors/colormaps.html#sphx-glr-tutorials-colors-colormaps-py
# for color maps. terrain looks like a good choice
################################

plt.figure(figsize=(9, 10), dpi=80)  # set the size of the image window. figsize x dpi gives the output size
plt.scatter(grDat["east"], grDat["north"], 1,c=grDat["Elev_y"],cmap="terrain")
plt.xlabel("x coord")
plt.ylabel("y coord")
# Add title
cbar=plt.colorbar()   # shows legend to the side
cbar.set_label("elevation (m)")
plt.title("Ireland Grid using c colour method")
plt.show()

#sns.scatterplot(grDat["east"], grDat["north"], data=grDat, hue=grDat["Elev_y"])
#plt.show()
def histogram_intersection(a, b):
    v = np.minimum(a, b).sum().round(decimals=1)
    return v
print(grDat.corr(method=histogram_intersection))

# max temp plot
plt.figure(figsize=(9, 10), dpi=80)  # set the size of the image window. figsize x dpi gives the output size
plt.scatter(grDat["m1Tmax"], grDat["Elev_y"])
plt.xlabel("Max temp")
plt.ylabel("Elevation (m)")
plt.show()

# min emp plot
plt.figure(figsize=(9, 10), dpi=80)  # set the size of the image window. figsize x dpi gives the output size
plt.scatter(grDat_new["m1Tmin"], grDat_new["Elev_y"])
plt.xlabel("Min temp")
plt.ylabel("Elevation (m)")
plt.show()