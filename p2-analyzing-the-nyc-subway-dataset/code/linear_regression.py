import numpy as np
import pandas
import statsmodels.api as sm

def linear_regression(features, values):
    X = features
    Y = values
    X = sm.add_constant(X)
    model = sm.OLS(Y,X)
    results = model.fit()
    intercept = results.params[0]
    params = results.params[1:]
    #print params
    print results.describe()
    return intercept, params

def predictions(dataframe):
    ################################ MODIFY THIS SECTION #####################################
    # Select features. You should modify this section to try different features!             #
    # We've selected rain, precipi, Hour, meantempi, and UNIT (as a dummy) to start you off. #
    # See this page for more info about dummy variables:                                     #
    # http://pandas.pydata.org/pandas-docs/stable/generated/pandas.get_dummies.html          #
    ##########################################################################################
    features = dataframe[['rain','weekday','hour']]
    dummy_units = pandas.get_dummies(dataframe[['UNIT']], prefix=['unit'])
    features = features.join(dummy_units)
    
    # Values
    values = dataframe['ENTRIESn_hourly']

    # Perform linear regression
    intercept, params = linear_regression(features, values)
    
    predictions = intercept + np.dot(features, params)
    return predictions
    
def compute_r_squared(original_data, predictions):
    SSres = np.sum((original_data - predictions)**2)
    SStot = np.sum((original_data - np.mean(original_data))**2)
    r_squared = 1 - (SSres / SStot)
    return r_squared    

##-----------------------------------------------------------------------------
    
df = pandas.read_csv('turnstile_weather_v2.csv')
r_squared = compute_r_squared(df['ENTRIESn_hourly'], predictions(df))

print('The R^2 value is: {}').format(r_squared)