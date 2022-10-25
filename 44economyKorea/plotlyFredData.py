import pandas_datareader as pdr # access fred
import pandas as pd
import requests # data from api
import plotly.express as px # visualize
import plotly.graph_objects as go
from datetime import datetime

#### boilerplate code for absolute imports #####
import sys
from pathlib import Path 
file = Path(__file__).resolve().parents
root = file[1]
sys.path.append(str(root))
from keyCollection import FRED_API_KEY
#################################################


def get_fred_data(param_list, start_date, end_date):
  df = pdr.DataReader(param_list, 'fred', start_date, end_date)
  return df.reset_index()

fred_api_key = FRED_API_KEY()

series = 'CABPPRIVSA' 
# get data for series
df = get_fred_data(param_list=[series], 
                   start_date='2018-01-01', 
                   end_date='2021-08-01')

print(df)
# Base plot
fig = go.Figure(
    layout=go.Layout(
        updatemenus=[dict(type="buttons", direction="right", x=0.9, y=1.16), ],
        xaxis=dict(range=["2018-01-01", "2021-08-01"],
                   autorange=False, tickwidth=2,
                   title_text="Time"),
        yaxis=dict(range=[0, 20000],
                   autorange=False,
                   title_text="Price"),
        title="Gold - Bitcoin prices evolution",
    ))

# Add traces
init = 1

fig.add_trace(
    go.Scatter(x=df.DATE[:init],
               y=df.CABPPRIVSA[:init],
               name="Gold",
               visible=True,
               line=dict(color="#33CFA5", dash="dash")))

fig.add_trace(
    go.Scatter(x=df.DATE[:init],
               y=df.CABPPRIVSA[:init],
               name="Bitcoin",
               visible=True,
               line=dict(color="#bf00ff", dash="dash")))

# Animation
fig.update(frames=[
    go.Frame(
        data=[
            go.Scatter(x=df.DATE[:k], y=df.CABPPRIVSA[:k]),
            go.Scatter(x=df.DATE[:k], y=df.CABPPRIVSA[:k])]
    )
    for k in range(init, len(df)+1)])

# Extra Formatting
fig.update_xaxes(ticks="outside", tickwidth=2, tickcolor='white', ticklen=10)
fig.update_yaxes(ticks="outside", tickwidth=2, tickcolor='white', ticklen=1)
fig.update_layout(yaxis_tickformat=',')
fig.update_layout(legend=dict(x=0, y=1.1), legend_orientation="h")

# Buttons
fig.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(label="Play",
                        method="animate",
                    args=[None, {"frame": {"duration": 1000}}]),
                dict(label="Gold",
                    method="update",
                    args=[{"visible": [False, True]},
                          {"showlegend": True}]),
                dict(label="Bitcoin",
                    method="update",
                    args=[{"visible": [True, False]},
                          {"showlegend": True}]),
                dict(label="All",
                    method="update",
                    args=[{"visible": [True, True, True]},
                          {"showlegend": True}]),
            ]))])

fig.show()
