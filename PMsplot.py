import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import matplotlib.dates as mdates
from datetime import datetime, time

data = pd.read_csv('Bogor_PM2.5-PM10.csv', parse_dates=['tgl_waktu'])
data.index = pd.to_datetime(data['tgl_waktu'],format='%m%d%Y%H:%M:%S%z')
data['Year']=data.index.year
data['Month']=data.index.month
data['Weekday Name']=data.index.weekday_name
data['pm25'][data['flag'].str.contains("X")] = ""
data['pm25'][data['flag'].str.contains("A")] = ""
data['pm25'] = pd.to_numeric(data['pm25'])
data['pm10'][data['flag'].str.contains("X")] = ""
data['pm10'][data['flag'].str.contains("A")] = ""
data['pm10'] = pd.to_numeric(data['pm10'])
data = data[(data['pm10'] >= 0)]
data = data[(data['pm25'] >= 0)]
plt.figure()
dates = data.loc[data['tgl_waktu']]
df1 = pd.DataFrame(dates, columns=['pm25', 'pm10'])
start, end = '2016', '2018'
session=pd.cut(dates.tgl_waktu.dt.hour,
               [0,8,16,23],
               labels=['Malam','Pagi','Siang'],
               include_lowest=True)
dff = pd.DataFrame(session)
dfe = dff.assign(pm10=df1['pm10'])

morning = dfe.loc[dfe['tgl_waktu'] == 'Pagi']
siyang = dfe.loc[dfe['tgl_waktu'] == 'Siang']
Malama = dfe.loc[dfe['tgl_waktu'] == 'Malam']
#pm25
sns.set(rc={'figure.figsize':(15,6)})
fig, ax = plt.subplots()
#range tanggal
ax.plot(morning.loc[start:end, 'pm10'])
ax.plot(siyang.loc[start:end, 'pm10'])
ax.plot(Malama.loc[start:end, 'pm10'])
ax.set_ylabel('Kadar PM10 (ppb)')
ax.set_title('KADAR PM10 BOGOR 2016-2018')
# Set x-axis major ticks to weekly interval, on Mondays ,bisa dihapus 
ax.xaxis.set_major_locator(mdates.MonthLocator())
# Format x-tick labels as 3-letter month name and day number
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.legend();
#pm10
'''
fig, ax = plt.subplots(figsize=(12,8))
#range tanggal
ax.plot(morning.loc[start:end, 'pm10'])
ax.plot(siyang.loc[start:end, 'pm10'])
ax.plot(Malama.loc[start:end, 'pm10'])
ax.set_ylabel('Kadar PM10 (ppb)')
ax.set_title('KADAR PM10 JANUARI 2018')
# Set x-axis major ticks to weekly interval, on Mondays ,bisa dihapus 
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.SUNDAY))
# Format x-tick labels as 3-letter month name and day number
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
ax.legend(["Pagi", "Siang", "Malam"], fontsize=15);
'''
"""
plt.plot(df1.as_matrix(),'-')
plt.xticks(x,labels,rotation='vertical',fontsize=12)
plt.legend(["PM2.5(ppb)", "PM10(ppb)"], fontsize=15)
plt.grid(True)
plt.xlabel('Bulan', fontsize=15)
plt.ylabel('Kandungan PM2.5 dan PM10(ppb)', fontsize=15)
plt.title('KANDUNGAN PM KOTA BOGOR 2017',fontsize=20)
plt.show()
"""