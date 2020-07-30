import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense, Flatten
import json


# Set window size
look_back = 12  # months
horizon = 6     # months
split_ratio = 0.8

def get_data():
    # Read in feature data
    with open('feature_database.json') as json_database:
        database = json.load(json_database)

    # Concat data
    feature_data = None 
    for i in database:
        new_data = pd.read_json(database[i]['data'])
        if new_data.shape[0] > 32:  # Filter CO2 data
            if feature_data is None:
                feature_data = new_data
            else:
                feature_data = pd.concat([feature_data, new_data], axis=1, join="inner")
        else:
            print(f"Feature not used: {i}")

    feature_data = feature_data.values
    feature_data = feature_data.astype('float64')
    scaler = StandardScaler()
    feature_data = scaler.fit_transform(feature_data)

    # Read in emission data
    emission_data = pd.read_csv(
    "oeko-institut_sektorale_abgrenzung_treibhausgasemissionen_daten_sektor_monthly.csv")
    emission_data = emission_data['Total_CO2_Emission'].values
    emission_data = emission_data.astype('float64')
    # Take only the emissions on which we have indicators
    emission_data = emission_data[len(emission_data)-feature_data.shape[0]:]

    return feature_data, emission_data

# Convert an array of values into a dataset matrix
def sliding_window(input, output, look_back=1, horizon=1):
    dataX, dataY = [], []
    if len(input) != len(output):
        raise ValueError('Input and ouput do not have same length!')
    for i in range(len(input)-look_back-horizon):
        dataX.append(input[i:(i+look_back)])
        dataY.append(output[(i+look_back):(i+look_back+horizon)])
    return np.array(dataX), np.array(dataY)

def train_model(trainX, trainY, testX,  testY, lock_back, horizon):
    model = Sequential()
    if len(trainX.shape) >= 3:
        model.add(Flatten())
        model.add(Dense(trainX.shape[2]*look_back,
                        input_dim=trainX.shape[2]*look_back,
                        activation='relu'))
        model.add(Dense(int(trainX.shape[2]/4)*look_back,
                        input_dim=(trainX.shape[2]*look_back),
                        activation='relu'))
        model.add(Dense(int(trainX.shape[2]/8)*look_back,
                        input_dim=(trainX.shape[2]*look_back)/4,
                        activation='relu'))
    else:
        model.add(Dense(24, input_dim=look_back, activation='relu'))
    model.add(Dense(12, activation='relu'))
    model.add(Dense(horizon))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=400, batch_size=2, verbose=2)
    # Estimate model performance
    trainScore = model.evaluate(trainX, trainY, verbose=0)
    print('Train Score: %.2f MSE (%.2f RMSE)' % (trainScore, math.sqrt(trainScore)))
    testScore = model.evaluate(testX, testY, verbose=0)
    print('Test Score: %.2f MSE (%.2f RMSE)' % (testScore, math.sqrt(testScore)))

    # Generate predictions for training
    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)

    return model, trainPredict, testPredict

feature_data, emission_data = get_data()

# Split into train and test sets
train_size = int(len(feature_data) * split_ratio)
test_size = len(feature_data) - train_size
if test_size < (look_back+horizon):
    raise ValueError('Split ratio too small. Increase test size!')

## Create datasets with features as inputs
# trainX, trainY = sliding_window(feature_data[0:train_size,:],
#                                 emission_data[0:train_size],
#                                 look_back,
#                                 horizon)
# testX, testY = sliding_window(feature_data[train_size:len(feature_data),:],
#                               emission_data[train_size:len(emission_data)],
#                               look_back,
#                               horizon)

# Create datasets with only emission data
trainX, trainY = sliding_window(emission_data[0:train_size],
                                emission_data[0:train_size],
                                look_back,
                                horizon)
testX, testY = sliding_window(emission_data[train_size:len(emission_data)],
                              emission_data[train_size:len(emission_data)],
                              look_back,
                              horizon)
print(trainX.shape)
print(trainY.shape)
print(testX.shape)
print(testY.shape)


# Create and fit Multilayer Perceptron model for every indicator
trainPredictPlot = np.empty_like(emission_data)
trainPredictPlot[:] = np.nan
testPredictPlot = np.empty_like(emission_data)
testPredictPlot[:] = np.nan

# Train model and generate predictions
model, trainPredict, testPredict = train_model(trainX, trainY, testX, testY,
                                               look_back, horizon)

# Shift train predictions for plotting
for t in range(len(trainPredict)):
    trainPredictPlot[t+look_back:t+look_back+horizon] = trainPredict[t, :]
for t in range(len(testPredict)):
    testPredictPlot[len(trainPredict)+t+look_back+horizon:len(trainPredict)+
                    t+look_back+(horizon*2)] = testPredict[t, :]

# Plot baseline and predictions
plt.plot(emission_data[:])
plt.plot(trainPredictPlot[:])
plt.plot(testPredictPlot[:])
plt.show()

# Save variables
import pickle
with open('mlp.pkl', 'wb') as f:
    pickle.dump([model, trainPredictPlot, testPredictPlot], f)

# Getting back the objects:
# with open('mlp.pkl', 'rb') as f:
#     model, trainPlot, testPlot = pickle.load(f)

# Forecast predictions
forecastPlot = np.zeros((len(emission_data) + horizon))
forecastPlot[:] = np.nan

## Features
# X = np.zeros((1, look_back, feature_data.shape[1]))
# X[0] = feature_data[len(feature_data)-look_back:, :]
# predict = model.predict(X)
# forecastPlot[len(feature_data):len(feature_data)+horizon] = predict[:]

# Emissions
X = np.zeros((1, look_back))
X[0] = emission_data[len(emission_data)-look_back:]
predict = model.predict(X)
forecastPlot[len(emission_data):len(emission_data)+horizon] = predict[:]

print(f"Forecast: {predict}")

# Plot baseline and forecast
plt.plot(emission_data[:])
plt.plot(trainPredictPlot[:])
plt.plot(testPredictPlot[:])
plt.plot(forecastPlot[:])
plt.show()