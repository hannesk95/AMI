#%% Imports

import models
from utils import plot_model_history, load_data, split_data
import pandas as pd
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
import matplotlib.pyplot as plt
import numpy as np

#%% Specify prediction properties

num_input_time_steps = 12
num_output_time_steps = 6

#%% Load data and standardize

emissions = pd.read_csv('../../../../data/greenhouse_emissions/oeko-institut_sektorale_abgrenzung_treibhausgasemissionen_daten_sektor_monthly.csv')
targets = emissions.values
targets = targets[144:365, -1]

X_energy_raw, X_eh_raw, X_eco_raw = load_data()
data = X_energy_raw[0]
data = pd.concat([data, X_energy_raw[1]], ignore_index=True, axis=1)
data = pd.concat([data, X_energy_raw[2]], ignore_index=True, axis=1)
data = pd.concat([data, X_energy_raw[3]], ignore_index=True, axis=1)
data = pd.concat([data, X_energy_raw[4]], ignore_index=True, axis=1)
data = pd.concat([data, X_energy_raw[5]], ignore_index=True, axis=1)
data = pd.concat([data, X_energy_raw[6]], ignore_index=True, axis=1)
data = pd.concat([data, X_eh_raw[1]], ignore_index=True, axis=1)
data = pd.concat([data, X_eh_raw[2]], ignore_index=True, axis=1)
data = pd.concat([data, X_eh_raw[3]], ignore_index=True, axis=1)
data = pd.concat([data, X_eco_raw[2]], ignore_index=True, axis=1)
data = pd.concat([data, X_eco_raw[3]], ignore_index=True, axis=1)

data = data.values
data = data[144:365, :]
data = np.concatenate((data, targets.reshape(-1,1)), axis=1)

scaler = StandardScaler()
data = scaler.fit_transform(data)

#%% Load data manual and prepare

# features = pd.read_excel('training_data.xlsx')
# targets = pd.read_csv('oeko-institut_sektorale_abgrenzung_treibhausgasemissionen_daten_sektor_monthly.csv')

# features = features.drop(['Jahr', 'Monat', 'CO2'], axis=1)

# data = features
# data['CO2'] = targets['Total_CO2_Emission']
# data_unscaled = data.values

# scaler = StandardScaler()
# data = scaler.fit_transform(data_unscaled)

#%% Split data

X_train, X_test, y_train, y_test = split_data(data, num_input_time_steps, num_output_time_steps)

#%% Build models

mlp = models.mlp(num_input_time_steps, X_train.shape[1], num_output_time_steps)
gru = models.gru(num_input_time_steps, X_train.shape[1], num_output_time_steps)
lstm = models.lstm(num_input_time_steps, X_train.shape[1], num_output_time_steps)

#%% Train models

history_mlp = mlp.fit(X_train, y_train, batch_size=8, validation_split=0.2, epochs=200, verbose=1)
history_gru = gru.fit(X_train, y_train, batch_size=8, validation_split=0.2, epochs=200, verbose=1)
history_lstm = lstm.fit(X_train, y_train, batch_size=8, validation_split=0.2, epochs=200, verbose=1)


#%% Plot history

fig, ax = plt.subplots(1, 2, figsize=(10,6))
plot_model_history(history_gru, ax = ax[0], plttitle='GRU')
plot_model_history(history_lstm, ax = ax[1], plttitle='LSTM')

#%% Evaluate on test set

model = [gru, lstm]
modelnames = ['GRU', 'LSTM']


for i,nme in enumerate(modelnames):
    print("Model: " + nme)
    print("Train [MSE, R2] value:")
    print(model[i].evaluate(X_train,y_train))
    print("")
    print("Test [MSE, R2] value:")
    print(model[i].evaluate(X_test,y_test))
    print('-------------------------------')
    
#%% Make prediction for last month of 2020

prediction_data = data[209:221, :-1].reshape(1,num_input_time_steps,-1)

predictions = lstm.predict(prediction_data)

mean = np.mean(targets)
std = np.std(targets)
predictions_rescaled = np.transpose(predictions*std + mean)
