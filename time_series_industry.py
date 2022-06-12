#!/usr/bin/env python
# coding: utf-8

from pydoc import describe
import chart_studio
import chart_studio.plotly as py
import plotly.graph_objects as go  # has more control, customizable
import plotly.io as pio  # produce an html file
import plotly.express as px  # fast, low effort
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


import os

# os.chdir("/Users/jackpiccione/Google Drive/")


sec = pd.read_csv("data/securities.csv")


sec.head()


prices = pd.read_csv("data/prices-split-adjusted.csv")


prices.head()


# join dataframe on stock
df = sec.merge(prices, left_on="Ticker symbol", right_on="symbol")


df.head()


df.close.max()


# 11 different industries
len(df["GICS Sector"].unique())


# convert to datetime
df["date"] = pd.to_datetime(df["date"])


# list of industries
df["GICS Sector"].unique()


# save industries as list
sectors = [
    "Industrials",
    "Health Care",
    "Information Technology",
    "Consumer Discretionary",
    "Utilities",
    "Financials",
    "Materials",
    "Consumer Staples",
    "Real Estate",
    "Energy",
    "Telecommunications Services",
]


dataframes_list = []
# create dataframe for each industry
def cleanSector(sector):
    # select industry
    sector = df[df["GICS Sector"] == sector]
    # create new variable that sums stock price for each day for each industry
    sector["close_sum"] = (
        sector["close"].groupby(sector["date"]).transform(lambda x: x.sum())
    )
    # sector["pct"] = sector["close_sum"].pct_change()
    # sector.dropna(inplace=True)
    # only keep 2 cols
    sector = sector[["date", "close_sum"]]

    sector = sector.set_index(sector.date)

    sector.drop_duplicates(inplace=True)
    sector.drop_duplicates(subset=["date"], inplace=True)
    sector.dropna(inplace=True)
    # sector.drop(sector.tail(1).index,inplace=True)
    # add dataframe to a list of dataframes
    dataframes_list.append(sector)


# run sector function for every industry (11)
for i in range(len(sectors)):
    cleanSector(sectors[i])


# scale every stock by 100
for i in range(len(sectors)):
    scalar = 100 / dataframes_list[i].close_sum[0]
    dataframes_list[i].close_sum = dataframes_list[i].close_sum * scalar


# create plot
fig = go.Figure(
    [
        go.Line(
            x=dataframes_list[0]["date"],
            y=dataframes_list[0]["close_sum"],
            opacity=1,
            name="Industrials",
            marker_color="#00FFFF",
        )
    ]
)
fig.add_trace(
    go.Line(
        x=dataframes_list[1]["date"],
        y=dataframes_list[1]["close_sum"],
        opacity=1,
        name="Health Care",
        marker_color="#000000",
    )
)
fig.add_trace(
    go.Line(
        x=dataframes_list[2]["date"],
        y=dataframes_list[2]["close_sum"],
        opacity=1,
        name="Information Technology",
        marker_color="#8B008B",
    )
)
fig.add_trace(
    go.Line(
        x=dataframes_list[3]["date"],
        y=dataframes_list[3]["close_sum"],
        opacity=1,
        name="Consumer Discretionary",
        marker_color="#4608F0",
    )
)
fig.add_trace(
    go.Line(
        x=dataframes_list[4]["date"],
        y=dataframes_list[4]["close_sum"],
        opacity=1,
        name="Utilities",
        marker_color="#FF69B4",
    )
)
fig.add_trace(
    go.Line(
        x=dataframes_list[5]["date"],
        y=dataframes_list[5]["close_sum"],
        opacity=1,
        name="Financials",
        marker_color="#FA8072",
    )
)
fig.add_trace(
    go.Line(
        x=dataframes_list[6]["date"],
        y=dataframes_list[6]["close_sum"],
        opacity=1,
        name="Materials",
        marker_color="#7FFF00",
    )
)
fig.add_trace(
    go.Line(
        x=dataframes_list[7]["date"],
        y=dataframes_list[7]["close_sum"],
        opacity=1,
        name="Consumer Staples",
        marker_color="#FF0000",
    )
)
fig.add_trace(
    go.Line(
        x=dataframes_list[8]["date"],
        y=dataframes_list[8]["close_sum"],
        opacity=1,
        name="Real Estate",
        marker_color="#228B22",
    )
)
fig.add_trace(
    go.Line(
        x=dataframes_list[9]["date"],
        y=dataframes_list[9]["close_sum"],
        opacity=1,
        name="Energy",
        marker_color="#FFD700",
    )
)
fig.add_trace(
    go.Line(
        x=dataframes_list[10]["date"],
        y=dataframes_list[10]["close_sum"],
        opacity=1,
        name="Telecommunications Services",
        marker_color="#1E90FF",
    )
)
# create legend
fig.update_layout(
    title="How much money would you make in each sector if you invested 100 dollars?",
    yaxis_title="Ticker Returns ($)",
    xaxis_title="Time",
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
fig.update_layout(
    legend_title_text="GICS Sector", paper_bgcolor="#fceee4", plot_bgcolor="#fceee4"
)  # add title to legend
pio.write_html(fig, file="sectorViz.html", auto_open=True)
fig.show()


# get_ipython().system('jupyter nbconvert --no-prompt --to script time_series_industry.ipynb')