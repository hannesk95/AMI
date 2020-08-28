
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import json
import random
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pmdarima as pm
from sklearn.utils import shuffle
from keras.models import Sequential
from keras.layers import Dense, Flatten, InputLayer, LSTM, Dropout, BatchNormalization, Conv1D, MaxPooling1D
from keras.callbacks import EarlyStopping
from keras import backend as K





def Sarima(emission_input, sector):
    # Read in emission data

    emission_index = emission_input.index
    #data = emission_input[emission_index[0]:'2018-12']
    original_data = emission_input[emission_index[0]:'2018-12']

    data = emission_input['2011-01':'2018-12']
    plotdata = emission_input['2011-01':'2020-12']
    prediction_index = emission_index[len(data)-24:len(data)]
    time_scope = emission_index
    #print(emission_index)
    
    
    #train_data = train_data['1991-01':'2018-12']
    #prediction_index = emission_index[len(data)-24:len(data)]

    #for i in range emission_index:
    #    if i == '2018-12'


    #first_date = emission_index[0]
    #last_date = emission_index[-1]
    #split_train = np.arange(0, len(data)-24)
    #split_test = np.arange((len(data)-24), len(data))
    #train_data = pd.Series(data, index=split_train)
    #test_data = pd.Series(data, index=split_test)
    #time_scope = emission_index

    # Seasonal - fit stepwise auto-ARIMA
    smodel = pm.auto_arima(data, start_p=1, start_q=1,
                            test='adf',
                            max_p=3, max_q=3, m=12,
                            start_P=0, seasonal=True,
                            d=None, D=1, trace=True,
                            error_action='ignore',  
                            suppress_warnings=True, 
                            stepwise=True)

    smodel.summary()
    # Forecast
    #to get accuracy predict last year as well


    n_periods = 24
    fitted, confint = smodel.predict(n_periods=n_periods, return_conf_int=True)
    #index_of_fc = pd.date_range(data.index[-1], periods = n_periods, freq='MS')
    #index_of_fc = np.arange(len(data)-12, len(data)-12+n_periods)

    #index_of_fc = np.arange(len(data)-24, len(data)-24+n_periods)
    #index_of_fc = np.arange()
    
    # make series for plotting purpose
    fitted_series = pd.Series(fitted, index=prediction_index)
    #lower_series = pd.Series(confint[:, 0], index=index_of_fc)
    #upper_series = pd.Series(confint[:, 1], index=index_of_fc)

    # Plot baseline, training, test and forecast
    #plt.figure(figsize=(20,6))
    #line1 = plt.plot(plotdata, label='Original Data')
    #line2 = plt.plot(fitted_series, label='Prediction')
    #line3 = plt.plot(original)
    #plt.fill_between(lower_series.index, 
    #                lower_series, 
    #                upper_series, 
    #                color='k', alpha=.15)
    #plt.legend(fontsize='x-large')
    #plt.grid()
    #plt.xticks(np.arange(len(time_scope))[::12], time_scope[::12], rotation=30, fontsize=12)
    #plt.xticks(np.arange(len(time_scope)), time_scope, rotation=30)
    #plt.xlim([120,380])
    #plt.xlabel("Timescope", fontsize=18)
    #plt.ylabel("Emissions in million tonnes CO2", fontsize=18)
    #plt.yticks(fontsize=18)
    #plt.title("Result SARIMA", fontsize=20)

    #plt.show()

    Sarima_Prediction = original_data.append(fitted_series)
    Sarima_Prediction.index = emission_index
    return Sarima_Prediction

#gets dataframe as input with 
def Sarima_Timeseries(timeseries, sector):

    return Sarima_Prediction  

emission_input = pd.read_csv('TimeSeriesForecasting/emission_values.csv')
emission_data = emission_input['M_Mio.tonnes_CO2'].values
emission_data = emission_data[0:len(emission_data)]
emission_data = emission_data.astype('float64')
emission_index = emission_input['date'].values
data= pd.Series(emission_data)
data.index = emission_index



#sector = mobility or energy
sector = 1
Sarima_Prediction = Sarima(data, sector)
print(Sarima_Prediction)
plt.plot(data)
plt.show()
