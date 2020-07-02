#%% Imports
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

#%% Fix random seed for reproducibility

np.random.seed(28)

#%% Load the dataset

data = pd.read_excel('./training_data.xlsx')
