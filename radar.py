# importing libraries
import numpy as np
import pandas as pd
import plotly.graph_objects as px
import plotly.graph_objs as go

# loading data
ratios = pd.read_csv('data/ratios.csv')
sec = pd.read_csv('data/securities.csv')

# keeping the most recent data
ratios = ratios.sort_values(by=['ticker_symbol','Period Ending'], ascending=False)
ratios = ratios.drop_duplicates(subset=['ticker_symbol'])
ratios = ratios.sort_values(by=['ticker_symbol'], ascending=True)

# merge the two data sets
df = sec.merge(ratios, left_on='Ticker symbol', right_on='Ticker Symbol')

# keeping only columns needed and merge
df=df[['GICS Sector','current_ratio','leverage','asset_utilisation','price_earnings_ratio','After Tax ROE']]
df = df.groupby('GICS Sector', as_index=False).mean()

# scaling all columns to 0-5
df['current_ratio'] = df['current_ratio']*2.275161580784258
df['leverage'] = (df['leverage']+16.06506136494)*0.267614868316362
df['asset_utilisation'] = df['asset_utilisation']*4.713975172214691
df['price_earnings_ratio'] = df['price_earnings_ratio']*0.12346036720176107
df['After Tax ROE'] = df['After Tax ROE']*0.05541651769753308

categories = ['Current Ratio','Leverage','Asset Utilisation','Price Earnings Ratio','After Tax ROE']

fig = go.Figure()
fig.add_trace(go.Scatterpolar(
      fillcolor='#4608F0',
      line=dict(color='#4608F0'),
      opacity = 0.4,
      r=[4.155571,0.000000,4.385128,4.250070,2.013836],
      theta=categories,
      fill='toself',
      name='Consumer Discretionary'
))
fig.add_trace(go.Scatterpolar(
      fillcolor='#FF0000',
      line=dict(color='#FF0000'),
      opacity = 0.4,
      r=[3.965634,3.718332,5.000000,3.217182,4.861540],
      theta=categories,
      fill='toself',
      name='Consumer Staples'
))
fig.add_trace(go.Scatterpolar(
      fillcolor='#FFD700',
      line=dict(color='#FFD700'),
      opacity = 0.4,
      r=[4.116339,4.822923,2.513989,1.125826,5.000000],
      theta=categories,
      fill='toself',
      name='Energy'
))
fig.add_trace(go.Scatterpolar(
      fillcolor='#FA8072',
      line=dict(color='#FA8072'),
      opacity = 0.4,
      r=[2.803410,4.519699,1.040736,2.004810,1.430172],
      theta=categories,
      fill='toself',
      name='Financials'
))
fig.add_trace(go.Scatterpolar(
      fillcolor='#000000',
      line=dict(color='#000000'),
      opacity = 0.4,
      r=[4.155180,4.466472,4.407921,4.296940,1.574860],
      theta=categories,
      fill='toself',
      name='Health Care'
))
fig.add_trace(go.Scatterpolar(
      fillcolor='#0000FF',
      line=dict(color='#0000FF'),
      opacity = 0.4,
      r=[3.662310,4.729524,4.570950,2.219994,2.654542],
      theta=categories,
      fill='toself',
      name='Industrials'
))
fig.add_trace(go.Scatterpolar(
      fillcolor='#8B008B',
      line=dict(color='#8B008B'),
      opacity = 0.4,
      r=[5.000000,4.763968,2.793360,3.688753,1.508686],
      theta=categories,
      fill='toself',
      name='Information Technology'
))
fig.add_trace(go.Scatterpolar(
      fillcolor='#7FFF00',
      line=dict(color='#7FFF00'),
      opacity = 0.4,
      r=[3.671853,4.746126,3.456939,2.812332,1.662496],
      theta=categories,
      fill='toself',
      name='Materials'
))
fig.add_trace(go.Scatterpolar(
      fillcolor='#228B22',
      line=dict(color='#228B22'),
      opacity = 0.4,
      r=[3.784197,4.784654,0.970193,5.000000,0.689628],
      theta=categories,
      fill='toself',
      name='Real Estate'
))
fig.add_trace(go.Scatterpolar(
      fillcolor='#1E90FF',
      line=dict(color='#1E90FF'),
      opacity = 0.4,
      r=[3.145653,5.000000,1.720879,0.752873,1.806578],
      theta=categories,
      fill='toself',
      name='Telecommunications Services'
))
fig.add_trace(go.Scatterpolar(
      fillcolor='#FF69B4',
      line=dict(color='#FF69B4'),
      opacity = 0.4,
      r=[3.142892,4.665946,1.186077,1.668244,0.547238],
      theta=categories,
      fill='toself',
      name='Utilities'
))



  
# Add dropdown
fig.update_layout(
    paper_bgcolor = '#fceee4', plot_bgcolor = '#fceee4', 
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(label="All Sectors",
                     method="update",
                     args=[{"visible": [True, True, True, True, True, True, True, True, True, True, True]},
                           {"title": "All Sectors"}]),
                dict(label="Consumer Discretionary",
                     method="update",
                     args=[{"visible": [True, False, False, False, False, False, False, False, False, False, False]},
                           {"title": "Consumer Discretionary",
                            }]),
                dict(label="Consumer Staples",
                     method="update",
                     args=[{"visible": [False, True, False, False, False, False, False, False, False, False, False]},
                           {"title": "Consumer Staples",
                            }]),
                dict(label="Energy",
                     method="update",
                     args=[{"visible": [False, False, True, False, False, False, False, False, False, False, False]},
                           {"title": "Energy",
                            }]),
                dict(label="Financials",
                     method="update",
                     args=[{"visible": [False, False, False, True, False, False, False, False, False, False, False]},
                           {"title": "Financials",
                            }]),
                dict(label="Health Care",
                     method="update",
                     args=[{"visible": [False, False, False, False, True, False, False, False, False, False, False]},
                           {"title": "Health Care",
                            }]),
                dict(label="Industrials",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, True, False, False, False, False, False]},
                           {"title": "Industrials",
                            }]),
                dict(label="Information Technology",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, True, False, False, False, False]},
                           {"title": "Information Technology",
                            }]),
                dict(label="Materials",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, False, True, False, False, False]},
                           {"title": "Materials",
                            }]),
                dict(label="Real Estate",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, False, False, True, False, False]},
                           {"title": "Real Estate",
                            }]),
                dict(label="Telecommunications Services",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, False, False, False, True, False]},
                           {"title": "Telecommunications Services",
                            }]),
                dict(label="Utilities",
                     method="update",
                     args=[{"visible": [False, False, False, False, False, False, False, False, False, False, True]},
                           {"title": "Utilities",
                            }]),
            ]),
        ),
    ])

fig.write_html("radar.html")
