import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the dataset
df = pd.read_csv('real_estate_data.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Real Estate Data Analysis Dashboard"),
    
    dcc.Graph(id='map', config={'scrollZoom': True}),
    
    html.Div([
        dcc.Graph(id='scatter-plot'),
        dcc.Graph(id='bar-chart')
    ]),
    
    html.Div([
        html.Label("Price Range:"),
        dcc.RangeSlider(
            id='price-slider',
            min=df['price'].min(),
            max=df['price'].max(),
            value=[df['price'].min(), df['price'].max()],
            marks={int(price): f'${price}' for price in range(int(df['price'].min()), int(df['price'].max()), 100000)},
            step=10000
        ),
    ]),
    
    html.Div([
        html.Label("Property Type:"),
        dcc.Dropdown(
            id='type-dropdown',
            options=[{'label': t, 'value': t} for t in df['type'].unique()],
            value=df['type'].unique(),
            multi=True
        ),
    ]),
])

# Callback to update map based on filters
@app.callback(
    Output('map', 'figure'),
    [Input('price-slider', 'value'),
     Input('type-dropdown', 'value')]
)
def update_map(price_range, property_types):
    filtered_df = df[(df['price'] >= price_range[0]) & (df['price'] <= price_range[1]) & (df['type'].isin(property_types))]
    
    fig = px.scatter_mapbox(filtered_df, lat='latitude', lon='longitude', color='price', size='size',
                            hover_data=['price', 'size', 'type'], zoom=10,
                            mapbox_style="carto-positron")
    return fig

# Callback to update scatter plot based on map selection
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('map', 'selectedData')]
)
def update_scatter(selectedData):
    if selectedData:
        selected_points = [point['pointIndex'] for point in selectedData['points']]
        filtered_df = df.iloc[selected_points]
    else:
        filtered_df = df
    
    fig = px.scatter(filtered_df, x='size', y='price', color='type', hover_data=['latitude', 'longitude'])
    return fig

# Callback to update bar chart based on map selection
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('map', 'selectedData')]
)
def update_bar(selectedData):
    if selectedData:
        selected_points = [point['pointIndex'] for point in selectedData['points']]
        filtered_df = df.iloc[selected_points]
    else:
        filtered_df = df

    fig = px.bar(filtered_df, x='type', y='price', hover_data=['latitude', 'longitude'])
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

