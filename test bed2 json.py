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

## need to use the "inplace" function to make sure that change applied to this DF
#tmpDF.loc[:,"NewEast"]=tmpDF2.loc[:,"east"]
#grDat.set_index(["east","north"],inplace=True)
#print(grDat)

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

for y in range(1):
    time.sleep(1)   # insert 1 second delay so that don't exceed the 1 per second URL request
    url1 = 'https://api.opentopodata.org/v1/eudem25m?locations='
    for s in range(99):
        url1=url1 + str(grDat.loc[y*5 + s,"Latit"]) + "," + str(grDat.loc[y*5 + s,"Longit"]) + "|"

    url1=url1 + str(grDat.loc[y*5 + 99,"Latit"]) + "," + str(grDat.loc[y*5 + 99,"Longit"])

    r = requests.get(url1)
    json_data = r.json()
  #  print(json_data)
    newlist = pd.json_normalize(json_data, record_path=["results"])
  #  print(newlist)

    # filter the list to take coords and elevation
    elev=newlist.filter(["location.lat","location.lng","elevation"], axis=1)
    elev.rename(columns={"location.lat":"Latit","location.lng":"Longit","elevation":"Elev"},inplace=True)

# concat the results to new DF and then rename so that ready for next set of results
    ElevRes2=pd.concat([ElevRes,elev],ignore_index=True)
    ElevRes=ElevRes2

print(ElevRes)

#print(grDat)

grDat_new=grDat.merge(ElevRes, on=["Latit","Longit"], how="left")

print(grDat_new)

grDat_new.to_csv("MerEireann 200 out.txt")
#df = pd.DataFrame(np.array(([1, 2, 3], [4, 5, 6])),
#                index=['mouse', 'rabbit'],
#                  columns=['one', 'two', 'three'])
#print(df)
#df.rename(columns={"one":"o1","two":"t2","three":"t3"},inplace=True)
#print(df)

#    elev_res=newlist["elevation"]
#    print(elev_res[1])
   # print(df["results"][0][0])
   # newdf=pd.DataFrame.from_dict(df["results"][0])
   # print(newdf)

# loop through the results and copy, item by item, to the original DF
   # for w in range(5):
   #     grDat.loc[y*5 + w, "Elev"]=newdf.loc[w,"elevation"]

