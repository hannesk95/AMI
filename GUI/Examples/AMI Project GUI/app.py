import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction

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


# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()






#Import Data from json FIle
category_list=[];
sector_list=[];

#open Data_Path

with open(DATA_PATH.joinpath("feature_database.json")) as json_file:
    database = json.load(json_file)



for i in database:
  feature = database.get(i)
  if feature['category'] not in category_list:
    category_list.append(feature['category'])


for i in database:
  feature = database.get(i)
  if feature['sector'] not in sector_list:
    sector_list.append(feature['sector'])






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
                X_eco_raw = pd.concat([X_eco_raw, new_data], axis=1, join="inner")
    
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
    return fig_data_of_sector

fig = go.Figure()#plot_data_of_sector('mobility')#go.Figure()
fig_range_plot = go.Figure()



# Data Availability Plot
data_range = '''
 Grade Start End
0 "Sector 1" 1990 2020
1 "Sector 2" 1999 2014
2 "Sector 3" 1994 2002
3 "Sector 4" 2001 2020
4 "Sector 5" 2003 2007
5 "Sector 6" 1990 2020
6 "Sector 7" 2001 2010
7 "Sector 8" 1994 2019
8 "Sector 9" 2003 2019
9 "Sector 10" 1997 2020
'''
max_sector_number=10

df = pd.read_csv(io.StringIO(data_range), sep='\s+')
df.sort_values('End', ascending=False, inplace=True, ignore_index=True)
    
    
w_lbl = [str(s) for s in df['Start'].tolist()]
m_lbl = [str(s) for s in df['End'].tolist()]

    
for i in range(0,max_sector_number):
    fig_range_plot.add_trace(go.Scatter(
        x=[df['Start'][i],df['End'][i]],
        y=[df['Grade'][i],df['Grade'][i]],
        orientation='h',
        line=dict(color='rgb(244,165,130)', width=8),
             ))

fig_range_plot.add_trace(go.Scatter(
    x=df['Start'],
    y=df['Grade'],
    marker=dict(color='#CC5700', size=14),
    mode='markers+text',
    text=w_lbl,
    textposition='middle left',
    name='Start'))

fig_range_plot.add_trace(go.Scatter(
    x=df['End'],
    y=df['Grade'],
    marker=dict(color='#227266', size=14),
    mode='markers+text',
    text=m_lbl,
    textposition='middle right',
    name='End'))

fig_range_plot.update_layout(title="Data Availability", showlegend=False)
    
    
    

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

clinic_list = category_list

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
                children="Some description about our Project.",
                
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
            html.Label("Select Sector"),
            html.Hr(),
            html.Br(),
            dcc.Dropdown(
                id="clinic-select",
                options=[{"label": i, "value": i} for i in clinic_list],
                value=clinic_list[0],
            ),
            html.Br(),
            
            dcc.Dropdown(
                id="-select_co2_source",
                options=[{"label": i, "value": i} for i in sector_list],
                value=sector_list[0],
            ),
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


            html.Br(),
            html.Label('Select Prediction Sector:'),
            html.Hr(),
            html.Br(),
                        
                        
            dcc.Checklist(
                            options=[
                                {'label': 'Mobility', 'value': 'NYC'},
                                {'label': u'Energy', 'value': 'MTL'},
                                {'label': 'Economy', 'value': 'SF'},
                                {'label': 'All', 'value': 'all'},
                            ],
             value=['MTL'],

            ),
            
                    
                dcc.Store(id="store"),                                                                                
                            
                        
                        html.Br(),
                        html.Label('Datatype'),
                        html.Hr(),
                        html.Br(),
                            dcc.Dropdown(
                            options=[
                                {'label': 'DAX Data', 'value': 'NYC'},
                                {'label': u'Mobility Data', 'value': 'MTL'},
                                {'label': 'Transportation Cars Data', 'value': 'SF'}
                            ],
                            value='MTL'
                            
                            
                        ),


                            
                        html.Label('Multi-Select Dropdown'),
                                
                        dcc.Dropdown(
                            options=[
                                {'label': 'New York City', 'value': 'NYC'},
                                {'label': u'Montréal', 'value': 'MTL'},
                                {'label': 'San Francisco', 'value': 'SF'}
                            ],
                            value=['MTL', 'SF'],
                            multi=True
                        ),

                    
                        # html.Label('Text Input'),
                        # dcc.Input(value='MTL', type='text'),
                        
                        html.Br(),
                        html.Label('Slider'),
                        html.Hr(),
                        html.Br(),
                        dcc.Slider(
                            min=0,
                            max=9,
                            marks={i: 'Infectionnumber'.format(i) if i == 1 else str(i) for i in range(1, 6)},
                            value=5,
                        ),
                        html.Br(),
                        dcc.Slider(
                            min=0,
                            max=9,
                            marks={i: 'R-Value'.format(i) if i == 1 else str(i) for i in range(1, 6)},
                            value=2,
                        ),
                        daq.BooleanSwitch(
                          on=True,
                          label="Second Wave",
                          labelPosition="top",
                          id="button_second_wave",
                        ),
                                                
                    
        
                    
                        html.Br(),
                        html.Label('App Control'),
                        html.Hr(),
                        html.Br(),
                        html.Div(
                            id="reset-btn-outer",
                            children=[html.Button(id="reset-btn", children="Reset", n_clicks=0), html.Button(id="Update", children="Update", n_clicks=0), html.Button(id="Update2", children="Update2", n_clicks=0),],
                        ),
                        
                        html.Br(),
                        dbc.Button(
                                "Generate Graphs",
                                color="primary",
                                block=True,
                                id="button",
                                className="mb-3",
                        ),
                        
            
        ],
    )



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
                html.Div(
                    id="patient_volume_card",
                    children=[
                        html.B("Patient Volume"),
                        html.Hr(),
                        dbc.Tabs(
                                [
                                dbc.Tab(label="Data", tab_id="scatter"),
                                dbc.Tab(label="Prediction", tab_id="histogram"),
                                ],
                                id="tabs",
                                active_tab="scatter",
                            ),
                            html.Div(id="tab-content", className="p-4"),                                                                                                    
                        
                    ],
                ),
                # Availability of Data
                html.Div(
                    id="wait_time_card",
                    children=[
                        html.B("Data availability"),
                        html.Hr(),
                        #html.Div(id="wait_time_table", children=initialize_table()),
                        dcc.Graph(figure=fig_range_plot),
                    ],
                ),
                
                
              

            ],
        ),
    ],
)








@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("store", "data")],
)
def render_tab_content(active_tab, data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab and data is not None:
        if active_tab == "scatter":
            return  dcc.Graph(figure=data["scatter"]) #dcc.Graph(id='example-graph2', figure=fig)  
           
        
        
        elif active_tab == "histogram":
            return dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=data["hist_1"]), width=6),
                    dbc.Col(dcc.Graph(figure=data["hist_2"]), width=6),
                ]
            )
    return "No tab selected"




@app.callback(Output("store", "data"), [Input("button", "n_clicks"),Input("clinic-select","value")])
def generate_graphs(n,value):
    """
    This callback generates three simple graphs from random data.
    """
    #if not n:
        # generate empty graphs when app loads
    #    return {k: go.Figure(data=[]) for k in ["scatter", "hist_1", "hist_2"]}

    # simulate expensive graph generation process
    #time.sleep(2)
        
    
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



    # generate 100 multivariate normal samples
    data = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], 100)

    scatter = go.Figure(
        data=[go.Scatter(x=data[:, 0], y=data[:, 1], mode="markers")]
    )
    
    scatter = plot_data_of_sector('target_values')
    hist_1 = plot_data_of_sector('economy')
    hist_2 = plot_data_of_sector('energy_households')

    # save figures in a dictionary for sending to the dcc.Store
    return {"scatter": scatter, "hist_1": hist_1, "hist_2": hist_2}





# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
