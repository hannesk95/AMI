#%% Imports

import numpy as np
import matplotlib.pyplot as plt
import json
from sklearn.model_selection import train_test_split
import pandas as pd


#%% Plot history function

def plot_model_history(history, ax=None, metric='loss', ep_start=1, ep_stop=None, monitor='val_loss', mode='min', plttitle=None):
    if ax is None:
        fig,ax = plt.subplots()
    if ep_stop is None:
        ep_stop = len(history.epoch)
    if plttitle is None:
        plttitle = metric[0].swapcase() + metric[1:] + ' During Training'
    ax.plot(np.arange(ep_start,ep_stop+1, dtype='int'),history.history[metric][ep_start-1:ep_stop])
    ax.plot(np.arange(ep_start,ep_stop+1, dtype='int'),history.history['val_' + metric][ep_start-1:ep_stop])
    ax.set(title=plttitle)
    ax.set(ylabel=metric[0].swapcase() + metric[1:])
    ax.set(xlabel='Epoch')
    ax.legend(['train', 'val'], loc='upper right')
    
    
#%% R2-score metrics for keras backend

from keras import backend as K

def r2_keras(y_true, y_pred):
    SS_res =  K.sum(K.square(y_true - y_pred)) 
    SS_tot = K.sum(K.square(y_true - K.mean(y_true))) 
    return ( 1 - SS_res/(SS_tot + K.epsilon()) )

#%% Load data from file

def load_data(path = '../../../../data/database.json'):   
    
    with open(path) as json_database:
        database = json.load(json_database)

    # Concat data from sector economy
    X_eco_raw = None 
    X_energy_raw = None
    X_eh_raw = None
    
    for i in database:
        feature = database.get(i)
        
        if feature['sector'] == 'Energy':
            new_data = pd.read_json(database[i]['data'])
            if X_energy_raw is None:
                X_energy_raw = new_data
            else:
                X_energy_raw = pd.concat([X_energy_raw, new_data], ignore_index=True, axis=1)#, join="inner")
                
        if feature['sector'] == 'energy_households':
            new_data = pd.read_json(database[i]['data'])
            if X_eh_raw is None:
                X_eh_raw = new_data
            else:
                X_eh_raw = pd.concat([X_eh_raw, new_data], ignore_index=True, axis=1)#, join="inner")
                
        if feature['sector'] == 'economy':
            new_data = pd.read_json(database[i]['data'])
            if X_eco_raw is None:
                X_eco_raw = new_data
            else:
                X_eco_raw = pd.concat([X_eco_raw, new_data], ignore_index=True, axis=1)#, join="inner")
    
    #dataset = X_eco_raw.values
    #dataset = dataset.astype('float64')
    
    return X_energy_raw, X_eh_raw, X_eco_raw

#%% Split data

def split_data(data, num_input=12, num_output=5):
    
    feature_data = data[:, :-1]
    target_data = data[:, -1].reshape(-1,1)
    
    first_dim = (len(feature_data)-(num_input+num_output))+1
    
    X = np.zeros((first_dim, num_input, feature_data.shape[1]))
    y = np.zeros((first_dim, num_output))    
    
    for i in range(first_dim):
        X[i, :, :] = feature_data[i:i+num_input,:]
        y[i, :] = target_data[i+num_input:i+(num_input+num_output), :].reshape(-1)   
    
    
    X_train, X_test, y_train, y_test = train_test_split(X , y, shuffle=True ,random_state=28 ,test_size=0.2)
    
    return X_train, X_test, y_train, y_test
    
    
        
        
    
    