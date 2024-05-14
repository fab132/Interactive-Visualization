import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from sklearn.datasets import fetch_california_housing

# Funktion zur Erstellung des Datasets aus Open Data
def load_dataset():
    housing = fetch_california_housing(as_frame=True)
    df = housing.frame
    df['longitude'] = df['Longitude']
    df['latitude'] = df['Latitude']
    df['price'] = df['MedHouseVal'] * 100000  # Skalieren der Preise für bessere Visualisierung
    df['size'] = df['AveRooms'] * df['AveOccup']
    df['type'] = pd.cut(df['MedHouseVal'], bins=[0, 1, 2, 3, 4, 5], labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
    df = df.dropna(subset=['type'])  # Entferne Zeilen mit NaN-Werten im 'type'-Feld
    return df

# Dataset laden
df = load_dataset()

# Dash-App initialisieren
app = dash.Dash(__name__)

# Layout der App definieren
app.layout = html.Div([
    html.H1("California Housing Data Analysis Dashboard"),
    
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
        html.Label("House Value Type:"),
        dcc.Dropdown(
            id='type-dropdown',
            options=[{'label': t, 'value': t} for t in df['type'].unique()],
            value=df['type'].unique().tolist(),
            multi=True
        ),
    ]),
])

# Callback zur Aktualisierung der Karte basierend auf den Filtern
@app.callback(
    Output('map', 'figure'),
    [Input('price-slider', 'value'),
     Input('type-dropdown', 'value')]
)
def update_map(price_range, house_types):
    filtered_df = df[(df['price'] >= price_range[0]) & (df['price'] <= price_range[1]) & (df['type'].isin(house_types))]
    
    fig = px.scatter_mapbox(filtered_df, lat='latitude', lon='longitude', color='price', size='size',
                            hover_data=['price', 'size', 'type'], zoom=5,
                            mapbox_style="carto-positron")
    return fig

# Callback zur Aktualisierung des Streudiagramms basierend auf der Kartenauswahl
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

# Callback zur Aktualisierung des Balkendiagramms basierend auf der Kartenauswahl
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

# App starten
if __name__ == '__main__':
    app.run_server(debug=True)
