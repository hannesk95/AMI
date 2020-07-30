#%% Imports

from keras.layers import InputLayer, GRU, Dense, Flatten, Dropout, Conv1D, GlobalAveragePooling1D, MaxPooling1D, LSTM, Embedding
from keras.models import Sequential
from keras.callbacks import EarlyStopping
from sklearn.metrics import r2_score,mean_squared_error
from utils import r2_keras

#%% GRU Neural Network

def gru(n_steps,n_feats,n_fore=1):
    model = Sequential(name='GRU')    

    model.add(InputLayer(input_shape=(n_steps, n_feats)))
    model.add(GRU(8, return_sequences=False, name="GRU_1"))
    #model.add(GRU(8, return_sequences=False, name="GRU_2"))
    model.add(Dense(8, activation='relu', name="GRU_Dense1"))
    #model.add(Dense(16, activation='relu', name="GRU_Dense2"))
    #model.add(Dense(8, activation='relu', name="GRU_Dense3"))    
    model.add(Dense(n_fore,activation="linear",name="GRU_output"))
    
    model.compile(loss='mse', optimizer='adam',metrics=[r2_keras])
    model.summary()
    return model


#%% LSTM Neural Network

def lstm(n_steps,n_feats,n_fore=1):
    model = Sequential(name='LSTM')
    
    model.add(InputLayer(input_shape=(n_steps, n_feats)))
    model.add(LSTM(128, return_sequences=True, name="LSTM_1"))
    model.add(LSTM(64, return_sequences=False, name="LSTM_2"))
    model.add(Dense(30, activation='relu', name="LSTM_Dense1"))
    model.add(Dense(16, activation='relu', name="LSTM_Dense2"))
    model.add(Dense(8, activation='relu', name="LSTM_Dense3"))    
    model.add(Dense(n_fore,activation="linear",name="LSTM_output"))
    
    model.compile(loss='mse', optimizer='adam',metrics=[r2_keras])
    model.summary()
    return model

#%% Feedforward Neural Network

def mlp(n_steps,n_feats,n_fore=1):
    model = Sequential(name='MLP')    

    model.add(InputLayer(input_shape=(n_steps, n_feats)))
    model.add(Dense(4, activation='elu', name="MLP_1"))
    #model.add(Dense(30, activation='elu', name="MLP_2"))    
    model.add(Flatten())    
    model.add(Dense(n_fore,activation="linear",name="MLP_output"))
    
    model.compile(loss='mse', optimizer='adam',metrics=[r2_keras])
    model.summary()
    return model


#%% Convolutional Neural Network

def cnn(n_steps,n_feats,n_fore=1):
    model = Sequential(name='CNN')    

    model.add(InputLayer(input_shape=(n_steps, n_feats)))
    model.add(Conv1D(filters=64, kernel_size=3, activation='relu', name="Conv_1"))
    model.add(MaxPooling1D(pool_size=2, name='MaxPool_1')) 
    model.add(Flatten())    
    model.add(Dense(n_fore, activation='linear', name="CNN_output"))
    
    model.compile(optimizer='adam', loss='mse', metrics=[r2_keras])
    model.summary()
    return model