
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import json
import random
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pmdarima as pm

#database = feature database
#sector = mobility or energy
#period = 12 or 24 months
def Sarima(database, sector, period):
    #extract target values
    Y_raw = None 
    if sector == 'mobility':
        for i in database:
            feature = database.get(i)
            if feature['sector'] == 'target_values':
                new_data = pd.read_json(database[i]['data'])
                if Y_raw is None:
                    Y_raw = new_data
                else:
                    Y_raw = pd.concat([Y_raw, new_data], axis=1)
    elif sector == 'energy':
        for i in database:
            feature = database.get(i)
            if feature['sector'] == 'energy_households':
                new_data = pd.read_json(database[i]['data'])
                if Y_raw is None:
                    Y_raw = new_data
                else:
                    Y_raw = pd.concat([Y_raw, new_data], axis=1)
                    
  
    #convert index in datetime format
    Y_raw['date'] = Y_raw.index
    Y_raw.date = pd.to_datetime(Y_raw.date).dt.to_period('m')
    Y_raw.index = Y_raw.date
    Y_raw = Y_raw.drop('date', axis=1)
    
    #get period
    y = Y_raw.loc['2011-01':'2020-12']
    if sector == 'mobility':
        y = y[['M_Mio.tonnes_CO2']]
        y.columns = ['co2']
    elif sector == 'energy':
        y = y[['CO2 of Total Energy (Millionen Tonnen)']]
        y.columns = ['co2']
       
    #split data to train
    if period == 12:
        y_train = y[(y.index.year <= 2019)]   
        y_test = y[(y.index.year > 2019)]
    elif period == 24:
        y_train = y[(y.index.year <= 2018)]   
        y_test = y[(y.index.year > 2018)]
        
    #trian sarima model
    smodel = pm.auto_arima(y_train, start_p=1, start_q=1,
                            test='adf',
                            max_p=1, max_q=1, m=12,
                            start_P=0, seasonal=True,
                            d=None, D=1, trace=True,
                            error_action='ignore',  
                            suppress_warnings=True, 
                            stepwise=True)

    smodel.summary()

    #get values for next months
    fitted = smodel.predict(n_periods=period, return_conf_int=False)

    #add sarima prediciton to already availiable data
    fit = pd.DataFrame({'co2':fitted}, index=y_test.index)
    Sarima_Prediction = pd.concat([y_train, fit], axis=0, join="inner")
    Sarima_Prediction.columns = ['co2']

    return Sarima_Prediction



######################
with open('../data/feature_database.json') as json_database:
    database = json.load(json_database)

#sector: mobility or energy 
sector = 'mobility'
Sarima_Prediction = Sarima(database, sector, period=24)
Sarima_Prediction.plot()
plt.show()
