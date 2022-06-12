#%%
from pydoc import describe
import heapq
import chart_studio
import chart_studio.plotly as py
import plotly.graph_objects as go #has more control, customizable
import plotly.io as pio #produce an html file
import plotly.express as px #fast, low effort
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

    
sec = pd.read_csv("./data/securities.csv")
prices = pd.read_csv("./data/prices-split-adjusted.csv")

#join dataframe on stock  
df =  sec.merge(prices, left_on='Ticker symbol', right_on='symbol')

#11 different industries
len(df["GICS Sector"].unique())

#convert to datetime 
df["date"] = pd.to_datetime(df["date"])

#list of industries 
df['GICS Sector'].unique()

#save industries as list
sectors=['Industrials', 'Health Care', 'Information Technology',
       'Consumer Discretionary', 'Utilities', 'Financials', 'Materials',
       'Consumer Staples', 'Real Estate', 'Energy',
       'Telecommunications Services']

df_list = []
fullDF = pd.DataFrame()

def cleanSector(sector,fullDF):
    #initialize sectorDF
    cleanSector = pd.DataFrame()
    sectorDF = df[df['GICS Sector'] == sector]
    
    #build up sectorDF from each ticker in the industry
    for ticker in sectorDF['Ticker symbol'].unique():
        #intialize tickerDF
        tickerDF = sectorDF[sectorDF['Ticker symbol'] == ticker]
        #filter out tickers with missing dates
        if len(tickerDF['date'].unique()) != 1762:
            continue

        #create scalar and add scalarClose to the tickerDF
        scalar = 100/tickerDF['close'].iloc[0]
        tickerDF['scalarClose'] = scalar * tickerDF['close']
        tickerDF['totalClose'] = tickerDF['scalarClose'].iloc[-1]

        #append tickerDF to sectorDF
        if(cleanSector.shape[0] == 0):
            cleanSector = tickerDF
        else:
            cleanSector = cleanSector.append(tickerDF)

        #append tickerDF to fullDF (with all sectors)
        if(fullDF.shape[0] == 0):
            fullDF = tickerDF
        else:
            fullDF = fullDF.append(tickerDF)

    #work to organize tickers by highest returns
    groupdf = cleanSector.groupby(['Ticker symbol']).sum()
    groupdf = groupdf.sort_values(by = ['totalClose'], ascending = False, inplace = False)
    cleanSector['position'] = 0
    groupdf = groupdf.reset_index(inplace = False)
    df_list.append(cleanSector)

    #write to sectorData directory as the code runs (avoid crashes)
    file_path = './sectorData/'+sector+'.csv'
    cleanSector.to_csv(file_path)

#clean all sectors
for sector in sectors:
    cleanSector(sector,fullDF)

#%%
import pandas as pd

#save industries as list
sectors=['Industrials', 'Health Care', 'Information Technology',
       'Consumer Discretionary', 'Utilities', 'Financials', 'Materials',
       'Consumer Staples', 'Real Estate', 'Energy',
       'Telecommunications Services']

def cleanSector(sector, topN = 5):
    filepath = './sectorData/' + sector + '.csv'
    sectorDF = pd.read_csv(filepath)
    groupdf = sectorDF.groupby(['Ticker symbol']).sum()
    groupdf = groupdf.sort_values(by = ['totalClose'], ascending = False, inplace = False)
    groupdf = groupdf.reset_index(inplace = False)

    #let's only take topN tickers from the sector (default topN = 5)
    topTickers = list(groupdf['Ticker symbol'].iloc[:topN])
    topSector = sectorDF[sectorDF['Ticker symbol'].isin(topTickers)]
    topSector = topSector.sort_values(by = ['totalClose'], ascending = False, inplace = False)

    writepath = './sectorData/finalData/' + sector + '.csv'
    topSector.to_csv(writepath)

for sector in sectors:
    cleanSector(sector)

# %%
from pydoc import describe
import heapq
import chart_studio
import chart_studio.plotly as py
import plotly.graph_objects as go #has more control, customizable
import plotly.io as pio #produce an html file
import plotly.express as px #fast, low effort
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#save industries as list
sectors=['Industrials', 'Health Care', 'Information Technology',
       'Consumer Discretionary', 'Utilities', 'Financials', 'Materials',
       'Consumer Staples', 'Real Estate', 'Energy',
       'Telecommunications Services']

dataframes_list = []
fullDF = pd.DataFrame()
#Load data
for sector in sectors:
    filepath = './sectorData/finalData/' + sector + '.csv'
    sectorDF = pd.read_csv(filepath)
    dataframes_list.append(sectorDF)
    fullDF = fullDF.append(sectorDF)  

sortedDF = fullDF.sort_values(by = ['totalClose'], ascending = False, inplace = False)
df = sortedDF

# generate plot

color_list = ['#00FFFF',
              '#000000',
              '#8B008B',
              '#4608F0',
              '#FF69B4',
              '#FA8072',
              '#7FFF00',
              '#FF0000',
              '#228B22',
              '#FFD700',
              '#1E90FF']

fullDF = pd.DataFrame()
for i in range(len(dataframes_list)):
    currentSector = dataframes_list[i]
    currentSector['color'] = color_list[i]
    fullDF = fullDF.append(currentSector)

sortedDF = fullDF.sort_values(by = ['totalClose'], ascending = False, inplace = False)
data = sortedDF

fig = go.Figure()
for i in range(len(dataframes_list)):
    df = dataframes_list[i]
    data = df.groupby(by = ['Ticker symbol']).mean().reset_index(inplace = False)
    data = data.sort_values(by = ['totalClose'], ascending = False, inplace = False)
    data['totalClose'] = data['totalClose'] - 100
    fig.add_trace(go.Bar(x = data['Ticker symbol'],
                         y = data['totalClose'],
                         name = df['GICS Sector'][0],
                         marker_color = color_list[i],
                         width = 0.75)
                )
#create legend
fig.update_layout(
    title="Best Performing Tickers for each GICS Sector (2010 to 2017)", yaxis_title="Ticker Returns in Percentage", xaxis_title="Ticker"
)
fig.update_layout(legend_title_text="GICS Sector")  # add title to legend
fig.update_traces(dict(marker_line_width=0))
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.update_layout(paper_bgcolor = '#fceee4', plot_bgcolor = '#fceee4')
pio.write_html(fig, file="OlivierTickerVizBar_BarChart.html", auto_open=True)
fig.show()

fig = go.Figure()
for i in range(len(dataframes_list)):
    df = dataframes_list[i]
    topTicker = df['Ticker symbol'][0]
    data = df[df['Ticker symbol'] == topTicker]
    data = data.sort_values(by = ['date'], ascending = True, inplace = False)
    fig.add_trace(go.Line(x = data['date'],
                        y = data['scalarClose'],
                        name = topTicker,
                        marker_color = color_list[i])
                )
# create legend
fig.update_layout(
    title="Highest Performing Tickers for each GICS Sector", yaxis_title="Ticker Returns ($)", xaxis_title="Time"
)
# create buttons for timestamps
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=6, label="6 months", step="month", stepmode="backward"),
                    dict(count=1, label="1 year", step="year", stepmode="backward"),
                    dict(count=3, label="3 years", step="year", stepmode="backward"),
                    dict(step="all"),
                ]
            )
        ),
        # create slider
        rangeslider=dict(visible=True),
        type="date",
    )
)
fig.update_layout(legend_title_text="Ticker")  # add title to legend
fig.update_traces(dict(marker_line_width=0))
# fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.update_layout(paper_bgcolor = '#fceee4', plot_bgcolor = '#fceee4')
pio.write_html(fig, file="OlivierTickerViz_LinePlot.html", auto_open=True)
fig.show()

#fceee4

# %%
import pandas as pd


df = pd.read_csv('./sectorData/finalData/Energy.csv')
data = df.groupby(by = ['Ticker symbol']).mean().reset_index(inplace = False)
# %%
