# Basic scatter plot, log scale
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
#from pyproj import Proj, transform
from pyproj import Transformer
import numpy as np
import time
import requests
import json

# transform to and from Irish Grid and Lat Long
transformerToXY = Transformer.from_crs("epsg:4326", "epsg:29902")
transformerFromXY = Transformer.from_crs("epsg:29902", "epsg:4326")

######################
# load file and create DF

filename="MetEireann 200.txt"
grDat=pd.read_csv(filename)

ListEast=grDat["east"].to_numpy()
ListNorth=grDat["north"].to_numpy()
# take the east and north columns and create numpy array

respArr=transformerFromXY.transform(ListEast,ListNorth)  # pass pts in dataframe
#print(respArr[0],respArr[1])

# create new dataframes of the results, rounded to 6 dp
newDFLat=np.around(pd.DataFrame(respArr[0]),decimals=6)
newDFLong=np.around(pd.DataFrame(respArr[1]),decimals=6)

grDat["Latit"]=newDFLat
grDat["Longit"]=newDFLong
grDat["Elev"]=0

url1='https://api.opentopodata.org/v1/eudem25m?locations='

# loop through the elements in the dataframe
# need to set up 2 nested loops so that can repeat the 100 reuests

# create DF to hold the results so that they can be merged with the initial values
ElevRes = pd.DataFrame(columns=['Latit', 'Longit', 'Elev'])
print(ElevRes)

def CreateURL(w, url):
    for s in range(w):
        url=url + str(grDat.loc[y*100 + s,"Latit"]) + "," + str(grDat.loc[y*100 + s,"Longit"]) + "|"
    url = url[:-1]
    return url

for y in range(2):
    time.sleep(1)   # insert 1 second delay so that don't exceed the 1 per second URL request
    url1 = 'https://api.opentopodata.org/v1/eudem25m?locations='
 #   for s in range(100):
 #       url1=url1 + str(grDat.loc[y*5 + s,"Latit"]) + "," + str(grDat.loc[y*5 + s,"Longit"]) + "|"
    print(CreateURL(100, url1))
  #  url1=url1[:-1]  # remove the final "|"
