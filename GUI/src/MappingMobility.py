import numpy as np
import pandas as pd
import sklearn
import json
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.decomposition import PCA
from sklearn.linear_model import Ridge, Lasso, LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.model_selection import KFold, LeaveOneOut, GridSearchCV
from sklearn.preprocessing import RobustScaler, MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


from sklearn.cross_decomposition import PLSRegression
from sklearn.compose import ColumnTransformer

from sklearn.model_selection import KFold
    
######################    
def featureMapping(database):    
    ##Format Data
    #extract mobility features
    X_mob_raw = None 
    for i in database:
        feature = database.get(i)
        if feature['sector'] == 'mobility':
            new_data = pd.read_json(database[i]['data'])
            if X_mob_raw is None:
                X_mob_raw = new_data
            else:
                X_mob_raw = pd.concat([X_mob_raw, new_data], axis=1)
                
    #convert index in datetime format
    X_mob_raw['date'] = X_mob_raw.index
    X_mob_raw.date = pd.to_datetime(X_mob_raw.date).dt.to_period('m')
    X_mob_raw.index = X_mob_raw.date
    X_mob_raw = X_mob_raw.drop('date', axis=1)
    
    #get period: 2011-01 - 2020-06
    X = X_mob_raw.loc['2011-01':'2020-06']
    X = X.dropna(axis=1)
        
    #extract target values
    Y_raw = None 
    for i in database:
        feature = database.get(i)
        if feature['sector'] == 'target_values':
            new_data = pd.read_json(database[i]['data'])
            if Y_raw is None:
                Y_raw = new_data
            else:
                Y_raw = pd.concat([Y_raw, new_data], axis=1, join="inner")
    
    #convert index in datetime format
    Y_raw['date'] = Y_raw.index
    Y_raw.date = pd.to_datetime(Y_raw.date).dt.to_period('m')
    Y_raw.index = Y_raw.date
    Y_raw = Y_raw.drop('date', axis=1)
    
    #get period: 2011-01 - 2020-06
    y = Y_raw.loc['2011-01':'2020-06']
    y = y[['M_Mio.tonnes_CO2']]
       
    #split data to train and prediction dataset
    X_train = X[(X.index.year <= 2018)]
    y_train = y[(y.index.year <= 2018)]
    X_test = X[(X.index.year > 2018)]    
    y_test = y[(y.index.year > 2018)]
        
    
    ##LASSO   
    #define alphas
    alphas = np.linspace(0,0.2,50)
    
    #scaling
    scaler = StandardScaler()
    scaler.fit(X_train)
    x_scaled = scaler.transform(X_train)
    
    #training with grid search
    cval = KFold(n_splits=10)
    lsso = Lasso()   
    tuned_parameters = [{'alpha': alphas}]
    search = GridSearchCV(lsso, tuned_parameters, n_jobs=-1,cv=cval,scoring='neg_mean_squared_error',return_train_score=True)
    search.fit(x_scaled, y_train)
    best_estimator = search.best_estimator_
            
    # best_param = search.best_params_['alpha']
    # ind = np.argmin(abs(alphas-best_param))
        
    #prediction
    X_test_scaled = scaler.transform(X_test)
    y_pred_test_LASSO = best_estimator.predict(X_test_scaled)
    
    #connect training target values and predicted CO2 values   
    corona1 = pd.DataFrame({'M_Mio.tonnes_CO2':y_pred_test_LASSO}, index=y_test.index)
    corona = pd.concat([y_train, corona1], axis=0, join="inner")
    corona.columns = ['co2']
    
    return corona
