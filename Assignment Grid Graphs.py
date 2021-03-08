# Basic scatter plot, log scale
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
#from pyproj import Proj, transform
from pyproj import Transformer

#def reproject_wgs_to_itm(longitude, latitude):
 #   prj_wgs = Proj(init='epsg:4326')
 #   prj_itm = Proj(init='epsg:2157')
 #   x, y = transform(prj_wgs, prj_itm, longitude, latitude)
 #   return x, y

#transformer = Transformer.from_crs("epsg:4326", "epsg:2157")
transformerToXY = Transformer.from_crs("epsg:4326", "epsg:29902")
transformerFromXY = Transformer.from_crs("epsg:29902", "epsg:4326")
#resp=transformerFromXY.transform(267187, 194797)
#print(resp)
tstPtsY=[345000,398000]
tstPtsX=[150000,350000]

# pass pts in dataframe. Results returned in dataframe
respArr=transformerFromXY.transform(tstPtsX,tstPtsY)  # pass pts in dataframe
#print(respArr)
#resp=transformerToXY.transform(53, -7)
#print(resp)
resp=transformerToXY.transform(54, -8)
#print(resp[0])



#print(reproject_wgs_to_itm(-7.748108, 53.431628))
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

# viridis takes a number between 0 and 1 and returns a colour
viridis = cm.get_cmap('viridis', 8)

seqe=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
#for s in seqe:
    #print(viridis(s))

#print(viridis(0.66))

filename="MetEireann.txt"
grDat=pd.read_csv(filename)
#print(grDat)
m1TmaxMin=grDat["m1Tmax"].min()  # 2.9
m1TmaxMax=grDat["m1Tmax"].max()  # 10.1

tmpT=grDat["m1Tmax"].to_numpy()
#print(tmpT)

# get the first 5 rows into new DF
tmpDF=grDat.iloc[:5]
print(tmpDF)

# take the east and north columns and create numpy array
tmpDFX=tmpDF["east"].to_numpy()
tmpDFY=tmpDF["north"].to_numpy()

# create numpy arrays of the easting an northings
ListEast=grDat["east"].to_numpy()
ListNorth=grDat["north"].to_numpy()

# convert pts from XY to LL
# information is returned in brackets as common separated arrays.
# It can be accessed using square brackets, 0 for latitude, 1 for longitude
respArr=transformerFromXY.transform(ListEast,ListNorth)  # pass pts in dataframe
print(respArr[0],respArr[1])

# create new dataframes of the results
newDFLat=pd.DataFrame(respArr[0])
newDFLong=pd.DataFrame(respArr[1])
#print(newDFLat)
#print(newDFLong)
grDat["Latit"]=newDFLat
grDat["Longit"]=newDFLong
print(grDat)


import requests
url = 'https://api.open-elevation.com/api/v1/lookup\?locations\=10,10\|20,20\|41.161758,-8.583933'
#r = requests.get(url)
r=requests.post(url)
print(r.text)    # prints out the text that has been returned
json_data = r.json()
#for key, value in json_data.items():
#    print(key + ':', value)



# check the normalize function at
# https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.Normalize.html#matplotlib.colors.Normalize

# calculate the scaled max temp
grDat["scaleTemp"]= (grDat["m1Tmax"]-m1TmaxMin)/(m1TmaxMax-m1TmaxMin)
#print(grDat)
# use the color argument to pass the color based on the array temperature which has been scaled between 0 and 1
plt.figure(figsize=(9, 10), dpi=80)  # set the size of the image window. figsize x dpi gives the output size
plt.scatter(grDat["east"], grDat["north"],s=1,color=viridis(grDat["scaleTemp"])) #, s = grDat["m1Tmax"]
plt.xlabel("x coord")
plt.ylabel("y coord")
# Add title
plt.title("Ireland Grid")
#plt.show()

##############################
# try the above using the scatter plat and the "c" method to colour the points by temp
################################

plt.figure(figsize=(9, 10), dpi=80)  # set the size of the image window. figsize x dpi gives the output size
plt.scatter(grDat["east"], grDat["north"],c=grDat["m1Tmax"])
plt.xlabel("x coord")
plt.ylabel("y coord")
# Add title
plt.title("Ireland Grid using c colour method")
#plt.show()

##############################
# try the above using the scatter plot in subplots and the "c" method to colour the points by temp
################################

fig, ax = plt.subplots()
fig.set_figheight(9)
fig.set_figwidth(7)

#plt.figure(figsize=(9, 10), dpi=80)  # set the size of the image window. figsize x dpi gives the output size
ax.scatter(grDat["east"], grDat["north"],c=grDat["m1Tmax"])
ax.set_xlabel("x coord")
ax.set_ylabel("y coord")
# Add title
plt.title("Ireland Grid using c colour method")
#plt.show()





col=['red', 'green', 'blue', 'blue', 'yellow', 'black', 'green', 'red', 'red', 'green', 'blue', 'yellow', 'green', 'blue', 'yellow', 'green', 'blue', 'blue', 'red', 'blue', 'yellow', 'blue', 'blue', 'yellow', 'red', 'yellow', 'blue', 'blue', 'blue', 'yellow', 'blue', 'green', 'yellow', 'green', 'green', 'blue', 'yellow', 'yellow', 'blue', 'yellow', 'blue', 'blue', 'blue', 'green', 'green', 'blue', 'blue', 'green', 'blue', 'green', 'yellow', 'blue', 'blue', 'yellow', 'yellow', 'red', 'green', 'green', 'red', 'red', 'red', 'red', 'green', 'red', 'green', 'yellow', 'red', 'red', 'blue', 'red', 'red', 'red', 'red', 'blue', 'blue', 'blue', 'blue', 'blue', 'red', 'blue', 'blue', 'blue', 'yellow', 'red', 'green', 'blue', 'blue', 'red', 'blue', 'red', 'green', 'black', 'yellow', 'blue', 'blue', 'green', 'red', 'red', 'yellow', 'yellow', 'yellow', 'red', 'green', 'green', 'yellow', 'blue', 'green', 'blue', 'blue', 'red', 'blue', 'green', 'blue', 'red', 'green', 'green', 'blue', 'blue', 'green', 'red', 'blue', 'blue', 'green', 'green', 'red', 'red', 'blue', 'red', 'blue', 'yellow', 'blue', 'green', 'blue', 'green', 'yellow', 'yellow', 'yellow', 'red', 'red', 'red', 'blue', 'blue']
gdp_cap=[974.5803384, 5937.029525999998, 6223.367465, 4797.231267, 12779.37964, 34435.367439999995, 36126.4927, 29796.04834, 1391.253792, 33692.60508, 1441.284873, 3822.137084, 7446.298803, 12569.85177, 9065.800825, 10680.79282, 1217.032994, 430.0706916, 1713.778686, 2042.09524, 36319.23501, 706.016537, 1704.063724, 13171.63885, 4959.114854, 7006.580419, 986.1478792, 277.5518587, 3632.557798, 9645.06142, 1544.750112, 14619.222719999998, 8948.102923, 22833.30851, 35278.41874, 2082.4815670000007, 6025.3747520000015, 6873.262326000001, 5581.180998, 5728.353514, 12154.08975, 641.3695236000002, 690.8055759, 33207.0844, 30470.0167, 13206.48452, 752.7497265, 32170.37442, 1327.60891, 27538.41188, 5186.050003, 942.6542111, 579.2317429999998, 1201.637154, 3548.3308460000007, 39724.97867, 18008.94444, 36180.78919, 2452.210407, 3540.651564, 11605.71449, 4471.061906, 40675.99635, 25523.2771, 28569.7197, 7320.8802620000015, 31656.06806, 4519.461171, 1463.249282, 1593.06548, 23348.139730000006, 47306.98978, 10461.05868, 1569.331442, 414.5073415, 12057.49928, 1044.770126, 759.3499101, 12451.6558, 1042.581557, 1803.151496, 10956.99112, 11977.57496, 3095.7722710000007, 9253.896111, 3820.17523, 823.6856205, 944.0, 4811.060429, 1091.359778, 36797.93332, 25185.00911, 2749.320965, 619.6768923999998, 2013.977305, 49357.19017, 22316.19287, 2605.94758, 9809.185636, 4172.838464, 7408.905561, 3190.481016, 15389.924680000002, 20509.64777, 19328.70901, 7670.122558, 10808.47561, 863.0884639000002, 1598.435089, 21654.83194, 1712.472136, 9786.534714, 862.5407561000002, 47143.17964, 18678.31435, 25768.25759, 926.1410683, 9269.657808, 28821.0637, 3970.095407, 2602.394995, 4513.480643, 33859.74835, 37506.41907, 4184.548089, 28718.27684, 1107.482182, 7458.396326999998, 882.9699437999999, 18008.50924, 7092.923025, 8458.276384, 1056.380121, 33203.26128, 42951.65309, 10611.46299, 11415.80569, 2441.576404, 3025.349798, 2280.769906, 1271.211593, 469.70929810000007]
life_exp=[43.828, 76.423, 72.301, 42.731, 75.32, 81.235, 79.829, 75.635, 64.062, 79.441, 56.728, 65.554, 74.852, 50.728, 72.39, 73.005, 52.295, 49.58, 59.723, 50.43, 80.653, 44.74100000000001, 50.651, 78.553, 72.961, 72.889, 65.152, 46.462, 55.322, 78.782, 48.328, 75.748, 78.273, 76.486, 78.332, 54.791, 72.235, 74.994, 71.33800000000002, 71.878, 51.57899999999999, 58.04, 52.947, 79.313, 80.657, 56.735, 59.448, 79.406, 60.022, 79.483, 70.259, 56.007, 46.38800000000001, 60.916, 70.19800000000001, 82.208, 73.33800000000002, 81.757, 64.69800000000001, 70.65, 70.964, 59.545, 78.885, 80.745, 80.546, 72.567, 82.603, 72.535, 54.11, 67.297, 78.623, 77.58800000000002, 71.993, 42.592, 45.678, 73.952, 59.44300000000001, 48.303, 74.241, 54.467, 64.164, 72.801, 76.195, 66.803, 74.543, 71.164, 42.082, 62.069, 52.90600000000001, 63.785, 79.762, 80.204, 72.899, 56.867, 46.859, 80.196, 75.64, 65.483, 75.53699999999998, 71.752, 71.421, 71.688, 75.563, 78.098, 78.74600000000002, 76.442, 72.476, 46.242, 65.528, 72.777, 63.062, 74.002, 42.56800000000001, 79.972, 74.663, 77.926, 48.159, 49.339, 80.941, 72.396, 58.556, 39.613, 80.884, 81.70100000000002, 74.143, 78.4, 52.517, 70.616, 58.42, 69.819, 73.923, 71.777, 51.542, 79.425, 78.242, 76.384, 73.747, 74.249, 73.422, 62.698, 42.38399999999999, 43.487]
pop=[31.889923, 3.600523, 33.333216, 12.420476, 40.301927, 20.434176, 8.199783, 0.708573, 150.448339, 10.392226, 8.078314, 9.119152, 4.552198, 1.639131, 190.010647, 7.322858, 14.326203, 8.390505, 14.131858, 17.696293, 33.390141, 4.369038, 10.238807, 16.284741, 1318.683096, 44.22755, 0.71096, 64.606759, 3.80061, 4.133884, 18.013409, 4.493312, 11.416987, 10.228744, 5.46812, 0.496374, 9.319622, 13.75568, 80.264543, 6.939688, 0.551201, 4.906585, 76.511887, 5.23846, 61.083916, 1.454867, 1.688359, 82.400996, 22.873338, 10.70629, 12.572928, 9.947814, 1.472041, 8.502814, 7.483763, 6.980412, 9.956108, 0.301931, 1110.396331, 223.547, 69.45357, 27.499638, 4.109086, 6.426679, 58.147733, 2.780132, 127.467972, 6.053193, 35.610177, 23.301725, 49.04479, 2.505559, 3.921278, 2.012649, 3.193942, 6.036914, 19.167654, 13.327079, 24.821286, 12.031795, 3.270065, 1.250882, 108.700891, 2.874127, 0.684736, 33.757175, 19.951656, 47.76198, 2.05508, 28.90179, 16.570613, 4.115771, 5.675356, 12.894865, 135.031164, 4.627926, 3.204897, 169.270617, 3.242173, 6.667147, 28.674757, 91.077287, 38.518241, 10.642836, 3.942491, 0.798094, 22.276056, 8.860588, 0.199579, 27.601038, 12.267493, 10.150265, 6.144562, 4.553009, 5.447502, 2.009245, 9.118773, 43.997828, 40.448191, 20.378239, 42.292929, 1.133066, 9.031088, 7.554661, 19.314747, 23.174294, 38.13964, 65.068149, 5.701579, 1.056608, 10.276158, 71.158647, 29.170398, 60.776238, 301.139947, 3.447496, 26.084662, 85.262356, 4.018332, 22.211743, 11.746035, 12.311143]
plt.scatter(gdp_cap, life_exp)
plt.xscale('log')

#print(gdp_cap)
# Strings
xlab = 'GDP per Capita [in USD]'
ylab = 'Life Expectancy [in years]'
title = 'World Development in 2007'

# Add axis labels

plt.xlabel(xlab)
plt.ylabel(ylab)
# Add title
plt.title(title)

# After customizing, display the plot
#plt.show()

## NEW CODE TO DISPLAY DIFFERENT TICK MARKS

# Scatter plot
plt.scatter(gdp_cap, life_exp)

# Previous customizations
plt.xscale('log')
plt.xlabel('GDP per Capita [in USD]')
plt.ylabel('Life Expectancy [in years]')
plt.title('World Development in 2007')

# Definition of tick_val and tick_lab
tick_val = [1000, 10000, 100000]
tick_lab = ['1k', '10k', '100k']

# Adapt the ticks on the x-axis
plt.xticks(tick_val,tick_lab)

# After customizing, display the plot
#plt.show()

##################################################
# NOW DISPLAY DATA WITH DOT THE SIZE OF POPULATION
# POP IS DOUBLED TO MAKE THE DOTS BIGGER
##################################################

# Import numpy as np
import numpy as np

# Store pop as a numpy array: np_pop
np_pop=np.array(pop)

# Double np_pop
np_pop=np_pop*2

# Update: set s argument to np_pop
plt.scatter(gdp_cap, life_exp, s = np_pop,c=col,alpha=0.8)

# Previous customizations
plt.xscale('log')
plt.xlabel('GDP per Capita [in USD]')
plt.ylabel('Life Expectancy [in years]')
plt.title('World Development in 2007')
plt.xticks([1000, 10000, 100000],['1k', '10k', '100k'])
plt.text(1550, 71, 'India')   # add text on graph at particular points
plt.text(5700, 80, 'China')
plt.grid(True)   # show grid lines

# Display the plot
#plt.show()