import pandas_datareader as pdr # access fred
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, writers
import numpy as np
from datetime import datetime
from fredapi import Fred as fred

#### boilerplate code for absolute imports #####
import sys
from pathlib import Path 
file = Path(__file__).resolve().parents
root = file[1]
sys.path.append(str(root))
from keyCollection import FRED_API_KEY
#################################################

#### Variables ####
fred = fred(api_key=FRED_API_KEY())
startDate = '2012-01-01'
endDate = datetime.today().strftime('%Y-%m-%d')
sourceData = 'fred'
series = 'QKRR628BIS' 
#################################################

def get_fred_data(param_list, start_date, end_date = endDate):
  df = pdr.DataReader(param_list, sourceData, start_date, end_date)
  return df.reset_index()

def animate(i):
    x.append(x_data[i])
    y.append(y_data[i])
    plt.plot(x, y, scaley=True, scalex=True, color="navy")
  
def fredMetaData(series, arg = "title"):
  info = fred.get_series_info(series)
  return info[arg]

# get data for series
df = get_fred_data(param_list=[series], 
                   start_date=startDate)


x_data = df['DATE'].to_list()
y_data = df[series].to_list()
x,y=[], []

fig = plt.figure(figsize=(16, 9), dpi=1920/16)  #300
ax = plt.gca()  # Get current axes
fig.set_facecolor('green')
ax.set_facecolor('green')

ax.set_ylim(min(y_data) * 0.95, max(y_data) * 1.1)
ax.set_xlim(min(x_data), max(x_data))
ax.tick_params(axis='both', which='major', labelsize=15)


fontName = 'Montserrat'

plt.title(label = fredMetaData(series),
          fontsize=30,
          font= fontName,
          color="black")
plt.grid(visible=True, c='gray')
annotation = 'Created by @daeminsong using ' + sourceData.capitalize() + ' data'
plt.figtext(0.9, 0.05, annotation, horizontalalignment='right', font = fontName)

animation = FuncAnimation(fig=fig, func=animate, frames= np.arange(0, len(x_data), 1), interval=30)

# plt.show()

# setting up wrtiers object
Writer = writers['ffmpeg']
writer = Writer(fps=30, metadata={'artist': 'Daemin Song'}, bitrate=20000000)
animation.save(str(file[0]) + 'Line Graph Animation.mp4', writer)
