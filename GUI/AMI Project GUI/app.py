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

from dash.dependencies import Input, Output
import json


fig = go.Figure()









app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

server = app.server
app.config.suppress_callback_exceptions = True

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()








#Import Data from json FIle
category_list=[];
sector_list=[];

with open(DATA_PATH.joinpath("feature_database.json")) as json_file:
    database = json.load(json_file)



for i in database:
  feature = database.get(i)
  if feature['category'] not in category_list:
    category_list.append(feature['category'])


for i in database:
  feature = database.get(i)
  if feature['sector'] not in category_list:
    sector_list.append(feature['sector'])



# Read data
df = pd.read_csv(DATA_PATH.joinpath("clinical_analytics.csv"))

clinic_list = df["Clinic Name"].unique()
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
            html.P("Select Data Sector"),
            dcc.Dropdown(
                id="clinic-select",
                options=[{"label": i, "value": i} for i in clinic_list],
                value=clinic_list[0],
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
            html.Br(),
            html.Br(),
            html.P("Select Admit Source"),
            dcc.Dropdown(
                id="admit-select",
                options=[{"label": i, "value": i} for i in admit_list],
                value=admit_list[:],
                multi=True,
            ),

            html.Label('Checkboxes'),
            dcc.Checklist(
                            options=[
                                {'label': 'New York City', 'value': 'NYC'},
                                {'label': u'Montréal', 'value': 'MTL'},
                                {'label': 'San Francisco', 'value': 'SF'}
                            ],
             value=['MTL'],

            ),
            
                    
                            dcc.Store(id="store"),                                                                                
                            
                            html.Label('Datatype'),
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
                    
                    
                        html.Label('Text Input'),
                        dcc.Input(value='MTL', type='text'),
                    
                        html.Label('Slider'),
                        dcc.Slider(
                            min=0,
                            max=9,
                            marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
                            value=5,
                        ),
                        
                    
                        daq.Slider(
                            id='my-daq-slider-ex',
                            value=17
                        ),
                        html.Br(),
                        html.Div(
                            id="reset-btn-outer",
                            children=html.Button(id="reset-btn", children="Reset", n_clicks=0),
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


# def generate_patient_volume_heatmap(start, end, clinic, hm_click, admit_type, reset):
#     """
#     :param: start: start date from selection.
#     :param: end: end date from selection.
#     :param: clinic: clinic from selection.
#     :param: hm_click: clickData from heatmap.
#     :param: admit_type: admission type from selection.
#     :param: reset (boolean): reset heatmap graph if True.

#     :return: Patient volume annotated heatmap.
#     """

#     filtered_df = df[
#         (df["Clinic Name"] == clinic) & (df["Admit Source"].isin(admit_type))
#     ]
#     filtered_df = filtered_df.sort_values("Check-In Time").set_index("Check-In Time")[
#         start:end
#     ]

#     x_axis = [datetime.time(i).strftime("%I %p") for i in range(24)]  # 24hr time list
#     y_axis = day_list

#     hour_of_day = ""
#     weekday = ""
#     shapes = []

#     if hm_click is not None:
#         hour_of_day = hm_click["points"][0]["x"]
#         weekday = hm_click["points"][0]["y"]

#         # Add shapes
#         x0 = x_axis.index(hour_of_day) / 24
#         x1 = x0 + 1 / 24
#         y0 = y_axis.index(weekday) / 7
#         y1 = y0 + 1 / 7

#         shapes = [
#             dict(
#                 type="rect",
#                 xref="paper",
#                 yref="paper",
#                 x0=x0,
#                 x1=x1,
#                 y0=y0,
#                 y1=y1,
#                 line=dict(color="#ff6347"),
#             )
#         ]

#     # Get z value : sum(number of records) based on x, y,

#     z = np.zeros((7, 24))
#     annotations = []

#     for ind_y, day in enumerate(y_axis):
#         filtered_day = filtered_df[filtered_df["Days of Wk"] == day]
#         for ind_x, x_val in enumerate(x_axis):
#             sum_of_record = filtered_day[filtered_day["Check-In Hour"] == x_val][
#                 "Number of Records"
#             ].sum()
#             z[ind_y][ind_x] = sum_of_record

#             annotation_dict = dict(
#                 showarrow=False,
#                 text="<b>" + str(sum_of_record) + "<b>",
#                 xref="x",
#                 yref="y",
#                 x=x_val,
#                 y=day,
#                 font=dict(family="sans-serif"),
#             )
#             # Highlight annotation text by self-click
#             if x_val == hour_of_day and day == weekday:
#                 if not reset:
#                     annotation_dict.update(size=15, font=dict(color="#ff6347"))

#             annotations.append(annotation_dict)

#     # Heatmap
#     hovertemplate = "<b> %{y}  %{x} <br><br> %{z} Patient Records"

#     data = [
#         dict(
#             x=x_axis,
#             y=y_axis,
#             z=z,
#             type="heatmap",
#             name="",
#             hovertemplate=hovertemplate,
#             showscale=False,
#             colorscale=[[0, "#caf3ff"], [1, "#2c82ff"]],
#         )
#     ]

#     layout = dict(
#         margin=dict(l=70, b=50, t=50, r=50),
#         modebar={"orientation": "v"},
#         font=dict(family="Open Sans"),
#         annotations=annotations,
#         shapes=shapes,
#         xaxis=dict(
#             side="top",
#             ticks="",
#             ticklen=2,
#             tickfont=dict(family="sans-serif"),
#             tickcolor="#ffffff",
#         ),
#         yaxis=dict(
#             side="left", ticks="", tickfont=dict(family="sans-serif"), ticksuffix=" "
#         ),
#         hovermode="closest",
#         showlegend=False,
#     )
#     return {"data": data, "layout": layout}


# def generate_table_row(id, style, col1, col2, col3):
#     """ Generate table rows.

#     :param id: The ID of table row.
#     :param style: Css style of this row.
#     :param col1 (dict): Defining id and children for the first column.
#     :param col2 (dict): Defining id and children for the second column.
#     :param col3 (dict): Defining id and children for the third column.
#     """

#     return html.Div(
#         id=id,
#         className="row table-row",
#         style=style,
#         children=[
#             html.Div(
#                 id=col1["id"],
#                 style={"display": "table", "height": "100%"},
#                 className="two columns row-department",
#                 children=col1["children"],
#             ),
#             html.Div(
#                 id=col2["id"],
#                 style={"textAlign": "center", "height": "100%"},
#                 className="five columns",
#                 children=col2["children"],
#             ),
#             html.Div(
#                 id=col3["id"],
#                 style={"textAlign": "center", "height": "100%"},
#                 className="five columns",
#                 children=col3["children"],
#             ),
#         ],
#     )


# def generate_table_row_helper(department):
#     """Helper function.

#     :param: department (string): Name of department.
#     :return: Table row.
#     """
#     return generate_table_row(
#         department,
#         {},
#         {"id": department + "_department", "children": html.B(department)},
#         {
#             "id": department + "wait_time",
#             "children": dcc.Graph(
#                 id=department + "_wait_time_graph",
#                 style={"height": "100%", "width": "100%"},
#                 className="wait_time_graph",
#                 config={
#                     "staticPlot": False,
#                     "editable": False,
#                     "displayModeBar": False,
#                 },
#                 figure={
#                     "layout": dict(
#                         margin=dict(l=0, r=0, b=0, t=0, pad=0),
#                         xaxis=dict(
#                             showgrid=False,
#                             showline=False,
#                             showticklabels=False,
#                             zeroline=False,
#                         ),
#                         yaxis=dict(
#                             showgrid=False,
#                             showline=False,
#                             showticklabels=False,
#                             zeroline=False,
#                         ),
#                         paper_bgcolor="rgba(0,0,0,0)",
#                         plot_bgcolor="rgba(0,0,0,0)",
#                     )
#                 },
#             ),
#         },
#         {
#             "id": department + "_patient_score",
#             "children": dcc.Graph(
#                 id=department + "_score_graph",
#                 style={"height": "100%", "width": "100%"},
#                 className="patient_score_graph",
#                 config={
#                     "staticPlot": False,
#                     "editable": False,
#                     "displayModeBar": False,
#                 },
#                 figure={
#                     "layout": dict(
#                         margin=dict(l=0, r=0, b=0, t=0, pad=0),
#                         xaxis=dict(
#                             showgrid=False,
#                             showline=False,
#                             showticklabels=False,
#                             zeroline=False,
#                         ),
#                         yaxis=dict(
#                             showgrid=False,
#                             showline=False,
#                             showticklabels=False,
#                             zeroline=False,
#                         ),
#                         paper_bgcolor="rgba(0,0,0,0)",
#                         plot_bgcolor="rgba(0,0,0,0)",
#                     )
#                 },
#             ),
#         },
#     )


# def initialize_table():
#     """
#     :return: empty table children. This is intialized for registering all figure ID at page load.
#     """

#     # header_row
#     header = [
#         generate_table_row(
#             "header",
#             {"height": "50px"},
#             {"id": "header_department", "children": html.B("Department")},
#             {"id": "header_wait_time_min", "children": html.B("Wait Time Minutes")},
#             {"id": "header_care_score", "children": html.B("Care Score")},
#         )
#     ]

#     # department_row
#     rows = [generate_table_row_helper(department) for department in all_departments]
#     header.extend(rows)
#     empty_table = header

#     return empty_table


# def generate_patient_table(figure_list, departments, wait_time_xrange, score_xrange):
#     """
#     :param score_xrange: score plot xrange [min, max].
#     :param wait_time_xrange: wait time plot xrange [min, max].
#     :param figure_list:  A list of figures from current selected metrix.
#     :param departments:  List of departments for making table.
#     :return: Patient table.
#     """
#     # header_row
#     header = [
#         generate_table_row(
#             "header",
#             {"height": "50px"},
#             {"id": "header_department", "children": html.B("Department")},
#             {"id": "header_wait_time_min", "children": html.B("Wait Time Minutes")},
#             {"id": "header_care_score", "children": html.B("Care Score")},
#         )
#     ]

#     # department_row
#     rows = [generate_table_row_helper(department) for department in departments]
#     # empty_row
#     empty_departments = [item for item in all_departments if item not in departments]
#     empty_rows = [
#         generate_table_row_helper(department) for department in empty_departments
#     ]

#     # fill figures into row contents and hide empty rows
#     for ind, department in enumerate(departments):
#         rows[ind].children[1].children.figure = figure_list[ind]
#         rows[ind].children[2].children.figure = figure_list[ind + len(departments)]
#     for row in empty_rows[1:]:
#         row.style = {"display": "none"}

#     # convert empty row[0] to axis row
#     empty_rows[0].children[0].children = html.B(
#         "graph_ax", style={"visibility": "hidden"}
#     )

#     empty_rows[0].children[1].children.figure["layout"].update(
#         dict(margin=dict(t=-70, b=50, l=0, r=0, pad=0))
#     )

#     empty_rows[0].children[1].children.config["staticPlot"] = True

#     empty_rows[0].children[1].children.figure["layout"]["xaxis"].update(
#         dict(
#             showline=True,
#             showticklabels=True,
#             tick0=0,
#             dtick=20,
#             range=wait_time_xrange,
#         )
#     )
#     empty_rows[0].children[2].children.figure["layout"].update(
#         dict(margin=dict(t=-70, b=50, l=0, r=0, pad=0))
#     )

#     empty_rows[0].children[2].children.config["staticPlot"] = True

#     empty_rows[0].children[2].children.figure["layout"]["xaxis"].update(
#         dict(showline=True, showticklabels=True, tick0=0, dtick=0.5, range=score_xrange)
#     )

#     header.extend(rows)
#     header.extend(empty_rows)
#     return header


# def create_table_figure(
#     department, filtered_df, category, category_xrange, selected_index
# ):
#     """Create figures.

#     :param department: Name of department.
#     :param filtered_df: Filtered dataframe.
#     :param category: Defining category of figure, either 'wait time' or 'care score'.
#     :param category_xrange: x axis range for this figure.
#     :param selected_index: selected point index.
#     :return: Plotly figure dictionary.
#     """
#     aggregation = {
#         "Wait Time Min": "mean",
#         "Care Score": "mean",
#         "Days of Wk": "first",
#         "Check-In Time": "first",
#         "Check-In Hour": "first",
#     }

#     df_by_department = filtered_df[
#         filtered_df["Department"] == department
#     ].reset_index()
#     grouped = (
#         df_by_department.groupby("Encounter Number").agg(aggregation).reset_index()
#     )
#     patient_id_list = grouped["Encounter Number"]

#     x = grouped[category]
#     y = list(department for _ in range(len(x)))

#     f = lambda x_val: dt.strftime(x_val, "%Y-%m-%d")
#     check_in = (
#         grouped["Check-In Time"].apply(f)
#         + " "
#         + grouped["Days of Wk"]
#         + " "
#         + grouped["Check-In Hour"].map(str)
#     )

#     text_wait_time = (
#         "Patient # : "
#         + patient_id_list
#         + "<br>Check-in Time: "
#         + check_in
#         + "<br>Wait Time: "
#         + grouped["Wait Time Min"].round(decimals=1).map(str)
#         + " Minutes,  Care Score : "
#         + grouped["Care Score"].round(decimals=1).map(str)
#     )

#     layout = dict(
#         margin=dict(l=0, r=0, b=0, t=0, pad=0),
#         clickmode="event+select",
#         hovermode="closest",
#         xaxis=dict(
#             showgrid=False,
#             showline=False,
#             showticklabels=False,
#             zeroline=False,
#             range=category_xrange,
#         ),
#         yaxis=dict(
#             showgrid=False, showline=False, showticklabels=False, zeroline=False
#         ),
#         paper_bgcolor="rgba(0,0,0,0)",
#         plot_bgcolor="rgba(0,0,0,0)",
#     )

#     trace = dict(
#         x=x,
#         y=y,
#         mode="markers",
#         marker=dict(size=14, line=dict(width=1, color="#ffffff")),
#         color="#2c82ff",
#         selected=dict(marker=dict(color="#ff6347", opacity=1)),
#         unselected=dict(marker=dict(opacity=0.1)),
#         selectedpoints=selected_index,
#         hoverinfo="text",
#         customdata=patient_id_list,
#         text=text_wait_time,
#     )

#     return {"data": [trace], "layout": layout}


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
                        dcc.Graph(id="patient_volume_hm"),
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
            return  dcc.Graph(id='example-graph2', figure=fig)  #dcc.Graph(figure=data["scatter"])
           
        
        
        elif active_tab == "histogram":
            return dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=data["hist_1"]), width=6),
                    dbc.Col(dcc.Graph(figure=data["hist_2"]), width=6),
                ]
            )
    return "No tab selected"




@app.callback(Output("store", "data"), [Input("button", "n_clicks")])
def generate_graphs(n):
    """
    This callback generates three simple graphs from random data.
    """
    if not n:
        # generate empty graphs when app loads
        return {k: go.Figure(data=[]) for k in ["scatter", "hist_1", "hist_2"]}

    # simulate expensive graph generation process
    #time.sleep(2)
        
    
    #Graphtest function
    
    x = ['2015-02-17','2015-02-18','2015-02-19','2015-02-20','2015-02-23','2015-02-24','2015-02-25','2015-02-26','2015-02-27','2015-03-02']

    x_rev = x[::-1]
    
    # Line 1
    y1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y1_upper = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    y1_lower = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y1_lower = y1_lower[::-1]
    
    # Line 2
    y2 = [5, 2.5, 5, 7.5, 5, 2.5, 7.5, 4.5, 5.5, 5]
    y2_upper = [5.5, 3, 5.5, 8, 6, 3, 8, 5, 6, 5.5]
    y2_lower = [4.5, 2, 4.4, 7, 4, 2, 7, 4, 5, 4.75]
    y2_lower = y2_lower[::-1]
    
    # Line 3
    y3 = [10, 8, 6, 4, 2, 0, 2, 4, 2, 0]
    y3_upper = [11, 9, 7, 20, 3, 1, 3, 5, 3, 1]
    y3_lower = [9, 7, 5, 3, 1, -.5, 1, 3, 1, -1]
    y3_lower = y3_lower[::-1]
    
    
    
    # Line 4
    y4 = [10, 8, 6, 4, 5, 0, 2, 4, 2, 0]
    y4_upper = [11, 9, 7, 20, 3, 1, 3, 5, 3, 1]
    y4_lower = [9, 7, 5, 3, 1, -.5, 1, 3, 1, -1]
    y4_lower = y3_lower[::-1]

    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
  #  fig = go.Figure([go.Scatter(x=df['Date'], y=df['AAPL.High'])])
    #fig.show()

    
    fig.data = []
    
    # fig.add_trace(go.Scatter(
    #     x=df['Date'], y=df['AAPL.High'],
    #     line_color='rgb(231,107,243)',
    #     name='Ideal',
    # ))
    




    fig.add_trace(go.Scatter(
        x=x+x_rev,
        y=y3_upper+y3_lower,
        fill='toself',
        fillcolor='rgba(231,107,243,0.2)',
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        name='Ideal',
    ))
    fig.add_trace(go.Scatter(
        x=x, y=y3,
        line_color='rgb(231,107,243)',
        name='Ideal',
    ))


    fig.add_trace(go.Scatter(
        x=x+x_rev,
        y=y1_upper+y1_lower,
        fill='toself',
        fillcolor='rgba(0,100,80,0.2)',
        line_color='rgba(255,255,255,0)',
        showlegend=False,
        name='Fair',
    ))
    fig.add_trace(go.Scatter(
        x=x+x_rev,
        y=y2_upper+y2_lower,
        fill='toself',
        fillcolor='rgba(0,176,246,0.2)',
        line_color='rgba(255,255,255,0)',
        name='Premium',
        showlegend=False,
    ))
    
    
    fig.add_trace(go.Scatter(
        x=x, y=y1,
        line_color='rgb(0,100,80)',
        name='Fair',
    ))
    fig.add_trace(go.Scatter(
        x=x, y=y2,
        line_color='rgb(0,176,246)',
        name='Premium',
    ))
    
    
    
    
    fig.update_traces(mode='lines')
    #fig.show()




    # generate 100 multivariate normal samples
    data = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], 100)

    scatter = go.Figure(
        data=[go.Scatter(x=data[:, 0], y=data[:, 1], mode="markers")]
    )
    hist_1 = go.Figure(data=[go.Histogram(x=data[:, 0])])
    hist_2 = go.Figure(data=[go.Histogram(x=data[:, 1])])

    # save figures in a dictionary for sending to the dcc.Store
    return {"scatter": scatter, "hist_1": hist_1, "hist_2": hist_2}





# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)
