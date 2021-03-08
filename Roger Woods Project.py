# Basic scatter plot, log scale
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
#from pyproj import Proj, transform
from pyproj import Transformer
#import pycurl



import requests
#url = 'https://api.open-elevation.com/api/v1/lookup\?locations\=10,10\|20,20\|41.161758,-8.583933'
# doesnt seem to work
#url='https://api.open-elevation.com/api/v1/lookup?locations=41.161758,-8.583933'

# this works. Max 100 locations per request, 1 call per second, 1000 calls per day
url='https://api.opentopodata.org/v1/eudem25m?locations=53.100736,-6.408332|53.200736,-6.508332'

# elevation api website. Free for a 5km grid hence maybe not that good to use
#url='https://elevation-api.io/api/elevation?points=(53.100736,-6.408332),(62.52417,10.02487)&key=mc9Y4kCAoU88ol677jb0gAA-u9O7DP'

r = requests.get(url)
#r=requests.post(url)
print(r.text)    # prints out the text that has been returned
json_data = r.json()
for key, value in json_data.items():
    print(key + ':', value)

df=pd.json_normalize(json_data)
print(df.columns)
print(df)

print(df)
