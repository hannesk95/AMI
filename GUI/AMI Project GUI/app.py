#%%

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction, State

import numpy as np
import pandas as pd

import datetime
from datetime import datetime as dt
import pathlib

import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import dash_daq as daq
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

from dash.dependencies import Input, Output
import json
import io

from src.MappingMobility import featureMapping
from src.CoronaMapping import TrainLRCoronaOnCO2, EstimateCO2withCorona
from src.ImpactOfSavedCO2 import ImpactOfReduction
from src.Sarima_gui import Sarima

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()
DATA_PATH_SRC = BASE_PATH.joinpath("src").resolve()

global Data_plot_name
Data_plot_name ='economy'

Prediction_1 = pd.read_csv(DATA_PATH.joinpath("Prediction_1.csv"), sep=';')
Prediction_2 = pd.read_csv(DATA_PATH.joinpath("Prediction_2.csv"), sep=';')
Prediction_3 = pd.read_csv(DATA_PATH.joinpath("Prediction_3.csv"), sep=';')
Prediction_4 = pd.read_csv(DATA_PATH.joinpath("Prediction_4.csv"), sep=';')



#Import Data 
category_list=[];
sector_list=[];



#open Data_Path


with open(DATA_PATH.joinpath("feature_database.json")) as json_file:
    database = json.load(json_file)

df_co2 = featureMapping(database)
#corona
df_cor = pd.read_csv(DATA_PATH.joinpath("CORONA_GERMANY.csv"))
df_cor = df_cor.rename(columns={'myDt': 'date'})
df_cor.index = df_cor.date
df_cor = df_cor.drop('date', axis=1)
lr_cor_co2 = TrainLRCoronaOnCO2(df_cor, df_co2) #im storage ablegen

sector = 'mobility' #oder/'energy'
Sarima_nn = Sarima(database, sector, period=24)
Sarima_mobility = Sarima(database, sector, period=24)#co2 ohne corona
sector = 'energy' #oder/'energy'
Sarima_energy = Sarima(database, sector, period=24)




#%%

#  EstimateCO2withCorona(lr_cor_co2,df_slider(juli-december),Sarima_mobility/Sarima_energy)
# data   cases
# 303-1   juli 12
v7=3
v8=344
v9=344
v10=123
v11=23
v12=53

        
d = {'date':["2020-07","2020-08","2020-09","2020-10","2020-11","2020-12"], 'cases': [v7,v8,v9,v10,v11,v12]}
        
df_slider_estimation = pd.DataFrame(data=d)
df_slider_estimation.index=df_slider_estimation['date']
        
trained_values_wrongformat=EstimateCO2withCorona(lr_cor_co2,df_slider_estimation,Sarima_mobility),

# trained_values= {'cases': [13.041935514899228,13.167659103529827,13.669042942906339,13.532680100891733,13.031704074531671,12.036724563547219]}
# df_trained_values = pd.DataFrame(data=trained_values)
# df_trained_values.index=["2020-07","2020-08","2020-09","2020-10","2020-11","2020-12"]
        

#%%







for i in database:
  feature = database.get(i)
  if feature['category'] not in category_list:
    category_list.append(feature['category'])


for i in database:
  feature = database.get(i)
  if feature['sector'] not in sector_list:
    sector_list.append(feature['sector'])


def plot_barchart(monat_value):
  #import plotly.express as px
  #import pandas as pd

  size=len(monat_value)

  monate_liste=['Month 1', 'Month 2', 'Month 3','Month 4', 'Month 5', 'Month 6']
  data_min_max_full_header = {'Month': monate_liste, 'Value': monat_value}
  df = pd.DataFrame(data=data_min_max_full_header)

  fig=go.Figure()  
  #df = pd.read_csv(io.StringIO(data_range), sep='\s+')
  #df['Value'][3]=80
  #print(df)
  fig = px.bar(x=df['Month'], y=df['Value'], labels={'x':'', 'y':'Total Number'}, width=400, height=200)



  return fig


def get_min_max_date(sector_choice):
  X_eco_raw = None 
  data_name_list=[]
  list_empty = []
  data_min_max_full_header = {'Category':list_empty, 'Sector': list_empty,'Data_name': list_empty,'Start': list_empty,'End': list_empty, 'Selected': list_empty}
  data_min_max_full = pd.DataFrame(data=data_min_max_full_header)

  for cat in category_list:
    for sect in sector_list:

        for i in database:
            feature = database.get(i)
            
            if feature['sector'] == sect and feature['category'] == cat:
                new_data = pd.read_json(database[i]['data'])

                new_data_name=new_data.columns.tolist()
                new_data_name=''.join(new_data_name)
                #data_name_list.extend(new_data_name)
                df = pd.DataFrame(new_data)
                min_date=min(df.index)
                max_date=max(df.index)
                #print(min_date)
                #print(min(df.index))
                #print([cat, sect, new_data_name, min_date, max_date])
                #data_name_list.extend([cat, sect, new_data_name, min_date, max_date])
                #print(new_data_name)
                selected_yj='no'
                if sector_choice==sect:
                  selected_yj='yes'
                new_row = {'Category':cat, 'Sector': sect,'Data_name': new_data_name,'Start': min_date,'End': max_date, 'Selected': selected_yj}
                #append row to the dataframe
                data_min_max_full = data_min_max_full.append(new_row, ignore_index=True)




  #convert index in datetime format
  #X_eco_raw['date'] = X_eco_raw.index
  #X_eco_raw.date = pd.to_datetime(X_eco_raw.date).dt.to_period('m')
  #X_eco_raw.index = X_eco_raw.date
  #X_eco_raw = X_eco_raw.drop('date', axis=1)
  #X_eco_raw.head()


  #print(data_min_max_full)

  return data_min_max_full



def generate_data_availability_plot(choice):
    # Concat data from sector economy
    fig_range_plot = go.Figure()
    color_temp=None
    df = get_min_max_date(choice)
    #print(df)
    #df.sort_values('End', ascending=False, inplace=True, ignore_index=True)
            
            
    w_lbl = [str(s) for s in df['Start'].tolist()]
    m_lbl = [str(s) for s in df['End'].tolist()]
        
    for i in range(0,len(df)):
      if df['Selected'][i]=='yes':

          #print(type(df['Data_name'][i]))    
          if df['Selected'][i]=='yes':
            fig_range_plot.add_trace(go.Scatter(
                  x=[df['Start'][i],df['End'][i]],
                  y=[df['Data_name'][i],df['Data_name'][i]],
                  orientation='h',
                  line=dict(color='rgb(244,165,130)', width=8),
              ))
          if df['Selected'][i]=='no':
            fig_range_plot.add_trace(go.Scatter(
            x=[df['Start'][i],df['End'][i]],
                  y=[df['Data_name'][i],df['Data_name'][i]],
                  orientation='h',
                  line=dict(color='rgb(34,165,130)', width=8),
              ))
          
          fig_range_plot.add_trace(go.Scatter(
                  x=[df['Start'][i]],
                  y=[df['Data_name'][i]],
                  marker=dict(color='#CC5700', size=14),
                  mode='markers+text',
                  #text=w_lbl,
                  text='Start',
                  textposition='middle left',
                  name='Start'))
              
          fig_range_plot.add_trace(go.Scatter(
                  x=[df['End'][i]],
                  y=[df['Data_name'][i]],
                  marker=dict(color='#227266', size=14),
                  mode='markers+text',
                  #text=m_lbl,
                  text='End',
                  textposition='middle right',
                  name='End'))
        
    fig_range_plot.update_layout(title="Data Availability", showlegend=False)
    #fig_range_plot.update_layout(title="Data Availability", showlegend=False, height=1800)    
      
    return fig_range_plot


def plot_prediction_data(Prediction_type):
     # Concat data from sector economy
    X_eco_raw = None 
    for i in database:
        feature = database.get(i)
        if feature['sector'] == 'target_values':
            new_data = pd.read_json(database[i]['data'])
            if X_eco_raw is None:
                X_eco_raw = new_data
            else:
                X_eco_raw = pd.concat([X_eco_raw, new_data], axis=1, join="outer")
    
    #convert index in datetime format
    X_eco_raw['date'] = X_eco_raw.index
    #X_eco_raw.date = pd.to_datetime(X_eco_raw.date).dt.to_period('m')
    #X_eco_raw.index = X_eco_raw.date
    #X_eco_raw = X_eco_raw.drop('date', axis=1)
    X_eco_raw.head()
    fig_data_of_sector = go.Figure()
    for col in X_eco_raw.columns:
        fig_data_of_sector.add_trace(go.Scatter(x=X_eco_raw.index, y=X_eco_raw[col], name=col))
        #print(col)

    if Prediction_type == 'Prediction_1':
        Prediction=Prediction_1  
    if Prediction_type == 'Prediction_2':
        Prediction=Prediction_2 
    if Prediction_type == 'Prediction_3':
        Prediction=Prediction_3
    if Prediction_type == 'Prediction_4':
        Prediction=Prediction_4  
        
    Prediction.index=Prediction['date']

    fig_data_of_sector.add_trace(go.Scatter(
        x=Prediction.index, y=Prediction['CO2-Emission'],
        line_color='rgb(0,100,80)',
        name=Prediction_type,
    ))    
    fig_data_of_sector.update_layout(title=Prediction_type, showlegend=True, height=500)
    fig_data_of_sector.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)        
    return fig_data_of_sector

def plot_data_of_sector(Sector):
     # Concat data from sector economy
    X_eco_raw = None 
    for i in database:
        feature = database.get(i)
        if feature['sector'] == Sector:
            new_data = pd.read_json(database[i]['data'])
            if X_eco_raw is None:
                X_eco_raw = new_data
            else:
                X_eco_raw = pd.concat([X_eco_raw, new_data], axis=1, join="outer")
    
    #convert index in datetime format
    X_eco_raw['date'] = X_eco_raw.index
    #X_eco_raw.date = pd.to_datetime(X_eco_raw.date).dt.to_period('m')
    #X_eco_raw.index = X_eco_raw.date
    #X_eco_raw = X_eco_raw.drop('date', axis=1)
    X_eco_raw.head()
    fig_data_of_sector = go.Figure()
    for col in X_eco_raw.columns:
        fig_data_of_sector.add_trace(go.Scatter(x=X_eco_raw.index, y=X_eco_raw[col], name=col))
        #print(col)
    #fig_data_of_sector.show()
    fig_data_of_sector.update_layout(title=Sector, showlegend=True, height=500)
    fig_data_of_sector.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)
    return fig_data_of_sector


# def generate_data_availability_plot(Sector_list, choice):
#      # Concat data from sector economy
#     fig_range_plot = go.Figure()

#     # Data Availability Plot
#     data_range = '''
#      Grade Start End
#     0 "Sector 1" 1990 2020
#     1 "Sector 2" 1999 2014
#     2 "Sector 3" 1994 2002
#     3 "Sector 4" 2001 2020
#     4 "Sector 5" 2003 2007
#     5 "Sector 6" 1990 2020
#     6 "Sector 7" 2001 2010
#     7 "Sector 8" 1994 2019
#     8 "Sector 9" 2003 2019
#     9 "Sector 10" 1997 2020
#     '''
#     max_sector_number=10
    
#     df = pd.read_csv(io.StringIO(data_range), sep='\s+')
#     df.sort_values('End', ascending=False, inplace=True, ignore_index=True)
        
        
#     w_lbl = [str(s) for s in df['Start'].tolist()]
#     m_lbl = [str(s) for s in df['End'].tolist()]
    
        
#     for i in range(0,max_sector_number):
#         fig_range_plot.add_trace(go.Scatter(
#             x=[df['Start'][i],df['End'][i]],
#             y=[df['Grade'][i],df['Grade'][i]],
#             orientation='h',
#             line=dict(color='rgb(244,165,130)', width=8),
#                  ))
    
#     fig_range_plot.add_trace(go.Scatter(
#         x=df['Start'],
#         y=df['Grade'],
#         marker=dict(color='#CC5700', size=14),
#         mode='markers+text',
#         text=w_lbl,
#         textposition='middle left',
#         name='Start'))
    
#     fig_range_plot.add_trace(go.Scatter(
#         x=df['End'],
#         y=df['Grade'],
#         marker=dict(color='#227266', size=14),
#         mode='markers+text',
#         text=m_lbl,
#         textposition='middle right',
#         name='End'))
    
#     fig_range_plot.update_layout(title="Data Availability", showlegend=False)    
#     return fig_range_plot




fig = go.Figure()#plot_data_of_sector('mobility')#go.Figure()
fig_range_plot =  generate_data_availability_plot('energy_households')




# # Data Availability Plot
# data_range = '''
#  Grade Start End
# 0 "Sector 1" 1990 2020
# 1 "Sector 2" 1999 2014
# 2 "Sector 3" 1994 2002
# 3 "Sector 4" 2001 2020
# 4 "Sector 5" 2003 2007
# 5 "Sector 6" 1990 2020
# 6 "Sector 7" 2001 2010
# 7 "Sector 8" 1994 2019
# 8 "Sector 9" 2003 2019
# 9 "Sector 10" 1997 2020
# '''
# max_sector_number=10

# df = pd.read_csv(io.StringIO(data_range), sep='\s+')
# df.sort_values('End', ascending=False, inplace=True, ignore_index=True)
    
    
# w_lbl = [str(s) for s in df['Start'].tolist()]
# m_lbl = [str(s) for s in df['End'].tolist()]

    
# for i in range(0,max_sector_number):
#     fig_range_plot.add_trace(go.Scatter(
#         x=[df['Start'][i],df['End'][i]],
#         y=[df['Grade'][i],df['Grade'][i]],
#         orientation='h',
#         line=dict(color='rgb(244,165,130)', width=8),
#              ))

# fig_range_plot.add_trace(go.Scatter(
#     x=df['Start'],
#     y=df['Grade'],
#     marker=dict(color='#CC5700', size=14),
#     mode='markers+text',
#     text=w_lbl,
#     textposition='middle left',
#     name='Start'))

# fig_range_plot.add_trace(go.Scatter(
#     x=df['End'],
#     y=df['Grade'],
#     marker=dict(color='#227266', size=14),
#     mode='markers+text',
#     text=m_lbl,
#     textposition='middle right',
#     name='End'))

# fig_range_plot.update_layout(title="Data Availability", showlegend=False)
    
    
    

# Set title and heigh
fig.update_layout(
    title_text="Time series with range slider and selectors",
    height=700
)

# Add range slider
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)




app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

server = app.server
app.config.suppress_callback_exceptions = True



# Read data
df = pd.read_csv(DATA_PATH.joinpath("clinical_analytics.csv"))


# clinic_list = df["Clinic Name"].unique()
df["Admit Source"] = df["Admit Source"].fillna("Not Identified")
admit_list = df["Admit Source"].unique().tolist()

#clinic_list = category_list

# Date
# Format checkin Time
df["Check-In Time"] = df["Check-In Time"].apply(
    lambda x: dt.strptime(x, "%Y-%m-%d %I:%M:%S %p")
)  # String -> Datetime

# Insert weekday and hour of checkin time
df["Days of Wk"] = df["Check-In Hour"] = df["Check-In Time"]
df["Days of Wk"] = df["Days of Wk"].apply(
    lambda x: dt.strftime(x, "%A")
)  # Datetime -> weekday string

df["Check-In Hour"] = df["Check-In Hour"].apply(
    lambda x: dt.strftime(x, "%I %p")
)  # Datetime -> int(hour) + AM/PM

day_list = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]



check_in_duration = df["Check-In Time"].describe()

# Register all departments for callbacks
all_departments = df["Department"].unique().tolist()
wait_time_inputs = [
    Input((i + "_wait_time_graph"), "selectedData") for i in all_departments
]
score_inputs = [Input((i + "_score_graph"), "selectedData") for i in all_departments]



def description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("AMI Projekt"),
            html.H3("2020 Group 6"),
            html.Div(
                id="intro",
                children="In the project, we used machine learning algorithms in order to predict and compare the greenhouse gas emissions in Germany with and without the impact of the COVID-19 pandemic. By comparing the two scenarios, we forecast the impact of the pandemic on Germany’s climate targets on a long-term basis and its effect on reaching the EU Climate Goals.",
                
            ),
        ],
    )


def generate_control_card():
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.P(),

            # html.Br(),
            # html.Div(id='dd-output-container'),
            
            # dcc.Dropdown(
            #     id="-select_co2_source",
            #     options=[{"label": i, "value": i} for i in sector_list],
            #     value=sector_list[0],
            # ),
            html.Br(),
            # html.P("Select Check-In Time"),
            # dcc.DatePickerRange(
            #     id="date-picker-select",
            #     start_date=dt(2014, 1, 1),
            #     end_date=dt(2014, 1, 15),
            #     min_date_allowed=dt(2014, 1, 1),
            #     max_date_allowed=dt(2014, 12, 31),
            #     initial_visible_month=dt(2014, 1, 1),
            # ),
            #html.Br(),
            # html.Br(),
            # html.P("Select Admit Source"),
            # dcc.Dropdown(
            #     id="admit-select",
            #     options=[{"label": i, "value": i} for i in admit_list],
            #     #value=admit_list[:],
            #     multi=True,
            # ),

            html.B("Prediction Controll"),
            html.Hr(),
            html.Br(),
            html.Label('Select Prediction Data:'),
            html.Br(),

                        
        dcc.Dropdown(
            id="Prediction_Selection",
                options=[
                    {'label': 'Mobility', 'value': 'Prediction_1'},
                    {'label': 'Energy', 'value': 'Prediction_2'},
                    {'label': 'Economy', 'value': 'Prediction_3'},
                    {'label': 'All', 'value': 'Prediction_4'}
                ],
                value='Prediction_1'
            ),
        
        
        
            # dcc.Checklist(
            #                 options=[
            #                     {'label': 'Mobility', 'value': 'NYC'},
            #                     {'label': u'Energy', 'value': 'MTL'},
            #                     {'label': 'Economy', 'value': 'SF'},
            #                     {'label': 'All', 'value': 'all'},
            #                 ],
            #  value=['MTL'],

            # ),
            
                    
                dcc.Store(id="store"),  
                dcc.Store(id="store2"),                                                                              
                            
                        
                        # html.Br(),
                        # html.Label('Datatype'),
                        # html.Hr(),
                        # html.Br(),
                        #     dcc.Dropdown(
                        #     options=[
                        #         {'label': 'DAX Data', 'value': 'NYC'},
                        #         {'label': u'Mobility Data', 'value': 'MTL'},
                        #         {'label': 'Transportation Cars Data', 'value': 'SF'}
                        #     ],
                        #     value='MTL'
                            
                            
                        # ),


                            
                        # html.Label('Multi-Select Dropdown'),
                                
                        # dcc.Dropdown(
                        #     options=[
                        #         {'label': 'New York City', 'value': 'NYC'},
                        #         {'label': u'Montréal', 'value': 'MTL'},
                        #         {'label': 'San Francisco', 'value': 'SF'}
                        #     ],
                        #     value=['MTL', 'SF'],
                        #     multi=True
                        # ),
                        # html.Label('Text Input'),
                        # dcc.Input(value='MTL', type='text'),
                        
                        
                        # html.Br(),
                        # html.Label('Slider'),
                        # html.Hr(),
                        # html.Br(),
                        # dcc.Slider(
                        #     min=0,
                        #     max=9,
                        #     marks={i: 'Infectionnumber'.format(i) if i == 1 else str(i) for i in range(1, 6)},
                        #     value=5,
                        # ),
                        # html.Br(),
                        # dcc.Slider(
                        #     min=0,
                        #     max=9,
                        #     marks={i: 'R-Value'.format(i) if i == 1 else str(i) for i in range(1, 6)},
                        #     value=2,
                        # ),
                        # daq.BooleanSwitch(
                        #   on=True,
                        #   label="Second Wave",
                        #   labelPosition="top",
                        #   id="button_second_wave",
                        # ),
                                                
                    
        
                        
                        html.Br(),
                        #html.Div(id="barchart"),
                        
                        # html.Div(
                        #     id="wait_time_card",
                        #     children=[
                        #     html.B("Data availability"),
                        #     html.Hr(),
                        #     dcc.graph(figure=plot_barchart([3,665,322,2542,23,5])),
                        #     ],
                        # ),
                        
                        html.Div(
                            #id="barchart",
                            id="barchart_plot"
                        ),             

                        html.Div(
                            id="chartplot_div",
                            children=[
                                    #html.B("Data availability"),
                                    #html.Hr(),
                            #html.Div(id="wait_time_table", children=initialize_table()),
                            #dcc.Graph(figure=fig_range_plot),
                            #dcc.Graph(figure=data["hist_1"]),
                            #dcc.Graph(figure=generate_data_availability_plot),
                            ],
                        ),

                        html.Label('Estimate Infectionrate from July to December 2020:'),
                        #html.Hr(),
                        html.Br(),
                        html.Br(),
                        
                        html.Div(
                            id="monthly_values",
                            children=[
                            # # daq.NumericInput(
                            # #         id="Month1",
                            # #         children="Month_c1",
                            # #         label='Label1',
                            # #         labelPosition='right',
                            # #         disabled=True,
                            # #         min=0,
                            # #         max=10,
                            # #         value=2
                            # #     ),  
                            # # daq.NumericInput(
                            # #         id="Month2",
                            # #         children="Month_c2",
                            # #         label='Label2',
                            # #         labelPosition='right',
                            # #         min=0,
                            # #         max=10,
                            # #         value=2
                            # #     ),  
                            # # daq.NumericInput(
                            # #         id="Month3",
                            # #         children="Month_c3",
                            # #         label='Label3',
                            # #         labelPosition='right',
                            # #         min=0,
                            # #         max=10,
                            # #         value=2
                            # #     ),  
                            # # daq.NumericInput(
                            # #         id="Month4",
                            # #         children="Month_c4",
                            # #         label='Label4',
                            # #         labelPosition='right',
                            # #         min=0,
                            # #         max=10,
                            # #         value=2
                            # #     ),  
                            # # daq.NumericInput(
                            # #         id="Month5",
                            # #         children="Month_c5",
                            # #         label='Label5',
                            # #         labelPosition='right',
                            # #         min=0,
                            # #         max=10,
                            # #         value=2
                            # #     ),  
                            # # daq.NumericInput(
                            # #         id="Month6",
                            # #         children="Month_c6",
                            # #         label='Label6',
                            # #         labelPosition='right',
                            # #         min=0,
                            # #         max=10,
                            # #         value=2
                            # #     ),   
                            # daq.NumericInput(
                            #         id="Month7",
                            #         children="Month_c7",
                            #         label='Label7',
                            #         labelPosition='right',
                            #         min=0,
                            #         max=100000,
                            #         value=2000
                            #     ),  
                            # daq.NumericInput(
                            #         id="Month8",
                            #         children="Month_c8",
                            #         label='Label8',
                            #         labelPosition='right',
                            #         min=0,
                            #         max=100000,
                            #         value=2000
                            #     ),  
                            # daq.NumericInput(
                            #         id="Month9",
                            #         children="Month_c9",
                            #         label='Label9',
                            #         labelPosition='right',
                            #         min=0,
                            #         max=100000,
                            #         value=2000
                            #     ),  
                            # daq.NumericInput(
                            #         id="Month10",
                            #         children="Month_c10",
                            #         label='Label10',
                            #         labelPosition='right',
                            #         min=0,
                            #         max=100000,
                            #         value=2000
                            #     ),  
                            # daq.NumericInput(
                            #         id="Month11",
                            #         children="Month_c11",
                            #         label='Label11',
                            #         labelPosition='right',
                            #         min=0,
                            #         max=100000,
                            #         value=2000
                            #     ),  
                            # daq.NumericInput(
                            #         id="Month12",
                            #         children="Month_c12",
                            #         label='Label12',
                            #         labelPosition='right',
                            #         min=0,
                            #         max=100000,
                            #         value=2000
                            #     ),   
                            # daq.Slider(
                            #     id="Month1",
                            #     min=0,
                            #     max=100,
                            #     value=50,
                            #     handleLabel={"showCurrentValue": True,"label": "Month1"},
                            #     step=10,
                            #     vertical=True
                            #     ), 
                            # daq.Slider(id="Month2", min=0,max=100,  value=50,handleLabel={"showCurrentValue": True,"label": "VALUE"},step=10,vertical=True),
                      
                                ],           
                        
                        ),
                        
                        dbc.Row(
                                     [
                                         # dbc.Col(daq.Slider(id="Month1", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "VALUE"},step=1000,vertical=True)),
                                         # dbc.Col(daq.Slider(id="Month2", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "VALUE"},step=1000,vertical=True)),
                                         # dbc.Col(daq.Slider(id="Month3", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "VALUE"},step=1000,vertical=True)),
                                         # dbc.Col(daq.Slider(id="Month4", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "VALUE"},step=1000,vertical=True)),
                                         # dbc.Col(daq.Slider(id="Month5", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "VALUE"},step=1000,vertical=True)),
                                         # dbc.Col(daq.Slider(id="Month6", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "VALUE"},step=1000,vertical=True)),    
                                         dbc.Col(daq.Slider(id="Month7", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "Juli"},step=1000,vertical=True)),
                                         dbc.Col(daq.Slider(id="Month8", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "August"},step=1000,vertical=True)),
                                         dbc.Col(daq.Slider(id="Month9", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "September"},step=1000,vertical=True)),
                                         dbc.Col(daq.Slider(id="Month10", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "Oktober"},step=1000,vertical=True)),
                                         dbc.Col(daq.Slider(id="Month11", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "November"},step=1000,vertical=True)),
                                         dbc.Col(daq.Slider(id="Month12", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "December"},step=1000,vertical=True)), 
                                     ]
                                 ),
            


                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Div(
                            id="reset-btn-outer",
                            children=[html.Button(id="reset-btn", children="Reset", n_clicks=0), html.Button(id="Update", children="Update", n_clicks=0), html.Button(id="Initialise", children="Initialisation", n_clicks=0),],
                        ),
                        
                        html.Br(),
                        dbc.Button(
                                "Generate Graphs",
                                color="primary",
                                block=True,
                                id="button",
                                className="mb-3",
                        ),
                        html.Br(),
                        html.B('Data Visualisation Control:'),
                        html.Hr(),
                        html.Br(),
                        dcc.Dropdown(
                            id="sector-select",
                            options=[{"label": i, "value": i} for i in sector_list],
                            value=sector_list[0],
                        ),
                        
            
        ],
    )


external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        # html.Div(
        #     id="banner",
        #     className="banner",
        #     children=[html.Img(src=app.get_asset_url("plotly_logo.png"))],
        # ),
        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[description_card(), generate_control_card()]
            + [
                html.Div(
                    ["initial child"], id="output-clientside", style={"display": "none"}
                )
            ],
        ),
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                # Patient Volume Heatmap
                #html.Div(id="patient_volume_card",
                    # children=[
                    #     html.B("Prediction"),
                    #     html.Hr(),
                    #     dbc.Tabs(
                    #             [
                    #             dbc.Tab(label="Data", tab_id="scatter"),
                    #             dbc.Tab(label="Prediction", tab_id="histogram"),
                    #             ],
                    #             id="tabs",
                    #             active_tab="scatter",
                    #         ),
                    #         html.Div(id="tab-content", className="p-4"),                                                                                                    

                    # ],
                #),
                
                
                  html.Div(
                             [
                                 dbc.Row(dbc.Col(html.Div(id="patient_volume_card",))),
                                 dbc.Row(
                                     [
                                         dbc.Col(html.Div("One of three columns")),
                                         dbc.Col(daq.LEDDisplay(label="color", value='1.001',color="#FF5E5E"), width=6),
                                         dbc.Col(daq.LEDDisplay(label="color", value='1.001',color="#FF5E5E"), width=6),
                                     ]
                                 ),
                             ]
                         ),
                                        
                                        
                                        
                                        
                                        
                # Availability of Data
                html.Div(
                    id="wait_time_card",
                    children=[
                        html.B("Data availability"),
                        html.Hr(),
                        #html.Div(id="wait_time_table", children=initialize_table()),
                        #dcc.Graph(figure=fig_range_plot),
                        #dcc.Graph(figure=data["hist_1"]),
                        #dcc.Graph(figure=generate_data_availability_plot),

                    ],
                ),
                
                
              

            ],
        ),
    ],
)










@app.callback(
    
    Output("barchart_plot", "children"),
    [Input("store2", "data")],
)

def render_chartplot(data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """

    children=[
                        html.Label("Estimate Infection Rate of COVID-19 in Germany:"),
                        #html.Hr(),
                        #html.Br(),
                        
                        #dbc.Col(dcc.Graph(figure=plot_barchart([3,665,322,2542,23,5])), width=6),
                        dbc.Col(dcc.Graph(figure=data['barchart']), width=6),
        
        ]

    return children




@app.callback(
    Output("patient_volume_card", "children"),
    [Input("store", "data")],
)
def render_tab1_content(data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """

    children=[                        
                        dbc.Col(dcc.Graph(figure=data["hist_1"]), width=6),
                       # dbc.Col(dcc.Graph(figure=data["barchart_fallzahl"]), width=6),
                        # daq.Gauge(
                        #   id='my-daq-gauge',
                        #   min=0,
                        #   max=10,
                        #   value=6
                        # ),
                        # daq.Thermometer(
                        #   id='my-daq-thermometer',
                        #   min=95,
                        #   max=105,
                        #   value=98.6
                        # ),
 

                       
                                                
                                                
                        # dbc.Row(
                        # [
                        #     dbc.Col(daq.LEDDisplay(label="color", value='1.001',color="#FF5E5E"), width=6),
                        #     dbc.Col(daq.LEDDisplay(label="color", value='1.001',color="#FF5E5E"), width=6),
                        # ]
                        # )
                       # html.Div(
                       #     daq.LEDDisplay(label="color", value='1.001',color="#FF5E5E"),
                       #     daq.LEDDisplay(label="color", value='1.001',color="#FF5E5E"),
                       #     style={'display': 'inline-block'}
                       #     ),

                       
                       

        ]

    return children


                
                
                
                
                
                

@app.callback(
    Output("wait_time_card", "children"),
    [Input("store", "data")],
)
def render_tab2_content(data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """

    children=[
                        html.B("Data Visualisation"),
                        html.Hr(),
                        
                        #dcc.Graph(figure=data["scatter"],
                        #dcc.Graph(figure=data["hist_2"],
                        dbc.Row(
                        [
                            dcc.Graph(figure=data["scatter"]),
                         
                            dcc.Graph(figure=data["hist_2"]),
                        ]
                        
                        
                        
                        
                        )
        ]

    return children




# @app.callback(
#     Output("tab-content", "children"),
#     [Input("tabs", "active_tab"), Input("store", "data")],
# )
# def render_tab_content(active_tab, data):
#     """
#     This callback takes the 'active_tab' property as input, as well as the
#     stored graphs, and renders the tab content depending on what the value of
#     'active_tab' is.
#     """
#     if active_tab and data is not None:
#         if active_tab == "scatter":

#             return dbc.Row(
#                 [
#                     dbc.Col(dcc.Graph(figure=data["scatter"]), width=6),
#                     dbc.Col(dcc.Graph(figure=data["hist_2"]), width=6),
#                 ]
#                 )
                
                
        
#         elif active_tab == "histogram":
#             return dbc.Row(
#                 [
#                     dbc.Col(dcc.Graph(figure=data["hist_1"]), width=6),
#                     #dbc.Col(dcc.Graph(figure=data["hist_2"]), width=6),
#                 ]
#             )
#     return "No tab selected"




@app.callback(Output(component_id="store", component_property="data"), 
   [
    Input(component_id="button", component_property="n_clicks"),
    Input(component_id="Prediction_Selection", component_property="value"),
    Input('sector-select', 'value'),
    ])

def generate_graphs(n, radio_button, val):
    """
    This callback generates three simple graphs from random data.
    """
    # if not n:
    #      #generate empty graphs when app loads
    #     return {k: go.Figure(data=[]) for k in ["scatter", "hist_1", "hist_2"]}

    # # simulate expensive graph generation process
    # time.sleep(2)
        
    
    # #Graphtest function
    
    # x = ['2015-02-17','2015-02-18','2015-02-19','2015-02-20','2015-02-23','2015-02-24','2015-02-25','2015-02-26','2015-02-27','2015-03-02']

    # x_rev = x[::-1]
    
    # # Line 1
    # y1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # y1_upper = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11]
    # y1_lower = [1, 2, 3, 4, 4, 5, 6, 7, 8, 9]
    # y1_lower = y1_lower[::-1]
    
    # # Line 2
    # y2 = [5, 2.5, 5, 7.5, 5, 2.5, 7.5, 4.5, 5.5, 5]
    # y2_upper = [5.5, 3, 5.5, 8, 6, 3, 8, 5, 6, 5.5]
    # y2_lower = [4.5, 2, 4.4, 7, 4, 2, 7, 4, 5, 4.75]
    # y2_lower = y2_lower[::-1]
    
    # # Line 3
    # y3 = [10, 8, 6, 4, 2, 0, 2, 4, 2, 0]
    # y3_upper = [11, 9, 7, 20, 3, 1, 3, 5, 3, 1]
    # y3_lower = [9, 7, 5, 3, 1, -.5, 1, 3, 1, -1]
    # y3_lower = y3_lower[::-1]
    
    
    # # Line 4
    # y4 = [10, 8, 6, 4, 5, 0, 2, 4, 2, 0]
    # y4_upper = [11, 9, 7, 20, 3, 1, 3, 5, 3, 1]
    # y4_lower = [9, 7, 5, 3, 1, -.5, 1, 3, 1, -1]
    # y4_lower = y3_lower[::-1]

  #  df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
  #  fig = go.Figure([go.Scatter(x=df['Date'], y=df['AAPL.High'])])
    #fig.show()

    
    # fig.data = []
    
    # # fig.add_trace(go.Scatter(
    # #     x=df['Date'], y=df['AAPL.High'],
    # #     line_color='rgb(231,107,243)',
    # #     name='Ideal',
    # # ))
    




    # fig.add_trace(go.Scatter(
    #     x=x+x_rev,
    #     y=y3_upper+y3_lower,
    #     fill='toself',
    #     fillcolor='rgba(231,107,243,0.2)',
    #     line_color='rgba(255,255,255,0)',
    #     showlegend=False,
    #     name='Ideal',
    # ))
    # fig.add_trace(go.Scatter(
    #     x=x, y=y3,
    #     line_color='rgb(231,107,243)',
    #     name='Ideal',
    # ))


    # fig.add_trace(go.Scatter(
    #     x=x+x_rev,
    #     y=y1_upper+y1_lower,
    #     fill='toself',
    #     fillcolor='rgba(0,100,80,0.2)',
    #     line_color='rgba(255,255,255,0)',
    #     showlegend=False,
    #     name='Fair',
    # ))
    # fig.add_trace(go.Scatter(
    #     x=x+x_rev,
    #     y=y2_upper+y2_lower,
    #     fill='toself',
    #     fillcolor='rgba(0,176,246,0.2)',
    #     line_color='rgba(255,255,255,0)',
    #     name='Premium',
    #     showlegend=False,
    # ))
    
    
    # fig.add_trace(go.Scatter(
    #     x=x, y=y1,
    #     line_color='rgb(0,100,80)',
    #     name='Fair',
    # ))
    # fig.add_trace(go.Scatter(
    #     x=x, y=y2,
    #     line_color='rgb(0,176,246)',
    #     name='Premium',
    # ))
    
    
    # fig.update_traces(mode='lines')
    # #fig.show()

#    fig = plot_data_of_sector('energy_households')



    # # generate 100 multivariate normal samples
    # data = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], 100)

    # scatter = go.Figure(
    #     data=[go.Scatter(x=data[:, 0], y=data[:, 1], mode="markers")]
    # )
    #value='target_values'
    scatter = plot_data_of_sector(val)
    scatter.update_layout(
        autosize=True,
        #width=1200,
        #height=900,
        #paper_bgcolor='rgba(0,0,0,0)',
        #plot_bgcolor='rgba(0,0,0,0)'
        )
 
 
    hist_1 = plot_prediction_data(radio_button)
    hist_2 = generate_data_availability_plot(val)

    # save figures in a dictionary for sending to the dcc.Store
    return {"scatter": scatter, "hist_1": hist_1, "hist_2": hist_2}



# @app.callback(
#     Output('dd-output-container', 'children'),
#     [Input('sector-select', 'value')])
# def update_output(value):
#     Data_plot_name=value
#     print(value)
#     return 'You have selected "{}"'.format(Data_plot_name)


@app.callback(Output(component_id="store2", component_property="data"),
                        [
                          # Input('Month1', 'value'),
                          # Input('Month2', 'value'),
                          # Input('Month3', 'value'),
                          # Input('Month4', 'value'),
                          # Input('Month5', 'value'),
                          # Input('Month6', 'value'),
                          Input('Month7', 'value'),
                          Input('Month8', 'value'),
                          Input('Month9', 'value'),
                          Input('Month10', 'value'),
                          Input('Month11', 'value'),
                          Input('Month12', 'value'),
                   
                    ])
                    
                    
def on_click(v7,v8,v9,v10,v11,v12):

        # Give a default data dict with 0 clicks if there's no data.
        v1=5
        v2=52
        v3=61856
        v4=97206
        v5=22363
        v6=12777
        monat_value=[5,52,61856,97206,22363,12777,v7,v8,v9,v10,v11,v12],
        #monat_value=[3,665,322,2542,23,5],
        #data = {'barchart_plot': plot_barchart([3,665,322,2542,23,5])},
        #print(data['barchart_plot']),
        #fig=plot_barchart([3,665,322,2542,23,5]),
        #fig=generate_data_availability_plot('mobility')
        fig=  go.Figure(
        data=[go.Bar(x=["2020-01","2020-02","2020-03","2020-04","2020-05","2020-06","2020-07","2020-08","2020-09","2020-10","2020-11","2020-12"],y=[v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12])],
        layout_title_text="Infectionrate"
        )
        fig.update_layout(
        autosize=True,
        width=700,
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        #plot_bgcolor='rgba(0,0,0,0)'
        )

        
        d = {'date':["2020-07","2020-08","2020-09","2020-10","2020-11","2020-12"], 'cases': [v7,v8,v9,v10,v11,v12]}
        
        df_slider_estimation = pd.DataFrame(data=d)
        df_slider_estimation.index=df_slider_estimation['date']
        
        #trained_values=EstimateCO2withCorona(lr_cor_co2,df_slider_estimation,Sarima_mobility),
        trained_values=23
        
        
        d = {'date':["2020-07","2020-08","2020-09","2020-10","2020-11","2020-12"], 'cases': [v7,v8,v9,v10,v11,v12]}
        
        df_slider_estimation = pd.DataFrame(data=d)
        df_slider_estimation.index=df_slider_estimation['date']
                
        trained_values_wrongformat=EstimateCO2withCorona(lr_cor_co2,df_slider_estimation,Sarima_mobility),
        
        trained_values= {'cases': [13.041935514899228,13.167659103529827,13.669042942906339,13.532680100891733,13.031704074531671,12.036724563547219]}
        df_trained_values = pd.DataFrame(data=trained_values)
        df_trained_values.index=["2020-07","2020-08","2020-09","2020-10","2020-11","2020-12"]
                
        
        prediction_figure_slider=plot_prediction_silder('energy')
        
                

        
        return {"barchart": fig, "monat_value":monat_value, "trained_values":trained_values, "prediction_figure_slider": prediction_figure_slider}

    
    
    
# @app.callback(
#     Output("patient_volume_card", "children"),
#     [Input("store", "data")],
# )
# def render_tab1_content(data):
#     """
#     This callback takes the 'active_tab' property as input, as well as the
#     stored graphs, and renders the tab content depending on what the value of
#     'active_tab' is.
#     """

#     children=[
#                         html.B("Prediction"),
#                         html.Hr(),
                        
#                         dbc.Col(dcc.Graph(figure=data["hist_1"]), width=6),
#                        # dbc.Col(dcc.Graph(figure=data["barchart_fallzahl"]), width=6),
        
#         ]

#     return children    

# @app.callback(
#     Output('barchart', 'children'),
#     [Input('Month1', 'value'),
#      Input('Month2', 'value'),
#      Input('Month3', 'value'),
#      Input('Month4', 'value'),
#      Input('Month5', 'value'),
#      Input('Month6', 'value'),
      
#      ]
    
#     )
# def plot_barchart_callback(v1,v2,v3,v4,v5,v6):
    
#     monat_value=[v1,v2,v3,v4,v5,v6],
#     #chart_plot=plot_barchart([3,665,322,2542,23,5])
#     children=[
#         html.B("Data availability"),
#         html.Hr(),
#         dcc.graph(),
#         ],
    
#     return children



# @app.callback(Output(component_id="store2", component_property="data"), 
#    [
#     #Input(component_id="button", component_property="n_clicks"),
#     #Input(component_id="Prediction_Selection", component_property="value"),
#     #Input('sector-select', 'value'),
#     Input('Month1', 'value'),
#     Input('Month2', 'value'),
#     Input('Month3', 'value'),
#     Input('Month4', 'value'),
#     Input('Month5', 'value'),
#     Input('Month6', 'value'),
#     ])

# def plot_barchart_callback(v1,v2,v3,v4,v5,v6):
#     """
#     This callback generates three simple graphs from random data.
#     """
#     # if not n:
#     #      #generate empty graphs when app loads
#     #     return {k: go.Figure(data=[]) for k in ["scatter", "hist_1", "hist_2"]}

#     # # simulate expensive graph generation process
#     # time.sleep(2)
#     monat_value=[v1,v2,v3,v4,v5,v6]
#     barchartplot = plot_barchart(monat_value)
 
 

#     # save figures in a dictionary for sending to the dcc.Store
#     return {"barchart_fallzahl": barchartplot}

                            

# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
