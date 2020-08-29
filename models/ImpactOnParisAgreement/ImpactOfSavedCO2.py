#!/usr/bin/env python
# coding: utf-8

# In[51]:


import pandas as pd
import numpy as np
import fair


# In[80]:


#df_co2_Cor: Dataframe with column 'co2_Cor' which has the monthly co2 emissions from 01/2011 to 12/2020
#df_co2_noCor: Dataframe with column 'co2_noCor' which has the monthly co2 emissions from 01/2011 to 12/2020
#start date 01/2011 can also be another date but both dataframes must have the same number of rows.

#return: dictionary with: 'delta_CO2_in_MioTons', 'savedEmission_in_Days', 'delta_T_in_GradK', 'delta_C_in_ppm''

def ImpactOfReduction(df_co2_Cor, df_co2_noCor):
    
   
    
    #convert to datetime if needed
    try: 
        df_co2_noCor.index = pd.to_datetime(df_co2_noCor.index) 
    except: 
        pass
    try: 
        df_co2_Cor.index = pd.to_datetime(df_co2_Cor.index) 
    except: 
        pass

    #yearly sums
    df_co2_noCor['year'] = df_co2_noCor.index.year
    df_co2_Cor['year'] = df_co2_Cor.index.year

    df_co2_noCor = df_co2_noCor.groupby('year').sum()
    df_co2_Cor = df_co2_Cor.groupby('year').sum()

    #impact on concentration and temperature increase
    emissions_noCor = df_co2_noCor.co2_noCor.to_numpy() #in MtC
    emissions_Cor = df_co2_Cor.co2_Cor.to_numpy() #in MtC
    
    #saved CO2 emissions in Mio tons and days of emissions
    delta_CO2 = (np.sum(emissions_noCor) - np.sum(emissions_Cor))
    dailyEmissions2019 = emissions_noCor[-2]/365
    savedEmissionInDays = delta_CO2/dailyEmissions2019
    
    emissions_noCor = emissions_noCor / 1000 #in GtCO2
    emissions_Cor = emissions_Cor / 1000 #in GtCO2
    
    #co2 mass must be converted to carbon mass using the molar mass of CO2 (44g/mol) and of Carbon (12g/mol)
    emissions_noCor = (emissions_noCor/44)*12 #in GtC
    emissions_Cor = (emissions_Cor/44)*12 #in GtC
    
    #usage of library FAIR to calculate the impact on global CO2 concentration and temperature increase
    #https://gmd.copernicus.org/articles/11/2273/2018/
    other_rf = np.zeros(emissions_noCor.size)
    for x in range(0, emissions_noCor.size):
        other_rf[x] = 0.5 * np.sin(2 * np.pi * (x) / 14.0)


    #running the fair simulator for the case of corona and no corona to get the difference
    C_noCor,F_noCor,T_noCor = fair.forward.fair_scm(
        emissions=emissions_noCor,
        other_rf=other_rf,
        useMultigas=False
    )

    C_Cor,F_Cor,T_Cor = fair.forward.fair_scm(
        emissions=emissions_Cor,
        other_rf=other_rf,
        useMultigas=False
    )
    

    
    delta_T = np.sum(T_noCor) - np.sum(T_Cor) #impact on global temperature
    delta_C = np.sum(C_noCor) - np.sum(C_Cor) #impact on global CO2 concentration
    
    
    dic_ret = {'delta_CO2_in_MioTons': delta_CO2,
               'savedEmission_in_Days': savedEmissionInDays,
               'delta_T_in_GradK': delta_T,
               'delta_C_in_ppm': delta_C
              }
    
    return dic_ret
    
    