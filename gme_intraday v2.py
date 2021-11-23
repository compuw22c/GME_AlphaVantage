#!/usr/bin/env python
# coding: utf-8

# In[1]:

import os
from datetime import datetime
import pandas as pd
from pandas_datareader import data as web
import plotly.graph_objects as go


# In[29]:


stock = 'GME'
interval = '15min'
#This should actually be '1' to be THIS month (you're adding 1 to the actual number)
monthsago = 11
#This should actually be '1' to be THIS year (you're adding 1 to the actual number)
yearsago = 1
trim_beginning = 300  #How many lines to trim off the CSV for performance
trim_ending = 700
api_key = 'YOUR_API_KEY'

adjusted = '&adjusted=false&'

csv_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol='+stock+'&interval='+interval+'&slice=year'+str(yearsago)+'month'+str(monthsago)+adjusted+'&apikey='+api_key
csv_url2 = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol='+stock+'&interval='+interval+'&slice=year'+str(yearsago)+'month'+str(monthsago-1)+adjusted+'&apikey='+api_key

df1 = pd.read_csv(csv_url)
#TrimBeginning (yes it's contradictory)
df1.drop(df1.tail(trim_beginning).index,inplace=True)
#df1.to_csv('test1.csv')  #ForDebugging
df2 = pd.read_csv(csv_url2)
#TrimEnding
df2.drop(df2.head(trim_ending).index,inplace=True)
#df2.to_csv('test2.csv')  #ForDebugging


df = df1.append(df2, sort=False)
#df.to_csv('testmerge.csv')  #ForDebugging

# In[35]:


trace1 = {
    'x': df.time,
    'open': df.open,
    'close': df.close,
    'high': df.high,
    'low': df.low,
    'type': 'candlestick',
    'name': 'GME',
    'showlegend': False
}


# In[24]:


# Calculate and define moving average of 30 periods
avg_30 = df.close.rolling(window=30, min_periods=1).mean()

# Calculate and define moving average of 50 periods
avg_50 = df.close.rolling(window=50, min_periods=1).mean()


# In[25]:


trace2 = {
    'x': df.time,
    'y': avg_30,
    'type': 'scatter',
    'mode': 'lines',
    'line': {
        'width': 1,
        'color': 'blue'
            },
    'name': 'Moving Average of 30 periods'
}


# In[34]:


# In[26]:


trace3 = {
    'x': df.time,
    'y': avg_50,
    'type': 'scatter',
    'mode': 'lines',
    'line': {
        'width': 1,
        'color': 'red'
    },
    'name': 'Moving Average of 50 periods'
}


# In[37]:


data = [trace1, trace2, trace3]


updatemenus = list([
    dict(active=1,
         buttons=list([
            dict(label='Log Scale',
                 method='update',
                 args=[{'visible': [True, True]},
                       {'title': 'Log scale',
                        'yaxis': {'type': 'log'}}]),
            dict(label='Linear Scale',
                 method='update',
                 args=[{'visible': [True, False]},
                       {'title': 'Linear scale',
                        'yaxis': {'type': 'linear'}}])
            ]),
        )
    ])

layout = dict(updatemenus=updatemenus, title='Linear scale')


# Config graph layout
##layout = go.Layout({
##    'title': {
##        'text': 'GME Moving Averages',
##        'font': {
##            'size': 15
##        }
##    }
##})


# In[38]:


fig = go.Figure(data=data, layout=layout)
##fig.update_xaxes(
##    rangebreaks=[
##        dict(bounds=["sat", "sun"]), #hide weekends
##    ]
##)
fig.write_html("GME Moving Averages.html")
fig.show()


# In[ ]:




