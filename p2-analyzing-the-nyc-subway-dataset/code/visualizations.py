from pandas import *
from ggplot import *
from numpy import *

# Visualization 1
def histograms(turnstile_weather):
    
    rain = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain']==1]
    no_rain = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain']==0]
    
    # this df causes the bars to be stacked   
    #df = pandas.DataFrame({'rain': rain, 'no rain': no_rain})    
    
    # separate df's
    df = pandas.DataFrame({'rain': rain})    
    #df = pandas.DataFrame({'no rain': no_rain})    
    
    df = pandas.melt(df)    
    
    # for combined df remove y scale
    plot = ggplot(aes(x='value', fill='variable', color='variable'), data=df) +\
           geom_histogram(alpha=0.6, binwidth=250, stat='bin', position = 'stack') +\
           scale_x_continuous(limits=(0, 6000)) + \
           scale_y_continuous(limits=(0, 8000)) + \
           xlab('Entries') + ylab('Frequency') + ggtitle("Histogram of Entries Hourly")
    
    return plot

# Visualization 2
def ridership_day_of_week(turnstile_weather, rain):

    mo = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['day_week']==0][turnstile_weather['rain']==rain].sum()
    tu = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['day_week']==1][turnstile_weather['rain']==rain].sum()
    we = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['day_week']==2][turnstile_weather['rain']==rain].sum()
    th = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['day_week']==3][turnstile_weather['rain']==rain].sum()
    fr = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['day_week']==4][turnstile_weather['rain']==rain].sum()
    sa = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['day_week']==5][turnstile_weather['rain']==rain].sum()
    su = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['day_week']==6][turnstile_weather['rain']==rain].sum()    
    
    df = pandas.DataFrame({
        'day_week': ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
        'entries': [mo,tu,we,th,fr,sa,su]
    })  
    
    title = "Entries by Day of the Week (Rain)"
    if rain == 0:
        title = "Entries by Day of the Week (No Rain)"
    
    plot = ggplot(aes(x="day_week", y="entries"), df) + \
           geom_bar(position = 'stack', stat = 'identity') + \
           scale_y_continuous(limits=(0, 15000000)) + \
           xlab('Day of the Week') + ylab('Entries') + ggtitle(title)
      
    return plot

##-----------------------------------------------------------------------------
    
df = pandas.read_csv('turnstile_weather_v2.csv')

print histograms(df)
#print ridership_day_of_week(df, 0)
#print ridership_day_of_week(df, 1)

