#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import json
import datetime as dt
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression
import seaborn as sns
from scipy import stats

plt.rcParams.update({'font.size':16})


# # Functions

# In[2]:
#Function to train the linear regression with Corona cases on co2 emissions
# df_cor needs one column named 'cases' with the Covid-19 cases in Germany
# df_co2 needs one column named 'co2' needs to be at least from 01/2019 to 06/2020

#return: lr_cor_co2: Linear regression model that maps monthyl corona cases on the Emission reduction to the year before. 
# This model is the input for EstimateCO2withCorona
def TrainLRCoronaOnCO2(df_cor, df_co2, verbose=True):
    
    #convert datetime index to string index if needed
    #for corona case numbers dataframe
    try: 
        df_cor.index = df_cor.index.strftime('%Y-%m')
    except:
        pass
    #for co2 emissions dataframe
    try: 
        df_co2.index = df_co2.index.strftime('%Y-%m')
    except:
        pass
    
    #reduce dataframes to 2019 and 2020 and concat them
    df_cor = df_cor.loc['2018-12':'2020-06']
    df_co2 = df_co2.loc['2018-12':'2020-06']
    df = pd.concat([df_cor, df_co2], axis=1)

    #calcualte difference between 2019 co2 emissions and 2020 co2 emissions
    diff_co2_1920 = ((df.loc['2018-12':'2019-06', 'co2'].to_numpy() - df.loc['2019-12':'2020-06', 'co2'].to_numpy())/df.loc['2018-12':'2019-06', 'co2'].to_numpy())
    
    #add diff co2 to dataframe
    df = df.loc['2019-12':'2020-06']
    df['diff_co2_1920'] = diff_co2_1920

    #train linear regression
    lr_cor_co2 = LinearRegression() #fit_intercept=False
    lr_cor_co2.fit(df.cases.values.reshape(-1, 1), df.diff_co2_1920)
    
    #test on same data
    pred_diff_co2_1920 = lr_cor_co2.predict(df.cases.values.reshape(-1, 1))
    
    #add predictions to dataframe
    df['pred_diff_co2_1920'] = pred_diff_co2_1920
    
    
    #plot result
    if verbose:
        print('r2: ', round(r2_score(diff_co2_1920, pred_diff_co2_1920),2))
        print('RMSE: ', round(np.sqrt(mean_squared_error(diff_co2_1920, pred_diff_co2_1920)),2))
        df[['diff_co2_1920', 'pred_diff_co2_1920']].plot(figsize=(12,9))
        plt.grid()
        plt.xlabel('Difference in Mio tons CO2 to 2019')
        
        #scatter plot
        g = sns.JointGrid(x=diff_co2_1920,y=pred_diff_co2_1920, ratio=100)
        g.plot_joint(sns.regplot)
        g.annotate(stats.pearsonr)
        g.ax_marg_x.set_axis_off()
        g.ax_marg_y.set_axis_off()
        plt.xlabel('diff_co2_1920')
        plt.ylabel('pred_diff_co2_1920')
        
    return lr_cor_co2
    
    
#use the linear model from "TrainLRCoronaOnCO2" to estimate the impact of cases on co2 
#Input: 
#lr_cor_co2: Linear regression model that maps monthyl corona cases on the Emission reduction to the year before. 
# df_cases_new needs one column named 'cases' with the Covid-19 cases in Germany
# df_co2 needs one column named 'co2' needs to be at least from 01/2019 to 06/2020

#return: dataframe with CO2 emissions for the time span 07/2020 to 12/2020
def EstimateCO2withCorona(lr_cor_co2, df_cases_new, df_co2):
    
    cases = df_cases_new.cases.to_numpy()
    for i in range(len(cases)):
        if cases[i] > 90000:
            cases[i] = 90000
        elif cases[i] < 0:
            cases[i] = 0
        
    #convert datetime index to string index if needed
    #for corona case numbers dataframe
    try: 
        df_cases_new.index = df_cases_new.index.strftime('%Y-%m')
    except:
        pass
    
    #for co2 emissions dataframe
    try: 
        df_co2.index = df_co2.index.strftime('%Y-%m')
    except:
        pass
        
    pred_diff = lr_cor_co2.predict(cases.reshape(-1, 1))
    
    pred = df_co2.loc['2019-07':'2019-12', 'co2'].to_numpy() * (1-pred_diff) 
    
    df_ret = pd.DataFrame({'co2':pred}, index=df_cases_new.index)

    return df_ret
    
    