import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

df = pd.read_csv("air-passengers-carried.csv")
# Rename the column 'Air transport, passengers carried' to 'Passengers_Carried'
df.rename(columns={'Air transport, passengers carried': 'Passengers_Carried'}, inplace=True)
# Iterate over the rows and fill missing 'Code' values with first three characters of 'Entity'
for index, row in df.iterrows():
    if pd.isna(row['Code']):
        df.at[index, 'Code'] = row['Entity'][:3].upper()
df_1 = df.copy()

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Assuming df_1 is your DataFrame containing relevant data
# You should replace it with your actual DataFrame

# List of countries you want to visualize
countries = df_1['Entity'].unique()

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    # Dropdown for selecting the country
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in countries],
        value='Malaysia',  # Default selected value
        style={'width': '50%'}
    ),
    
    # Placeholder for the Treemap chart
    dcc.Graph(id='treemap-chart'),
])

# Callback to update the Treemap chart based on the selected country
@app.callback(
    Output('treemap-chart', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_chart(selected_entity):
    # Filter the DataFrame for the selected 'Entity'
    df_entity = df_1[df_1['Entity'] == selected_entity]
    
    # Add a constant 'world' column to simulate a continent level
    df_entity['world'] = 'world'
    
    # Create a treemap chart for the selected 'Entity'
    fig = px.treemap(df_entity, path=['world', 'Year'], values='Passengers_Carried',
                     color='Passengers_Carried', hover_data=['Year'],
                     title=f'Treemap Chart for {selected_entity}',
                     labels={'Year': 'Year', 'Passengers_Carried': 'Air Transport Passenger_Carried'})
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

