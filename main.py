import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Funktion zur Erstellung des Datasets
def create_dataset(filename='real_estate_data.csv', num_properties=1000):
    np.random.seed(42)
    latitude = np.random.uniform(low=34.0, high=38.0, size=num_properties)
    longitude = np.random.uniform(low=-118.5, high=-121.5, size=num_properties)
    price = np.random.uniform(low=100000, high=2000000, size=num_properties).astype(int)
    size = np.random.uniform(low=500, high=5000, size=num_properties).astype(int)
    property_type = np.random.choice(['House', 'Apartment', 'Condo', 'Townhouse'], size=num_properties)
    
    data = {
        'latitude': latitude,
        'longitude': longitude,
        'price': price,
        'size': size,
        'type': property_type
    }
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Dataset '{filename}' created with {num_properties} properties.")

# Funktion zur Erstellung des Dashboards
def create_dashboard():
    # Dataset laden
    df = pd.read_csv('real_estate_data.csv')

    # Dash-App initialisieren
    app = dash.Dash(__name__)

    # Layout der App definieren
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

    # Callback zur Aktualisierung der Karte basierend auf den Filtern
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

# Hauptfunktion
def main():
    create_dataset()
    create_dashboard()

if __name__ == '__main__':
    main()
