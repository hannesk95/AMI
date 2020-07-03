#%% Imports
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import utils

from keras import layers
from keras.models import Sequential, Model
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout, GlobalAveragePooling2D, LSTM


#%% Fix random seed for reproducibility

np.random.seed(28)

#%% Load the dataset

data = pd.read_excel('./training_data.xlsx')
targets = pd.read_excel('./training_data_(targets_only).xlsx')
X = (data.iloc[:,2:-1]).to_numpy()
y = (data.iloc[:,-1]).to_numpy()

X = X.astype('float32')
y = y.astype('float32')

#%% Scale the data

#scaler = StandardScaler()
scaler = MinMaxScaler(feature_range=(0, 1))
X = scaler.fit_transform(X)

#%% Frame data for supervised learning

reframed = utils.series_to_supervised(X, 1, 10)
# drop columns in (t) which will be not prediced
reframed.drop(reframed.columns[[3,4,6,7,9,10,12,13,15,16,18,19,21,22,24,25,27,28, 30, 31]], axis=1, inplace=True)

#%% Reshape input to be 3D [samples, timesteps, features]

values =reframed.values
train_X, train_y = values[:, :-1], values[:, -1]
train_X = train_X[:,0:2]

train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = train_X
test_y = train_y
print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

#%% Create neural network archtecture

model = Sequential()
model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2]), return_sequences=True))
model.add(LSTM(10))
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')
model.summary()

#%% Train network
history = model.fit(X, y, validation_data=(test_X, test_y), 
                    epochs=250, batch_size=16, verbose=1,shuffle=False)

#%% Plot training history
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.legend()
plt.title('Progression of loss over epochs')
plt.ylabel('loss')
plt.xlabel('epochs')
plt.show()

#%% Prediction

