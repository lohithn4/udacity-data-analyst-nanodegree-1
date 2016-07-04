import numpy as np
import pandas
import scipy
import scipy.stats

def mann_whitney_plus_means(turnstile_weather): 
    df_rain = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain']==1]
    df_without_rain = turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain']==0]
    with_rain_mean = np.mean(df_rain)
    without_rain_mean = np.mean(df_without_rain)
    result = scipy.stats.mannwhitneyu(df_rain, df_without_rain)
    U = result[0]
    p = result[1]
    return with_rain_mean, without_rain_mean, U, p
    
turnstile_weather = pandas.read_csv('turnstile_weather_v2.csv')

results = mann_whitney_plus_means(turnstile_weather)

print('Mean with rain: {}').format(results[0])
print('Mean without rain: {}').format(results[1])
print('U-statistic: {}').format(results[2])
print('p-value: {}').format(round(results[3],4))