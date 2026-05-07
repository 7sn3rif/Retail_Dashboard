import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Load dataset (adjust depending on actual file type)
dataset_path = r'C:\Users\LENOVO\Desktop\Retail_Dashboard\datasets\retail_analytics_20k.csv.xls'
df = pd.read_csv(dataset_path)

# Initial figure
profit_by_quarter = df.groupby('quarter')['profit_egp'].sum().reset_index()
profit_by_quarter_bar = px.bar(profit_by_quarter, x='quarter', y='profit_egp')

# Initialize app
app = Dash(__name__) 
app.title = 'Retail Analysis Dashboard'

app.layout = html.Div([
    html.H1('Retail Analysis Dashboard'),
    html.Div([
        html.H2('Profit per quarter'),
        dcc.Dropdown(
            id='dropdown_region',
            options=[{'label': r, 'value': r} for r in df['region'].unique()],
            placeholder="Select a region"
        ),
        dcc.Graph(id='profit_per_region_fig', figure=profit_by_quarter_bar),
        dcc.Interval(
            id='interval_component',
            interval=5000,  # refresh every 5 seconds
            n_intervals=0
        )
    ])
])

@app.callback(
    Output('profit_per_region_fig', 'figure'),
    [Input('dropdown_region', 'value'),
     Input('interval_component', 'n_intervals')]
)
def update_dashboard(selected_region, n_intervals):
    df = pd.read_csv(dataset_path)  # reload to simulate live updates
    if selected_region is None:
        profit_by_quarter = df.groupby('quarter')['profit_egp'].sum().reset_index()
    else:
        filtered_df = df[df['region'] == selected_region]
        profit_by_quarter = filtered_df.groupby('quarter')['profit_egp'].sum().reset_index()

    return px.bar(profit_by_quarter, x='quarter', y='profit_egp')


app.run()
