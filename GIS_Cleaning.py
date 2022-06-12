import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.tools as tls
import plotly
import plotly.express as px
import seaborn as sns
from IPython.core.display import display
import glob
import re
from isort.profiles import black
from datetime import datetime
import os
import itertools
import seaborn as sns
from pandas.api.types import is_numeric_dtype
import plotly.graph_objects as go
import geopandas as gpd
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from geopy.geocoders import Nominatim
from opencage.geocoder import OpenCageGeocode
import time
from tqdm import tqdm
pd.options.mode.chained_assignment = None
pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", lambda x: "%.3f" % x)

## Cleaning data
df = pd.read_csv("data/securities.csv")


# df.info()
# Good.

# Subset necessary columns for our purpose
df_sub = df.iloc[:,[0,1,3,5]]

# Create seperate columns for city and state
city_state = df_sub['Address of Headquarters'].str.split(',', n=1, expand=True)
df_sub["City"] = city_state[0]
df_sub["State"] = city_state[1]


# Strip whitespace from state
df_sub["State"] =  df_sub['State'].str.strip()




# keep U.S. based companies
df_sub = df_sub.loc[(df_sub['State'] != "UnitedKingdom" ) &
            (df_sub['State'] != "Ireland") &
            (df_sub['State'] != "Switzerland")  &
            (df_sub['State'] != "Kent, United Kingdom") &
            (df_sub['State'] != "Netherlands") &
            (df_sub['State'] != "Kingdom of the Netherlands") &
            (df_sub['State'] != "UK") &
            (df_sub['State'] != "United Kingdom") &
            (df_sub['State'] != "Bermuda")
            ]

# Some values have [number] infront of them. lets clean them
df_sub['State'] = df_sub['State'].map(lambda x: re.sub(r'[^a-zA-Z]*','',x))


# Cleaning for homogeneity
df_sub["State"] = df_sub["State"].replace(to_replace= 'NewYork', value='New York', regex=True)
df_sub["State"] = df_sub["State"].replace(to_replace= 'NY', value='New York', regex=True)
df_sub["State"] = df_sub["State"].replace(to_replace= 'NewJersey', value='New Jersey', regex=True)
df_sub["State"] = df_sub["State"].replace(to_replace= 'DC', value='District of Columbia', regex=True)
df_sub["State"] = df_sub["State"].replace(to_replace= 'UT', value='Utah', regex=True)
df_sub["State"] = df_sub["State"].replace(to_replace= 'RhodeIsland', value='Rhode Island', regex=True)
df_sub["State"] = df_sub["State"].replace(to_replace= 'SouthCarolina', value='South Carolina', regex=True)
df_sub["State"] = df_sub["State"].replace(to_replace= 'NorthCarolina', value='North Carolina', regex=True)


# Define state abbrev dictionary to map it to Two letter attributes
us_state_to_abbrev = {
"Alabama": "AL",
"Alaska": "AK",
"Arizona": "AZ",
"Arkansas": "AR",
"California": "CA",
"Colorado": "CO",
"Connecticut": "CT",
"Delaware": "DE",
"Florida": "FL",
"Georgia": "GA",
"Hawaii": "HI",
"Idaho": "ID",
"Illinois": "IL",
"Indiana": "IN",
"Iowa": "IA",
"Kansas": "KS",
"Kentucky": "KY",
"Louisiana": "LA",
"Maine": "ME",
"Maryland": "MD",
"Massachusetts": "MA",
"Michigan": "MI",
"Minnesota": "MN",
"Mississippi": "MS",
"Missouri": "MO",
"Montana": "MT",
"Nebraska": "NE",
"Nevada": "NV",
"New Hampshire": "NH",
"New Jersey": "NJ",
"New Mexico": "NM",
"New York": "NY",
"North Carolina": "NC",
"North Dakota": "ND",
"Ohio": "OH",
"Oklahoma": "OK",
"Oregon": "OR",
"Pennsylvania": "PA",
"Rhode Island": "RI",
"South Carolina": "SC",
"South Dakota": "SD",
"Tennessee": "TN",
"Texas": "TX",
"Utah": "UT",
"Vermont": "VT",
"Virginia": "VA",
"Washington": "WA",
"West Virginia": "WV",
"Wisconsin": "WI",
"Wyoming": "WY",
"District of Columbia": "DC",
"American Samoa": "AS",
"Guam": "GU",
"Northern Mariana Islands": "MP",
"Puerto Rico": "PR",
"United States Minor Outlying Islands": "UM",
"U.S. Virgin Islands": "VI",
}


# Map full state name to abbreviations, Creating new column which holds abv
df_sub['state_abv']= df_sub['State'].map(us_state_to_abbrev)








###GEOCODING,
# We have the city and state, but we need the longitude and latitude. Will use the following API to get the longitude latitude for each city state
# as a list.
key = '0a035f89398f4b1bbea71a0e9611ee31'
geocoder = OpenCageGeocode(key)
list_lat = []  # create empty lists
list_long = []

for index, row in df_sub.iterrows():  # iterate over rows in dataframe

    City = row['City']
    State = row['State']
    query = str(City) + ',' + str(State)

    results = geocoder.geocode(query)
    lat = results[0]['geometry']['lat']
    long = results[0]['geometry']['lng']

    list_lat.append(lat)
    list_long.append(long)

# create new columns from lists

df_sub['lat'] = list_lat

df_sub['lon'] = list_long

print("Finished process")

# Write output file.
df_sub.to_csv("data/Geolocations.csv", index=False)








