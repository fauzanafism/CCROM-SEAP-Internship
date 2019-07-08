import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import matplotlib.dates as mdates
from datetime import datetime, time

"""def parse(x):
    return datetime.strptime(x, '%m%d%Y %H:%M:%S%z')"""

#parse untuk memisahkan tgl
data = pd.read_csv('Bogor_O3.csv', parse_dates=['tgl_waktu'])
data.index = pd.to_datetime(data['tgl_waktu'],format='%m%d%Y%H:%M:%S%z')
#groupby
data['Year']=data.index.year
data['Month']=data.index.month
data['Weekday Name']=data.index.weekday_name
#OnlyFlag=N
data['o3'][data['flag'].str.contains("X")] = ""
data['o3'][data['flag'].str.contains("A")] = ""
data['o3'] = pd.to_numeric(data['o3'])
data = data[(data['o3'] >= 0)]
plt.figure()

dates = data.loc[data['tgl_waktu']]
df1 = pd.DataFrame(dates, columns=['o3'])
dfhourly = df1.o3.resample('H').mean()
dfhourly = pd.DataFrame(dfhourly)
dfdaily = dfhourly['o3'].resample('D').mean()
dfdaily = pd.DataFrame(dfdaily)
dfweekly = dfdaily['o3'].resample('W').mean()
dfweekly = pd.DataFrame(dfweekly)
dfmonthly = dfweekly['o3'].resample('M').mean()
dfmonthly = pd.DataFrame(dfmonthly)
start, end = '2017-02-01', '2017-02-28'

#daily hourly
sns.set(rc={'figure.figsize':(11,4)})
fig, ax = plt.subplots()
ax.plot(dfhourly.loc[start:end, 'o3'], marker = '.', linestyle='-', linewidth=0.5, label='Hourly')
ax.plot(dfdaily.loc[start:end, 'o3'], marker = 'o', linestyle='-', label='Daily')
ax.set_title('Kadar O3 Bogor 2016-2018')
ax.xaxis.set_major_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
ax.set_ylabel('O3 (ppb)');

"""
#range tanggal
ax.plot(df1.loc[start:end, 'o3'], marker = '.', linestyle='-', linewidth=0.5, label='Hourly')
ax.plot(dfdaily.loc[start:end, 'o3'], marker = 'o', linestyle='-', label='Daily')
ax.set_ylabel('Kadar O3')
ax.set_title('KADAR O3 JANUARI 2018')
# Set x-axis major ticks to weekly interval, on Mondays ,bisa dihapus 
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.SUNDAY))
# Format x-tick labels as 3-letter month name and day number
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
ax.legend();
"""