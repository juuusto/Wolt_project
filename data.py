import pandas as pd
import numpy as np
import geopy as gp
import json
from geopy.geocoders import Nominatim
from dateutil import parser


#read data from csv and transform it to numpy
df_loc = pd.read_csv("locations.csv")
df_time = pd.read_csv("pickup_times.csv")
data_loc = df_loc.values
data_time = df_time.values

#returns town based oparser
def get_town(lat, long):
    geolocator = Nominatim(user_agent="latickup")
    location = geolocator.reverse(str(long) + ","+ str(lat))
    r = json.dumps(location.raw)
    loaded = json.loads(r)
    return loaded["address"]["city"]

#returns data based on city 
def sort_by_city(city,data):
    n = len(data)
    return_data = []
    for i in range(n):
        if get_town(data[i][1],data[i][2]) == city:
            return_data.append(data[i][0])
    return np.array(return_data)

#returns pickup times for wanted stores
def get_store_pickuptime(storeId,data):
    n = len(data)
    return_data = []
    for i in range(n):
        if data[i][0] in storeId:
            return_data.append(data[i])
    return return_data

#parse data value date
def parse_date(data):
    date = parser.parse(data[1])
    return  date.date()

#parse data value time
def parse_time(data):
    time = parser.parse(data[1])
    return time.time()
#filter data with given date        
def filter_data_with_date(data,date):
    n = len(data)
    return_data = []
    for i in range(n):
        if date == parse_date(data[i]).strftime('%Y-%m-%d'):
            return_data.append(data[i])
    return np.array(return_data)

#filter data with given timeframe
def filter_data_with_time(data,start,end):
    n = len(data)
    return_data =[]
    for i in range(n):
        if start <= parse_time(data[i]).strftime('%X') and end >= parse_time(data[i]).strftime('%X'):
            return_data.append(data[i])
    return np.array(return_data)
print(len(filter_data_with_time(filter_data_with_date(get_store_pickuptime(sort_by_city("Helsinki",data_loc),data_time),"2019-01-13"),"19","20")))
