import numpy as np
import pandas as pd

def ReadEnergyValues(database):

    Y_raw = None
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
    y = y[['CO2 of Total Energy (Millionen Tonnen)']]
    y.columns = ['co2']

    y.index = y.index.strftime('%Y-%m')

    return y