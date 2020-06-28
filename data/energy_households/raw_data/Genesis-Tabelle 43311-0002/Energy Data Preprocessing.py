# -*- coding: utf-8 -*-
"""Energy Data Conversion to csv.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vSX7XENEY-tZTp9_UTcU4l1ZVrBTe8hQ
"""

# Import necessary packages
import numpy as np
import pandas as pd
import seaborn as sns 
import json
import datetime

import pandas as pd
df= pd.read_csv('/content/43311_1.csv', encoding='UTF-8', sep=';', skiprows=5)
df=df.replace('-', 0)
df=df.replace('.', 0)
df.head(55)

#print(df['Energieart'][0*624])

Monat=100;
Energieart=8;
print(df['Jahr'][Monat*52+Energieart]); print(df['Monat'][Monat*52+Energieart]); print(df['Energieart'][Monat*52+Energieart]); print(df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+Energieart])

size=218
list_empty = [None] * size
list_empty
#d = {'Date': list_empty, 'Coal-PC': list_empty, 'Gas': list_empty,'Biomass': list_empty, 'Solar PV - Utility scale': list_empty, 'Solar PV - rooftop': list_empty, 'Geothermal': list_empty, 'Concentrated solar power': list_empty, 'Hydropower': list_empty, 'Wind Offshore': list_empty, 'Nuclear': list_empty, 'Wind Onshore': list_empty, 'Pre-commercial technologies': list_empty, 'Ocean (Tidal and wave)': list_empty}
d = {'date': list_empty, 'CO2 of Coal-Energy in (gram)': list_empty, 'CO2 of Gas in (gram)': list_empty,'CO2 of Biomass (gram)': list_empty, 'CO2 of Photovoltaik (gram)': list_empty, 'CO2 of Hydropower (gram)': list_empty, 'CO2 of Nuclear (gram)': list_empty, 'CO2 of Windenergy (gram)': list_empty}


df_CO2_Energy_related = pd.DataFrame(data=d)

df_CO2_Energy_related.head(5) 



for Monat in range(0, size+1):
  COAL_TEMP=0; 
  GAS_TEMP=0;   
  BIOMASS_TEMP=0; 
  SOLAR_TEMP=0;  
  SOLAR_PHOTOVOLTAIK_TEMP=0;
  Geothermal_TEMP=0;
  WATERPOWER_TEMP=0;
  WINDPOWER_TEMP=0;
  NUCLEARPOWER_TEMP=0;

  #Summation for Coal
  for i_temp in range(0, 12):
  #  print(i_temp);
    COAL_TEMP=COAL_TEMP+int(df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+i_temp]);
  #  print (df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+i_temp]);

  #Summation for GAS
  for i_temp in range(15, 17):
   # print(i_temp);
    GAS_TEMP=GAS_TEMP+int(df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+i_temp]);
    #print (df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+i_temp]);

  for i_temp in range(19, 25):
    GAS_TEMP=GAS_TEMP+int(df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+i_temp]);
    #print(i_temp);
    #print (df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+i_temp]);
 
  for i_temp in range(37, 41):
    GAS_TEMP=GAS_TEMP+int(df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+i_temp]);
    #print(i_temp);
    #print (df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+i_temp]);
  
#Summation for Biomass
  for i_temp in range(35, 37):
   # print(i_temp);
    BIOMASS_TEMP=BIOMASS_TEMP+int(df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+i_temp]);
    #print (df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+i_temp]);

  for i_temp in range(42, 46):
   # print(i_temp);
    BIOMASS_TEMP=BIOMASS_TEMP+int(df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+i_temp]);
    #print (df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+i_temp]);


#Summation for Solarthermie

  SOLAR_TEMP=SOLAR_TEMP+int(df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+34]);
  #print (df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+34]);

#Summation for Photovoltaik

  SOLAR_PHOTOVOLTAIK_TEMP=SOLAR_PHOTOVOLTAIK_TEMP+int(df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+31]);
  #print (df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+31]);

#Summation for Geothermal Energy

#  Geothermal_TEMP=Geothermal_TEMP+int(df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+32]);
  #print (df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+31]);

#Summation for Nuclear Power

  NUCLEARPOWER_TEMP=NUCLEARPOWER_TEMP+int(df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+46]);
  #print (df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+46]);


#Summation for Water Power
  for i_temp in range(25, 30):
   # print(i_temp);
    WATERPOWER_TEMP=WATERPOWER_TEMP+int(df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+i_temp]);
    #print (df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+i_temp]);

#Summation for Wind Power
  i_temp=30;
   # print(i_temp);
  WINDPOWER_TEMP=WINDPOWER_TEMP+int(df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+i_temp]);
  #print (df['Elektrizitätserzeugung (brutto) in MWh'][Monat*52+i_temp]);




# Umrechnung von MWh in gCo2 siehe: https://en.wikipedia.org/wiki/Life-cycle_greenhouse-gas_emissions_of_energy_sources#2014_IPCC.2C_Global_warming_potential_of_selected_electricity_sources

  df_CO2_Energy_related ['CO2 of Coal-Energy in (gram)'][Monat]=COAL_TEMP*1000*820; 
  df_CO2_Energy_related ['CO2 of Gas in (gram)'][Monat]=GAS_TEMP*1000*490; 
  df_CO2_Energy_related ['CO2 of Biomass (gram)'][Monat]=BIOMASS_TEMP*1000*230; 
  #df_CO2_Energy_related ['Solar PV - Utility scale'][Monat]=SOLAR_TEMP*1000*48; 
  df_CO2_Energy_related ['CO2 of Photovoltaik (gram)'][Monat]=SOLAR_PHOTOVOLTAIK_TEMP*1000*41; 
  #df_CO2_Energy_related ['Geothermal'][Monat]=Geothermal_TEMP*1000*38;
  df_CO2_Energy_related ['CO2 of Hydropower (gram)'][Monat]=WATERPOWER_TEMP*1000*24;
  df_CO2_Energy_related ['CO2 of Windenergy (gram)'][Monat]=WINDPOWER_TEMP*1000*11;
  df_CO2_Energy_related ['CO2 of Nuclear (gram)'][Monat]= NUCLEARPOWER_TEMP*1000*12;


  if 1+Monat%12 <10:
    Monat_temp= '0'+ str(1+Monat%12)
  else:
    Monat_temp=str(1+Monat%12)

  df_CO2_Energy_related ['date'][Monat]=str(2002+(Monat//12))+'-'+Monat_temp;



df_CO2_Energy_related.to_csv('E_ProccessEnergyCO2EMISSIONS', index=False)
df_CO2_Energy_related

import matplotlib.pyplot as plt
plt.plot(df_CO2_Energy_related ['Coal-PC'])
plt.plot(df_CO2_Energy_related ['Biomass'])
#plt.plot(df_CO2_Energy_related ['Gas'])
#plt.plot(df_CO2_Energy_related ['Biomass'])

#plt.plot(df_CO2_Energy_related ['Solar PV - Utility scale'])
plt.plot(df_CO2_Energy_related ['Photovoltaik'])
#plt.plot(df_CO2_Energy_related ['Geothermal'])
plt.plot(df_CO2_Energy_related ['Wind'])
plt.plot(df_CO2_Energy_related ['Nuclear'])


plt.plot(df_CO2_Energy_related ['Date'], df_CO2_Energy_related ['Nuclear'], linewidth=2.0)

plt.ylabel('Coal C02 Emission (gCO2)')
plt.show()

# Create database
database = {}


# Add to database
columns = list(df) 
columns.pop(0)
# The for loop is only necessary if you have multiple features in the same CSV
for i in columns:
        # Put your feature name in here - `indice[feature_name]`
        database[i] = {}
        database[i]['sector'] = 'enegy'
        database[i]['category'] = 'electricity and heat production'
        database[i]['feature_descprition'] = 'Describe your feature here.'
        database[i]['yearly_data'] = False

        # Create Pandas DataFrame for single feature
        timeseries=df['date'].to_frame().join(df[i])
        timeseries.date = pd.to_datetime(timeseries.date).dt.to_period('m')
        timeseries = timeseries.set_index('date')
        # Convert dataframe to JSON format
        database[i]['data'] = timeseries.to_json()