# Import required libraries

import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px


# ============================================================
# Read the SpaceX launch data into pandas dataframe
# ============================================================

spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# ============================================================
# Create a Dash application
# ============================================================

app = dash.Dash(__name__)


# ============================================================
# Create an app layout
# ============================================================

app.layout = html.Div(children=[

    html.H1(
        'SpaceX Launch Records Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 40
        }
    ),

    # ========================================================
    # TASK 1: Add a dropdown list to enable Launch Site
    # selection
    # ========================================================

    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),

    html.Br(),

    # ========================================================
    # TASK 2: Pie chart
    # ========================================================

    html.Div(
        dcc.Graph(
            id='success-pie-chart'
        )
    ),

    html.Br(),

    html.P("Payload range (Kg):"),

    # ========================================================
    # TASK 3: Range Slider
    # ========================================================

    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # ========================================================
    # TASK 4: Scatter chart
    # ========================================================

    html.Div(
        dcc.Graph(
            id='success-payload-scatter-chart'
        )
    ),

])


# ============================================================
# TASK 2:
# Callback for site-dropdown -> success-pie-chart
# ============================================================

@app.callback(
    Output(
        component_id='success-pie-chart',
        component_property='figure'
    ),
    Input(
        component_id='site-dropdown',
        component_property='value'
    )
)
def get_pie_chart(entered_site):

    # --------------------------------------------------------
    # If ALL sites are selected
    # --------------------------------------------------------

    if entered_site == 'ALL':

        # Only successful launches
        success_df = spacex_df[
            spacex_df['class'] == 1
        ]

        fig = px.pie(
            success_df,
            names='Launch Site',
            title='Total Success Launches By Site'
        )

    # --------------------------------------------------------
    # If a specific launch site is selected
    # --------------------------------------------------------

    else:

        filtered_df = spacex_df[
            spacex_df['Launch Site'] == entered_site
        ]

        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Success vs. Failed Launches for {entered_site}'
        )

    return fig


# ============================================================
# TASK 4:
# Callback for site-dropdown + payload-slider
# -> success-payload-scatter-chart
# ============================================================

@app.callback(
    Output(
        component_id='success-payload-scatter-chart',
        component_property='figure'
    ),
    [
        Input(
            component_id='site-dropdown',
            component_property='value'
        ),
        Input(
            component_id='payload-slider',
            component_property='value'
        )
    ]
)
def update_scatter_plot(entered_site, payload_range):

    # Get the selected payload range
    low, high = payload_range

    # Filter by payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    # --------------------------------------------------------
    # If ALL sites are selected
    # --------------------------------------------------------

    if entered_site == 'ALL':

        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for all Sites'
        )

    # --------------------------------------------------------
    # If a specific launch site is selected
    # --------------------------------------------------------

    else:

        filtered_df = filtered_df[
            filtered_df['Launch Site'] == entered_site
        ]

        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Correlation between Payload and Success for {entered_site}'
        )

    return fig


# ============================================================
# Run the app
# ============================================================

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8050,
        debug=False
    )
    