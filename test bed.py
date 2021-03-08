# Basic scatter plot, log scale
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
#from pyproj import Proj, transform
from pyproj import Transformer
import numpy as np
import time
import requests

# transform to and from Irish Grid and Lat Long
transformerToXY = Transformer.from_crs("epsg:4326", "epsg:29902")
transformerFromXY = Transformer.from_crs("epsg:29902", "epsg:4326")


filename="MetEireann 20.txt"
grDat=pd.read_csv(filename)
#print(grDat)

## need to use the "inplace" function to make sure that change applied to this DF
#tmpDF.loc[:,"NewEast"]=tmpDF2.loc[:,"east"]
#grDat.set_index(["east","north"],inplace=True)
#print(grDat)


#print(grDat.loc[0,"east"])
#grDat.loc[0,"east"]=2500
#print(grDat.loc[0,"east"])

ListEast=grDat["east"].to_numpy()
ListNorth=grDat["north"].to_numpy()
# take the east and north columns and create numpy array


respArr=transformerFromXY.transform(ListEast,ListNorth)  # pass pts in dataframe
#print(respArr[0],respArr[1])

# create new dataframes of the results, rounded to 6 dp
#newDFLat=pd.DataFrame(respArr[0])
#newDFLong=pd.DataFrame(respArr[1])

newDFLat=np.around(pd.DataFrame(respArr[0]),decimals=6)
newDFLong=np.around(pd.DataFrame(respArr[1]),decimals=6)

grDat["Latit"]=newDFLat
grDat["Longit"]=newDFLong
grDat["Elev"]=0


url1='https://api.opentopodata.org/v1/eudem25m?locations='

# loop through the elements in the dataframe
# need to set up 2 nested loops so that can repeat the 100 reuests

for y in range(4):
    time.sleep(1)   # insert 1 second delay so that don't exceed the 1 per second URL request
    url1 = 'https://api.opentopodata.org/v1/eudem25m?locations='
    for s in range(4):
        url1=url1 + str(grDat.loc[y*5 + s,"Latit"]) + "," + str(grDat.loc[y*5 + s,"Longit"]) + "|"

    url1=url1 + str(grDat.loc[y*5 + 4,"Latit"]) + "," + str(grDat.loc[y*5 + 4,"Longit"])

    print(url1)
    r = requests.get(url1)
    json_data = r.json()
    for key, value in json_data.items():
        print(key + ':', value)

    df=pd.json_normalize(json_data)

    print(df["results"][0][0])
    newdf=pd.DataFrame.from_dict(df["results"][0])
    print(newdf)

# loop through the results and copy, item by item, to the original DF
    for w in range(5):
        grDat.loc[y*5 + w, "Elev"]=newdf.loc[w,"elevation"]

# need to get the JSON file into a DF with the elevation, lat and long so that I can do a left join
stations_new=stations.merge(ridership, on="station_id", how="left")

print(grDat)
