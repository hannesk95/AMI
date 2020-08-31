#%%

import numpy as np
import pandas as pd

import datetime
from datetime import datetime as dt
import pathlib


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction, State
import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.graph_objs as go
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import json
import io

import warnings
warnings.filterwarnings("ignore")


from src.MappingMobility import featureMapping
from src.CoronaMapping import TrainLRCoronaOnCO2, EstimateCO2withCorona
from src.ImpactOfSavedCO2 import ImpactOfReduction
from src.Sarima_gui import Sarima
from src.ReadEnergyValues import ReadEnergyValues

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()
DATA_PATH_SRC = BASE_PATH.joinpath("src").resolve()

global Data_plot_name
Data_plot_name ='economy'

#Import Data 
category_list=[];
sector_list=[];


#open Data_Path
with open(DATA_PATH.joinpath("feature_database_gui.json")) as json_file:
    database_gui = json.load(json_file)

with open(DATA_PATH.joinpath("feature_database.json")) as json_file:
    database = json.load(json_file)

#read energy values for 2011 to 06/2020
df_energy = ReadEnergyValues(database)
df_energy = df_energy.loc[:'2020-06']

# Do Machine Learning Allgorithm
df_co2 = featureMapping(database)
df_cor = pd.read_csv(DATA_PATH.joinpath("CORONA_GERMANY.csv"))
df_cor = df_cor.rename(columns={'myDt': 'date'})
df_cor.index = df_cor.date
df_cor = df_cor.drop('date', axis=1)

sector = 'mobility' #oder/'energy'
#Sarima_nn = Sarima(database, sector, period=24)
Sarima_mobility = Sarima(database, sector, period=24)#co2 ohne corona
sector = 'energy' #oder/'energy'
Sarima_energy = Sarima(database, sector, period=12)
lr_cor_co2_mobility = TrainLRCoronaOnCO2(df_cor, df_co2) #im storage ablegen
lr_cor_co2_energy = TrainLRCoronaOnCO2(df_cor, df_energy) #im storage ablegen



# Load Data Base
for i in database_gui:
  feature = database_gui.get(i)
  if feature['category'] not in category_list:
    category_list.append(feature['category'])
for i in database_gui:
  feature = database_gui.get(i)
  if feature['sector'] not in sector_list:
    sector_list.append(feature['sector'])


#Subprograms
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
  fig = px.bar(x=df['Month'], y=df['Value'], labels={'x':'', 'y':'Total Number'})

  return fig

def get_min_max_date(sector_choice):
  X_eco_raw = None 
  data_name_list=[]
  list_empty = []
  data_min_max_full_header = {'Category':list_empty, 'Sector': list_empty,'Data_name': list_empty,'Start': list_empty,'End': list_empty, 'Selected': list_empty}
  data_min_max_full = pd.DataFrame(data=data_min_max_full_header)

  for cat in category_list:
    for sect in sector_list:

        for i in database_gui:
            feature = database_gui.get(i)
            
            if feature['sector'] == sect and feature['category'] == cat:
                new_data = pd.read_json(database_gui[i]['data'])

                new_data_name=new_data.columns.tolist()
                new_data_name=''.join(new_data_name)
                #data_name_list.extend(new_data_name)
                df = pd.DataFrame(new_data)
                min_date=min(df.index)
                max_date=max(df.index)

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
        
    #fig_range_plot.update_layout(title="Data Availability", showlegend=False, autosize=True)
    fig_range_plot.update_layout(paper_bgcolor='rgba(0,0,0,0)',showlegend=False, height=550)    #Dataavailabilityplot
      
    return fig_range_plot

def plot_prediction_data_slider(Prediction_type,trained_values, df_co2):
    pd.set_option('display.max_rows', None)

    if Prediction_type == 'energy':
        Prediction=Sarima_energy  
        Prediction_type_titel='Prediction based on Energy'
        trained_values_joined_complete=pd.concat([df_energy, trained_values])
    if Prediction_type == 'mobility':
        Prediction=Sarima_mobility
        Prediction_type_titel='Prediction based on Mobility'
        trained_values_joined_complete=pd.concat([Sarima_mobility.loc[:'2020-01'], df_co2.loc['2020-02':], trained_values])

    fig_data_of_sector = go.Figure()
    trained_values_joined=pd.concat([df_co2[-1:], trained_values])
    
    #trained_values_joined_complete=pd.concat([df_co2, trained_values])
    x_data1 = df_co2.index #['2015-02-17','2015-02-18','2015-02-19','2015-02-20','2015-02-23','2015-02-24','2015-02-25','2015-02-26','2015-02-27','2015-03-02']
    y_data2 = Sarima_energy['co2'][0:len(df_co2['co2'])]

    fig_data_of_sector.add_trace(go.Scatter(
        x=trained_values_joined_complete.index, y=trained_values_joined_complete['co2'],
        line_color='rgb(255,100,80)',
        name='CO2 Emission Aproximation with COVID-19',
        
    ))

    fig_data_of_sector.add_trace(go.Scatter(
        x=Prediction.index, y=Prediction['co2'],
        line_color='rgb(56,100,80)',
        name='CO2 Emission Aproximation without COVID-19 [Mio. Tons]',
        fill='tonexty'
    ))
    

    fig_data_of_sector.update_layout(title=Prediction_type_titel, showlegend=True, height=800)
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
    initial_range = ['2018-01', '2020-12']
    fig_data_of_sector['layout']['xaxis'].update(range=initial_range)
        
    return fig_data_of_sector

def plot_data_of_sector(Sector):
    if Sector == 'economy':
        Sector_titel='Economy'
    if Sector == 'mobility':
        Sector_titel='Mobility'
    if Sector == 'energy_households': 
        Sector_titel='Energy & Households'
    if Sector == 'target_values':
        Sector_titel='Real CO2 Data'
 
     # Concat data from sector economy
    X_eco_raw = None 
    for i in database_gui:
        feature = database_gui.get(i)
        if feature['sector'] == Sector:
            new_data = pd.read_json(database_gui[i]['data'])
            if X_eco_raw is None:
                X_eco_raw = new_data
            else:
                X_eco_raw = pd.concat([X_eco_raw, new_data], axis=1, join="outer")
    
    #convert index in datetime format
    X_eco_raw['date'] = X_eco_raw.index
    X_eco_raw.head()
    fig_data_of_sector = go.Figure()
    for col in X_eco_raw.columns:
        fig_data_of_sector.add_trace(go.Scatter(x=X_eco_raw.index, y=X_eco_raw[col], name=col))

    fig_data_of_sector.update_layout(title=Sector_titel, showlegend=True, height=700)
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
    
    initial_range = ['2017-01', '2020-12']
    fig_data_of_sector['layout']['xaxis'].update(range=initial_range)

    return fig_data_of_sector


    

fig = go.Figure()#plot_data_of_sector('mobility')#go.Figure()
fig_range_plot =  generate_data_availability_plot('energy_households')



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
            visible=True,
        ),
        type="date"
    )
)
initial_range = ['2017-01', '2020-12']
fig['layout']['xaxis'].update(range=initial_range)


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

server = app.server
app.config.suppress_callback_exceptions = True



# # Read data
# df = pd.read_csv(DATA_PATH.joinpath("clinical_analytics.csv"))


# # clinic_list = df["Clinic Name"].unique()
# df["Admit Source"] = df["Admit Source"].fillna("Not Identified")
# admit_list = df["Admit Source"].unique().tolist()

# #clinic_list = category_list

# # Date
# # Format checkin Time
# df["Check-In Time"] = df["Check-In Time"].apply(
#     lambda x: dt.strptime(x, "%Y-%m-%d %I:%M:%S %p")
# )  # String -> Datetime

# # Insert weekday and hour of checkin time
# df["Days of Wk"] = df["Check-In Hour"] = df["Check-In Time"]
# df["Days of Wk"] = df["Days of Wk"].apply(
#     lambda x: dt.strftime(x, "%A")
# )  # Datetime -> weekday string

# df["Check-In Hour"] = df["Check-In Hour"].apply(
#     lambda x: dt.strftime(x, "%I %p")
# )  # Datetime -> int(hour) + AM/PM

# day_list = [
#     "Monday",
#     "Tuesday",
#     "Wednesday",
#     "Thursday",
#     "Friday",
#     "Saturday",
#     "Sunday",
# ]



# check_in_duration = df["Check-In Time"].describe()

# # Register all departments for callbacks
# all_departments = df["Department"].unique().tolist()
# wait_time_inputs = [
#     Input((i + "_wait_time_graph"), "selectedData") for i in all_departments
# ]
# score_inputs = [Input((i + "_score_graph"), "selectedData") for i in all_departments]



# def description_card():
#     """

#     :return: A Div containing dashboard title & descriptions.
#     """
#     return html.Div(
#         id="description-card",
#         children=[
#             html.H5("AMI Projekt"),
#             html.H3("2020 Group 10"),
#             html.Label("In the project, we used machine learning algorithms in order to predict and compare the greenhouse gas emissions in Germany with and without the impact of the COVID-19 pandemic. By comparing the two scenarios, we forecast the impact of the pandemic on Germany’s climate targets on a long-term basis and its effect on reaching the EU Climate Goals.",
# ),
#         ],
#     )


def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        
        id="control-card",
        children=[
            html.H5("AMI Projekt"),
            html.H3("2020 Group 10"),
            #html.Label(""),
            dbc.Row(
            [
  
                dbc.Col(html.Label(html.Label("In the project, we used machine learning algorithms in order to predict and compare the greenhouse gas emissions in Germany with and without the impact of the COVID-19 pandemic. By comparing the two scenarios, we forecast the impact of the pandemic on Germany’s climate targets on a long-term basis and its effect on reaching the EU Climate Goals."))),

                
            ]
            ),
                                    
                                    
            # dcc.Markdown('''
            # In the project, we used machine learning algorithms in order to predict
            # and compare the greenhouse gas emissions in Germany with and without 
            # the impact of the COVID-19 pandemic. By comparing the two scenarios, we 
            # forecast the impact of the pandemic on Germany’s climate targets on a 
            # long-term basis and its effect on reaching the EU Climate Goals.
            # '''),
            
            
            html.P(),
            html.Br(),
            html.B("Prediction Controll:"),
            html.Hr(),
            html.Br(),
            html.Label('Select Prediction Data:'),
            html.Br(),
               
            dcc.Dropdown(
                id="Prediction_Selection",
                    options=[
                        {'label': 'Mobility', 'value': 'mobility'},
                        {'label': 'Energy', 'value': 'energy'},
                        #{'label': 'Economy', 'value': 'Prediction_3'},
                        #{'label': 'All', 'value': 'Prediction_4'}
                    ],
                    value='mobility'
                ),

            dcc.Store(id="store"),  
            dcc.Store(id="store2"),                                                                              
      
            html.Br(),     
            html.Div(
                            #id="barchart",
                            id="barchart_plot"
                        ),             


                        html.Label('Estimate Infectionrate from July to December 2020:'),
                        #html.Hr(),
                        html.Br(),
                        html.Br(),
                        
                        # html.Div(
                        #     id="monthly_values",
                        #     children=[
                                           
                        #         ],           
                        
                        # ),
                        
                        dbc.Row(
                                     [
                                         # dbc.Col(daq.Slider(id="Month1", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "VALUE"},step=1000,vertical=True)),
                                         # dbc.Col(daq.Slider(id="Month2", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "VALUE"},step=1000,vertical=True)),
                                         # dbc.Col(daq.Slider(id="Month3", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "VALUE"},step=1000,vertical=True)),
                                         # dbc.Col(daq.Slider(id="Month4", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "VALUE"},step=1000,vertical=True)),
                                         # dbc.Col(daq.Slider(id="Month5", min=0,max=100000,  value=50,handleLabel={"showCurrentValue": True,"label": "VALUE"},step=1000,vertical=True)),
                                         dbc.Col(),    
                                         dbc.Col(daq.Slider(id="Month7", min=0,max=90000,  value=4000,handleLabel={"showCurrentValue": True,"label": "July"},step=1000,vertical=True)),
                                         dbc.Col(daq.Slider(id="Month8", min=0,max=90000,  value=2000,handleLabel={"showCurrentValue": True,"label": "August"},step=1000,vertical=True)),
                                         dbc.Col(daq.Slider(id="Month9", min=0,max=90000,  value=1000,handleLabel={"showCurrentValue": True,"label": "September"},step=1000,vertical=True)),
                                         dbc.Col(daq.Slider(id="Month10", min=0,max=90000,  value=200,handleLabel={"showCurrentValue": True,"label": "October"},step=1000,vertical=True)),
                                         dbc.Col(daq.Slider(id="Month11", min=0,max=90000,  value=50,handleLabel={"showCurrentValue": True,"label": "November"},step=1000,vertical=True)),
                                         dbc.Col(daq.Slider(id="Month12", min=0,max=90000,  value=50,handleLabel={"showCurrentValue": True,"label": "December"},step=1000,vertical=True)), 
                                     ]
                                 ),
            


                        html.Br(),
                        html.Br(),
                        html.Br(),
                        # html.Div(
                        #     id="reset-btn-outer",
                        #     children=[html.Button(id="reset-btn", children="Reset", n_clicks=0), html.Button(id="Update", children="Update", n_clicks=0), html.Button(id="Initialise", children="Initialisation", n_clicks=0),],
                        # ),
                        
                        html.Br(),
                        # dbc.Button(
                        #         "Generate Graphs",
                        #         color="primary",
                        #         block=True,
                        #         id="button",
                        #         className="mb-3",
                        # ),
                        # dbc.Button(
                        #         "Apply Allgorithm",
                        #         color="primary",
                        #         block=True,
                        #         id="button1",
                        #         className="mb-3",
                        # ),
                        html.Br(),
                        html.B('Data Visualisation:'),
                        html.Hr(),
                        html.Br(),
                        html.Label('Select Data Sector:'),
                        html.Br(),
                        dcc.Dropdown(
                            id="sector-select",

                            options=[
                                {'label': 'Mobility', 'value': sector_list[0]},
                                {'label': 'Economy', 'value': sector_list[1]},
                                {'label': 'Energy & Households', 'value': sector_list[2]},
                                {'label': 'Real CO2', 'value': sector_list[3]},
                            ],
                                                
                            value=sector_list[0],
                        ),
                        html.Br(),
                        html.Label('Data Availability:'),
                        html.Div(
                            id="wait_time_card_timeplot",
                            children=[
                                ],
                        ),
                        
            
        ],
    )


external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



app.layout = html.Div(
    id="app-container",
    children=[
        #Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Div(html.Img(src=app.get_asset_url("8_tum.svg"), style={'height':'12%', 'width':'12%'}))],

        ),
        #Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[generate_control_card()]
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
    
                  html.Div(
                             [
                                 dbc.Row(dbc.Col(html.Div(id="patient_volume_card",))),  
                             ]
                         ),

                # Availability of Data
                html.Div(
                    id="wait_time_card",
                    children=[
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
                        dcc.Graph(figure=data['barchart']),
        
        ]

    return children




@app.callback(
    Output("patient_volume_card", "children"),
    [Input("store2", "data")],
)
def render_tab1_content(data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """

    children=[                        
                        
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
                       html.B("Prediction:"),
                       html.Hr(),
                       html.Div(
                            [
                                dbc.Row(dbc.Col(dcc.Graph(figure=data["prediction_figure_plot"]))),
                                dbc.Row(
                                    [
                                        dbc.Col(html.Div(daq.LEDDisplay(label="\u0394 CO2 [Mio. Tons]", value=round(data['delta_CO2_in_MioTons'],2),color="#FF5E5E"))),
                                        dbc.Col(html.Div(daq.LEDDisplay(label="Days of emission of \u0394 CO2", value=round(data['savedEmission_in_Days'],2),color="#FF5E5E"))),
                                        dbc.Col(html.Div(daq.LEDDisplay(label="\u0394 C [ppb]", value=round(data['delta_C_in_ppm']*1000,2),color="#FF5E5E"))),
                                        dbc.Col(html.Div(daq.LEDDisplay(label="\u0394 T [\u03BC ° K]", value=round(data['delta_T_in_GradK']*(10**6),2),color="#FF5E5E"))),
                                        
                                    ]
                                ),
                            ]
                        )        

        ]

    return children


                
                
                
                
@app.callback(
    Output("wait_time_card_timeplot", "children"),
    [Input("store", "data")],
)
def render_card_timeplot_content(data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """

    children=[
   
                        html.Div(
                            [
                                dbc.Row(dbc.Col(dcc.Graph(figure=data["hist_2"]))),
                            ]
                        )    
                           
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
                        html.B("Data Visualisation:"),
                        html.Hr(),
                        html.Div(
                            [
                                dbc.Row(dbc.Col(dcc.Graph(figure=data["scatter"]))),
                                #dbc.Row(dbc.Col(dcc.Graph(figure=data["hist_2"]))),
                            ]
                        )    
                        
        ]

    return children




@app.callback(Output(component_id="store", component_property="data"), 
   [
    #Input(component_id="button", component_property="n_clicks"),
    #Input(component_id="Prediction_Selection", component_property="value"),
    Input('sector-select', 'value'),
    ])

def generate_graphs(val):

    scatter = plot_data_of_sector(val)
    scatter.update_layout(
        autosize=True,
        #width=1200,
        height=800,
        #paper_bgcolor='rgba(0,0,0,0)',
        #plot_bgcolor='rgba(0,0,0,0)'
        )
 
    hist_1 = generate_data_availability_plot(val)
    hist_2 = generate_data_availability_plot(val)

    # save figures in a dictionary for sending to the dcc.Store
    return {"scatter": scatter, "hist_1": hist_1, "hist_2": hist_2}


@app.callback(Output(component_id="store2", component_property="data"),
                        [
                          Input('Month7', 'value'),
                          Input('Month8', 'value'),
                          Input('Month9', 'value'),
                          Input('Month10', 'value'),
                          Input('Month11', 'value'),
                          Input('Month12', 'value'),
                          Input(component_id="Prediction_Selection", component_property="value"),
                   
                    ])
                    
                    
def on_click(v7,v8,v9,v10,v11,v12,Prediction_type):

        monat_value=[5,52,61856,97206,22363,12777,v7,v8,v9,v10,v11,v12],
        
        fig=  go.Figure(
        data=[go.Bar(x=["2020-01","2020-02","2020-03","2020-04","2020-05","2020-06","2020-07","2020-08","2020-09","2020-10","2020-11","2020-12"],y=[5,52,61856,97206,22363,12777,v7,v8,v9,v10,v11,v12])],
        #layout_title_text="Infectionrate"
        )
        fig.update_layout(
        autosize=True,
        # width=700,
        height=330,
        paper_bgcolor='rgba(0,0,0,0)',
        #plot_bgcolor='rgba(0,0,0,0)'
        )


        d = {'cases': [v7,v8,v9,v10,v11,v12]}
                
        df_slider_estimation = pd.DataFrame(data=d)
        df_slider_estimation.index=["2020-07","2020-08","2020-09","2020-10","2020-11","2020-12"]
        
        if Prediction_type == 'energy':
            Prediction=Sarima_energy 
            trained_values=EstimateCO2withCorona(lr_cor_co2_energy,df_slider_estimation,Sarima_energy)

            trained_values_joined = pd.concat([df_energy, trained_values])
            trained_values_joined = trained_values_joined.rename(columns={'co2': 'co2_Cor'})
            print(trained_values_joined)
        if Prediction_type == 'mobility':
            Prediction=Sarima_mobility
            trained_values=EstimateCO2withCorona(lr_cor_co2_mobility,df_slider_estimation,Sarima_mobility)

            trained_values_joined = pd.concat([df_co2, trained_values])
            trained_values_joined = trained_values_joined.rename(columns={'co2': 'co2_Cor'})
       

        prediction_figure_slider = plot_prediction_data_slider(Prediction_type,trained_values,df_co2) 

        Sarima_temp = Prediction.rename(columns={'co2': 'co2_noCor'})
        Impact = ImpactOfReduction(trained_values_joined, Sarima_temp)
        

        return {"barchart": fig, "monat_value":monat_value, "prediction_figure_plot": prediction_figure_slider, "delta_CO2_in_MioTons":Impact["delta_CO2_in_MioTons"], "delta_C_in_ppm":Impact["delta_C_in_ppm"] ,"delta_T_in_GradK":Impact["delta_T_in_GradK"],"savedEmission_in_Days":Impact["savedEmission_in_Days"]}

# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
