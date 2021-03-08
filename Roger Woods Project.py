# Basic scatter plot, log scale
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
#from pyproj import Proj, transform
from pyproj import Transformer
import numpy as np

import requests

# transform to and from Irish Grid and Lat Long
transformerToXY = Transformer.from_crs("epsg:4326", "epsg:29902")
transformerFromXY = Transformer.from_crs("epsg:29902", "epsg:4326")


filename="MetEireann.txt"
grDat=pd.read_csv(filename)
#print(grDat)
#m1TmaxMin=grDat["m1Tmax"].min()  # 2.9
#m1TmaxMax=grDat["m1Tmax"].max()  # 10.1

#tmpT=grDat["m1Tmax"].to_numpy()

# get the min and max easting and northing values and print
print("Min East = " + str(grDat["east"].min()))
print("Max East = " + str(grDat["east"].max()))
print("Min North = " + str(grDat["north"].min()))
print("Max North = " + str(grDat["north"].max()))

####################################################
###########################################
# this only looks at the first 50 rows
# get the first 5 rows into new DF
# the first 5 values have some sea points with elevation=0 which is a NaN in dataframe
# so can do some data cleaning!!!!!!

tmpDF=grDat.iloc[:50]
print(tmpDF)

# take the east and north columns and create numpy array
tmpDFX=tmpDF["east"].to_numpy()
tmpDFY=tmpDF["north"].to_numpy()

###########################################################
###########################################################
# create numpy arrays of the easting and northings
ListEast=grDat["east"].to_numpy()
ListNorth=grDat["north"].to_numpy()

# convert pts from XY to LL
# information is returned in brackets as common separated arrays.
# It can be accessed using square brackets, 0 for latitude, 1 for longitude
respArr=transformerFromXY.transform(ListEast,ListNorth)  # pass pts in dataframe
#print(respArr[0],respArr[1])

# create new dataframes of the results, rounded to 6 dp
#newDFLat=pd.DataFrame(respArr[0])
#newDFLong=pd.DataFrame(respArr[1])

newDFLat=np.around(pd.DataFrame(respArr[0]),decimals=6)
newDFLong=np.around(pd.DataFrame(respArr[1]),decimals=6)

# create a new Elev column
grDat["Latit"]=newDFLat
grDat["Longit"]=newDFLong

# set Elev column to zero
grDat["Elev"]=0

print(grDat.columns)
print(grDat)

tempDF=grDat.iloc[:50]
print(tempDF)

#url = 'https://api.open-elevation.com/api/v1/lookup\?locations\=10,10\|20,20\|41.161758,-8.583933'
# doesnt seem to work
#url='https://api.open-elevation.com/api/v1/lookup?locations=41.161758,-8.583933'

# elevation api website. Free for a 5km grid hence maybe not that good to use
#url='https://elevation-api.io/api/elevation?points=(53.100736,-6.408332),(62.52417,10.02487)&key=mc9Y4kCAoU88ol677jb0gAA-u9O7DP'


# this works. Max 100 locations per request, 1 call per second, 1000 calls per day
url='https://api.opentopodata.org/v1/eudem25m?locations=53.100736,-6.408332|53.200736,-6.508332'
url1='https://api.opentopodata.org/v1/eudem25m?locations='
#nrows=len(tempDF.index)
#print(nrows)
# loop through the elements in the dataframe
#print(tempDF.loc[0,"Latit"])
for s in range(49):
    url1=url1 + str(tempDF.loc[s,"Latit"]) + "," + str(tempDF.loc[s,"Longit"]) + "|"

url1=url1 + str(tempDF.loc[49,"Latit"]) + "," + str(tempDF.loc[49,"Longit"])
print(url)
print(url1)

r = requests.get(url1)
#r=requests.post(url)
#print(r.text)    # prints out the text that has been returned
json_data = r.json()
for key, value in json_data.items():
    print(key + ':', value)

df=pd.json_normalize(json_data)
#print(df.columns)
#print(df)
print(df["results"][0][0])
newdf=pd.DataFrame.from_dict(df["results"][0])
print(newdf)

# loop through the results and copy, item by item, to the original DF
for s in range(49):
    tempDF.loc[s, "Elev"]=newdf.loc[s,"elevation"]

print(tempDF)
#tempDF.to_csv("tempDF.txt")
#newdf.to_csv("newdf.txt")
#tempDF["Elevation"]=newdf["elevation"]
