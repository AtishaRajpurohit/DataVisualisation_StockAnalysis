import pandas as pd
import pandas as pdr
import yfinance as yf
import pandas.api.types
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
import time
from tqdm import tqdm
import plotly.io as pio
import yfinance as yf
from datetime import date
pd.options.mode.chained_assignment = None
pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", lambda x: "%.3f" % x)
pd.options.mode.chained_assignment = None


# data = yf.download(  # or pdr.get_data_yahoo(...
#         # tickers list or string as well
#         tickers = "AET" ,period = "1d", group_by = 'ticker',threads = True,
#         proxy = None)
#
#
# data["Adj Close"]


companies = pd.read_csv("data/Geolocations.csv")


ticks = companies["Ticker symbol"].tolist()
strlist = ' '.join(ticks)


list =[]
companies["stock_price"] = None
for i in companies["Ticker symbol"]:
    stock = yf.download(
        tickers = i ,period = "1d", group_by = 'ticker',threads = True,
        proxy = None)
    if pandas.api.types.is_numeric_dtype(stock["Adj Close"]):
        list.append(stock["Adj Close"])
    else:
        list.append("Not Available")


for i in range(len(list)):
    try:
        companies["stock_price"][i] = float("{:.2f}".format(list[i][0]))
    except:
        companies["stock_price"][i] = 0


df = companies



df = df[df["stock_price"] != 0]
df["stock_price"] = df["stock_price"].astype(str)

# df= df[~df['stock_price'].notnull()]
# notnullhq_by_count = ["State"].value_counts()
# hq_by_count = pd.DataFrame(hq_by_count)


# Creating text column. In the graph, when you hover over a point, the following is the information
# Displayed. So if you want different set of info to be displayed, you can do so
# By making changes to the right hand side below.
df["text"] = "Company name:" + df["Security"] + "; " \
             + "Ticker:       " + df["Ticker symbol"] + "; "\
             + "\n stock price:     $" +  df["stock_price"]
# df_g = df.groupby(["GICS Sector", "State"])["Ticker symbol"].agg('count').reset_index()




sectors=df['GICS Sector'].unique()
token = "pk.eyJ1IjoibWF0ZW5leiIsImEiOiJjbDF2MjlvZjAwMmJmM2JwZjJjZXhpOTZrIn0.7KHqy0R5NXB4SGJ9Ywk8xg"

# token = "pk.eyJ1IjoibWF0ZW5leiIsImEiOiJjbDF2MjlvZjAwMmJmM2JwZjJjZXhpOTZrIn0.7KHqy0R5NXB4SGJ9Ywk8xg"

fig = px.scatter_mapbox(df,
                        lat = df["lat"],
                        lon = df["lon"],
                        color = df["GICS Sector"], # which column to use to set the color of markers
                        hover_name = df["text"],
                        size = pd.to_numeric(df["stock_price"]),# column added to hover informatio
                        color_discrete_map={sectors[0]: '#00FFFF',  # Aqua,  industrials
                                            sectors[1]: '#000000',  # Black, Health Care
                                            sectors[2]: '#8B008B', # Dark Magenta, Information Technology
                                            sectors[3]: '#4608F0',  # Navy,  Consumer Discretionary
                                            sectors[4]: '#FF69B4',  # Hot pink , Utilities
                                            sectors[5]: '#FA8072',  # Salmon, Financials
                                            sectors[6]: '#7FFF00',  # chartreuse,   Materials
                                            sectors[7]: '#FF0000',  # Red , Consumer Staples
                                            sectors[8]: '#228B22',  # Forest Green, Real Estate
                                            sectors[9]: '#FFD700',  # Gold, Energy
                                            sectors[10]: '#1E90FF', # Dodger blue, Telecommunication Services
                                            }



                     )
fig.update_layout(
    title = 'Headquarters per Industry by State',
    geo_scope='world')

fig.update_layout(
    paper_bgcolor='#fceee4', mapbox_style = "dark", mapbox_accesstoken=token)

fig.add_scattergeo(
    locations=df['state_abv'],    ###codes for states,
    locationmode='USA-states',
    text=df['state_abv'],
    mode = "text")


fig.show()
##
#Write html plot.
fig.write_html("Headquarters_plotly.html")








