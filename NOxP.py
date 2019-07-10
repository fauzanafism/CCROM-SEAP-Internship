import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import matplotlib.dates as mdates
from datetime import datetime, time

data = pd.read_csv('_Bogor_Nox.csv', parse_dates=['tgl_waktu'])
data.index = pd.to_datetime(data['tgl_waktu'],format='%m%d%Y%H:%M:%S%z')
data['Year']=data.index.year
data['Month']=data.index.month
data['Weekday Name']=data.index.weekday_name

kolom = ['no', 'nox', 'no2']
data['no'][data['flag'].str.contains("X")] = ""
data['no'][data['flag'].str.contains("A")] = ""
data['no'] = pd.to_numeric(data['no'])
data['no2'][data['flag'].str.contains("X")] = ""
data['no2'][data['flag'].str.contains("A")] = ""
data['no2'] = pd.to_numeric(data['no2'])
data['nox'][data['flag'].str.contains("X")] = ""
data['nox'][data['flag'].str.contains("A")] = ""
data['nox'] = pd.to_numeric(data['nox'])
data = data[(data['no'] >= 0)]
data = data[(data['no2'] >= 0)]
data = data[(data['nox'] >= 0)]
#data = data[(data['pm25'] >= 0)]

dates = data.loc[data['tgl_waktu']]
df1 = pd.DataFrame(dates, columns=['no', 'no2', 'nox'])

dfhourlyno = df1[kolom].resample('H').mean()
dfhourlyno = pd.DataFrame(dfhourlyno)
dfdailyno = dfhourlyno[kolom].resample('D').mean()
dfdailyno = pd.DataFrame(dfdailyno)
dfweeklyno = dfdailyno[kolom].resample('W').mean()
dfweeklyno = pd.DataFrame(dfweeklyno)
dfmonthlyno = dfweeklyno[kolom].resample('M').mean()
dfmonthlyno = pd.DataFrame(dfmonthlyno)


"""
session=pd.cut(dates.tgl_waktu.dt.hour,
               [0,8,16,23],
               labels=['Malam','Pagi','Siang'],
               include_lowest=True)
dff = pd.DataFrame(session)
dfe = dff.assign(pm10=df1['pm10'])
morning = dfe.loc[dfe['tgl_waktu'] == 'Pagi']
siyang = dfe.loc[dfe['tgl_waktu'] == 'Siang']
Malama = dfe.loc[dfe['tgl_waktu'] == 'Malam']
"""


#no
sns.set(rc={'figure.figsize':(15,6)})
fig, ax = plt.subplots()
#range tanggal
ax.plot(dfmonthlyno.loc['2018', 'no'], label='no(µg/m3) ')
ax.plot(dfmonthlyno.loc['2018', 'no2'], label='no2(µg/m3) ')
ax.plot(dfmonthlyno.loc['2018', 'nox'], label='nox(µg/m3) ')
ax.set_ylabel('Kadar NO(µg/m3)')
ax.set_title('TREND NO BOGOR 2016-2018')
# Set x-axis major ticks to weekly interval, on Mondays ,bisa dihapus 
ax.xaxis.set_major_locator(mdates.MonthLocator())
# Format x-tick labels as 3-letter month name and day number
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.legend();

#Januari
sns.set(rc={'figure.figsize':(15,6)})
fig, ax = plt.subplots()

#range tanggal
ax.plot(dfdailyno.loc['2018-01', 'no'], label='no(µg/m3)')
ax.plot(dfdailyno.loc['2018-01', 'nox'], label='nox(µg/m3)')
ax.plot(dfdailyno.loc['2018-01', 'no2'], label='no2(µg/m3)')

ax.set_ylabel('Kadar NO(µg/m3)')
ax.set_title('Kadar NO Kota Bogor Januari 2018')
# Set x-axis major ticks to weekly interval, on Mondays ,bisa dihapus 
ax.xaxis.set_major_locator(mdates.DayLocator())
# Format x-tick labels as 3-letter month name and day number
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
ax.legend();

#Feb
sns.set(rc={'figure.figsize':(15,6)})
fig, ax = plt.subplots()
#range tanggal
ax.plot(dfdailyno.loc['2018-02', 'no'], label='no(µg/m3)')
ax.plot(dfdailyno.loc['2018-02', 'nox'], label='nox(µg/m3)')
ax.plot(dfdailyno.loc['2018-02', 'no2'], label='no2(µg/m3)')

ax.set_ylabel('Kadar NO(µg/m3)')
ax.set_title('Kadar NO Kota Bogor Februari 2018')
# Set x-axis major ticks to weekly interval, on Mondays ,bisa dihapus 
ax.xaxis.set_major_locator(mdates.DayLocator())
# Format x-tick labels as 3-letter month name and day number
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
ax.legend();
"""
#Okt
sns.set(rc={'figure.figsize':(15,6)})
fig, ax = plt.subplots()
#range tanggal
ax.plot(dfdailypm.loc['2017-10', 'pm25'], label='pm2.5(µg/m3)')
ax.plot(dfdailypm.loc['2017-10', 'pm10'], label='pm10(µg/m3)')
ax.set_ylabel('Kadar PM (ppb)')
ax.set_title('PM BOGOR Oktober 2017')
# Set x-axis major ticks to weekly interval, on Mondays ,bisa dihapus 
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.SUNDAY))
# Format x-tick labels as 3-letter month name and day number
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
ax.legend();

#Nov
sns.set(rc={'figure.figsize':(15,6)})
fig, ax = plt.subplots()
#range tanggal
ax.plot(dfdailypm.loc['2017-11', 'pm25'], label='pm2.5(µg/m3)')
ax.plot(dfdailypm.loc['2017-11', 'pm10'], label='pm10(µg/m3)')
ax.set_ylabel('Kadar PM (ppb)')
ax.set_title('PM BOGOR November 2017')
# Set x-axis major ticks to weekly interval, on Mondays ,bisa dihapus 
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.SUNDAY))
# Format x-tick labels as 3-letter month name and day number
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
ax.legend();

#Des
sns.set(rc={'figure.figsize':(15,6)})
fig, ax = plt.subplots()
#range tanggal
ax.plot(dfdailypm.loc['2017-12', 'pm25'], label='pm2.5(µg/m3)')
ax.plot(dfdailypm.loc['2017-12', 'pm10'], label='pm10(µg/m3)')
ax.set_ylabel('Kadar PM (ppb)')
ax.set_title('PM BOGOR Desember 2017')
# Set x-axis major ticks to weekly interval, on Mondays ,bisa dihapus 
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.SUNDAY))
# Format x-tick labels as 3-letter month name and day number
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
ax.legend();
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