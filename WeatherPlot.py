import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import matplotlib.dates as mdates
from datetime import datetime, time

data = pd.read_csv('Bogor_Weather.csv', parse_dates=['tgl_waktu'])
data.index = pd.to_datetime(data['tgl_waktu'],format='%m%d%Y%H:%M:%S%z')
data['Year']=data.index.year
data['Month']=data.index.month
data['Weekday Name']=data.index.weekday_name
data = data[(data['rain'] <= 3000)]
dates = data.loc[data['tgl_waktu']]
df1 = pd.DataFrame(dates, columns=['temp', 'hum', 'press', 'wd', 'ws', 'rain', 'timrain', 'intrain'])
dfhourly = df1.rain.resample('H').sum()
dfhourly = pd.DataFrame(dfhourly)
dfdaily = dfhourly['rain'].resample('D').sum()
dfdaily = pd.DataFrame(dfdaily)
dfweekly = dfdaily['rain'].resample('W').sum()
dfweekly = pd.DataFrame(dfweekly)
dfmonthly = dfweekly['rain'].resample('M').sum()
dfmonthly = pd.DataFrame(dfmonthly)
start, end = '2016', '2018'
summa = df1.rain.sum()

#rain
sns.set(rc={'figure.figsize':(15,6)})
fig, ax = plt.subplots(figsize = (15, 10))
#range tanggal
ax.plot(df1.loc[start:end, 'rain'], linestyle='-')
ax.set_ylabel('Curah Hujan (mm)')
ax.set_title('CURAH HUJAN 2016-2018')
# Set x-axis major ticks to weekly interval, on Mondays ,bisa dihapus 
ax.xaxis.set_major_locator(mdates.MonthLocator())
# Format x-tick labels as 3-letter month name and day number
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'));

fig, ax = plt.subplots(figsize = (15, 10))
#range tanggal
ax.plot(df1.loc['2018', 'press'], linestyle='-')
ax.set_ylabel('Tekanan Udara (mb)')
ax.set_title('TEKANAN UDARA JANUARI 2018')
# Set x-axis major ticks to weekly interval, on Mondays ,bisa dihapus 
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.SUNDAY))
# Format x-tick labels as 3-letter month name and day number
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'));

fig, ax = plt.subplots(figsize = (15, 10))
#range tanggal
ax.plot(df1.loc['2018', 'hum'], linestyle='-')
ax.set_ylabel('Kelembaban Udara (%)')
ax.set_title('KELEMBABAN UDARA JANUARI 2018')
# Set x-axis major ticks to weekly interval, on Mondays ,bisa dihapus 
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.SUNDAY))
# Format x-tick labels as 3-letter month name and day number
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'));

fig, ax = plt.subplots(figsize = (15, 10))
#range tanggal
ax.plot(df1.loc['2018', 'temp'], linestyle='-')
ax.set_ylabel('Suhu (`C)')
ax.set_title('SUHU UDARA JANUARI 2018')
# Set x-axis major ticks to weekly interval, on Mondays ,bisa dihapus 
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.SUNDAY))
# Format x-tick labels as 3-letter month name and day number
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))

#Buat WindRose
"""
total_count = df1.shape[0]
calm_count = df1.query("ws == 0").shape[0]
print('Of {} total observations, {} have calm winds.'.format(total_count, calm_count))

def speed_labels(bins, units):   
    labels = []
    for left, right in zip(bins[:-1], bins[1:]):
        if left == bins[0]:
            labels.append('calm'.format(right))
        elif np.isinf(right):
            labels.append('>{} {}'.format(left, units))
        else:
            labels.append('{} - {} {}'.format(left, right, units))

    return list(labels)

def _convert_dir(directions, N=None):
    if N is None:
        N = directions.shape[0]
    barDir = directions * np.pi/180. - np.pi/N
    barWidth = 2 * np.pi / N
    return barDir, barWidth

spd_bins = [-1, 0, 5, 10, 15, 20, 25, 30, np.inf]
spd_labels = speed_labels(spd_bins, units='knots')

dir_bins = np.arange(-7.5, 370, 15)
dir_labels = (dir_bins[:-1] + dir_bins[1:]) / 2

rose = (
    df1.assign(ws_bins=lambda df:
            pd.cut(df['ws'], bins=spd_bins, labels=spd_labels, right=True)
         )
        .assign(wd_bins=lambda df:
            pd.cut(df['wd'], bins=dir_bins, labels=dir_labels, right=False)
         )
        .replace({'wd_bins': {360: 0}})
        .groupby(by=['ws_bins', 'wd_bins'])
        .size()
        .unstack(level='ws_bins')
        .fillna(0)
        .assign(calm=lambda df: calm_count / df.shape[0])
        .sort_index(axis=1)
        .applymap(lambda x: x / total_count * 100)
)

def wind_rose(rosedata, wind_dirs, palette=None):
    if palette is None:
        palette = sns.color_palette('inferno', n_colors=rosedata.shape[1])

    bar_dir, bar_width = _convert_dir(wind_dirs)

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    ax.set_theta_direction('clockwise')
    ax.set_theta_zero_location('N')

    for n, (c1, c2) in enumerate(zip(rosedata.columns[:-1], rosedata.columns[1:])):
        if n == 0:
            # first column only
            ax.bar(bar_dir, rosedata[c1].values, 
                   width=bar_width,
                   color=palette[0],
                   edgecolor='none',
                   label=c1,
                   linewidth=0)

        # all other columns
        ax.bar(bar_dir, rosedata[c2].values, 
               width=bar_width, 
               bottom=rosedata.cumsum(axis=1)[c1].values,
               color=palette[n+1],
               edgecolor='none',
               label=c2,
               linewidth=0)

    leg = ax.legend(loc=(0.75, 0.95), ncol=2)
    xtl = ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
    
    return fig

directions = np.arange(0, 360, 15)
fig = wind_rose(rose, directions)
"""

"""


fig, ax = plt.subplots(figsize = (15, 10))
#range tanggal
ax.plot(df1.loc['2018', 'ch4'], linestyle='-')
ax.set_ylabel('Kadar CH4')
ax.set_title('KADAR CH4 JANUARI 2018')
# Set x-axis major ticks to weekly interval, on Mondays ,bisa dihapus 
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.SUNDAY))
# Format x-tick labels as 3-letter month name and day number
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'));
"""
