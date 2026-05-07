import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Load dataset 
dataset_path = r'C:\Users\LENOVO\Desktop\Retail_Dashboard\datasets\sales_data.csv'
df = pd.read_csv(dataset_path)
# Ensure order_date is datetime
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

# KPIs
total_revenue = df['revenue_egp'].sum()
total_profit = df['profit_egp'].sum()
total_orders = len(df)
return_rate = len(df[df['returned'] == 'Yes']) / len(df)



#figures
#figure 1: revenue per quarter
revenue_by_quarter = df.groupby('quarter')['revenue_egp'].sum().reset_index()
revenue_by_quarter_bar = px.bar(revenue_by_quarter, x='quarter', y='revenue_egp', template='plotly_dark', color_discrete_sequence=['#60a5fa'])


# figure 2: profit per quarter
profit_by_quarter = df.groupby('quarter')['profit_egp'].sum().reset_index()
profit_by_quarter_bar = px.bar(profit_by_quarter, x='quarter', y='profit_egp', template='plotly_dark', color_discrete_sequence=['#34d399'])

#figure 3: monthly revenue trend
monthly_revenue=df.groupby(df['order_date'].dt.to_period('M'))['revenue_egp'].sum().reset_index()
monthly_revenue
monthly_revenue['order_date'] = monthly_revenue['order_date'].dt.to_timestamp()
monthly_revenue_line=px.line(monthly_revenue,x='order_date',y='revenue_egp',title='Monthly Revenue', template='plotly_dark', color_discrete_sequence=['#60a5fa'])

#figure 4 :monthly profit trend
monthly_profit=df.groupby(df['order_date'].dt.to_period('M'))['profit_egp'].sum().reset_index()
monthly_profit['order_date'] = monthly_profit['order_date'].dt.to_timestamp()
monthly_profit_line=px.line(monthly_profit,x='order_date',y='profit_egp',title='Monthly Profit', template='plotly_dark', color_discrete_sequence=['#34d399'])    

#figure 5: Category revenue distribution
category_revenue = df.groupby('category')['revenue_egp'].sum().reset_index()
category_revenue_bar = px.bar(category_revenue, x='category', y='revenue_egp', title='Revenue by Category', color='category', template='plotly_dark', color_discrete_sequence=px.colors.sequential.Blues)

#figure 6: category profit distribution
category_profit = df.groupby('category')['profit_egp'].sum().reset_index()  
category_profit_bar = px.bar(category_profit, x='category', y='profit_egp', title='Profit by Category',color='category', template='plotly_dark', color_discrete_sequence=px.colors.sequential.Greens)

#figure 7: revenue by segment with dropdown for age group
segment_revenue = df.groupby('customer_segment')['revenue_egp'].sum().reset_index()
segment_revenue_pie = px.pie(segment_revenue, names='customer_segment', values='revenue_egp', title='Revenue by Customer Segment', template='plotly_dark')

#figure 8: revenue by city
revenue_by_city=df.groupby('city')['revenue_egp'].sum().reset_index()
revenue_by_city_treemap=px.treemap(revenue_by_city,path=['city'],values='revenue_egp',title='Revenue by City', template='plotly_dark', color_continuous_scale='Blues')

#figure 9: Sales channel performance
sales_channel_performance = df.groupby('sales_channel')['revenue_egp'].sum().reset_index()
sales_channel_performance_pie = px.pie(sales_channel_performance, names='sales_channel', values='revenue_egp', title='Revenue by Sales Channel', template='plotly_dark')

#figure 10: revenue by campaign
revenue_by_campaign = df.groupby('campaign')['revenue_egp'].sum().reset_index()
revenue_by_campaign_bar = px.bar(revenue_by_campaign, x='campaign', y='revenue_egp', title='Revenue by Campaign', color='campaign', template='plotly_dark')

#figure 11: revenue by traffic source
revenue_by_traffic_source = df.groupby('traffic_source')['revenue_egp'].sum().reset_index()
revenue_by_traffic_source_bar = px.bar(revenue_by_traffic_source, x='traffic_source', y='revenue_egp', title='Revenue by Traffic Source', color='traffic_source', template='plotly_dark')

#figure 12: heatmap of profit by category and campaign
profit_by_category_campaign = df.groupby(['category', 'campaign'])['profit_egp'].sum().reset_index()
profit_by_category_campaign_heatmap = px.imshow(profit_by_category_campaign.pivot(index='category', columns='campaign', values='profit_egp'), title='Profit by Category and Campaign', color_continuous_scale='Viridis', template='plotly_dark')



# Initialize app
app = Dash(__name__) 
app.title = 'Retail Analysis Dashboard'


# Premium styling injection
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
                background-attachment: fixed;
                color: #e2e8f0;
                margin: 0;
                padding: 0;
                min-height: 100vh;
            }
            h1 {
                text-align: center;
                font-size: 2.8rem;
                font-weight: 700;
                background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 30px 0 10px 0;
                letter-spacing: -0.5px;
            }
            h2 {
                font-size: 1.3rem;
                font-weight: 600;
                color: #f1f5f9;
                margin: 25px 0 15px 0;
                padding-bottom: 8px;
                border-bottom: 1px solid rgba(148, 163, 184, 0.2);
            }
            h3 {
                font-size: 0.85rem;
                font-weight: 500;
                color: #94a3b8;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                margin: 0 0 8px 0;
            }
            .dash-dropdown {
                margin-bottom: 15px;
            }
            .dash-dropdown .Select-control {
                background: rgba(30, 41, 59, 0.8) !important;
                border: 1px solid rgba(148, 163, 184, 0.2) !important;
                border-radius: 10px !important;
                color: #e2e8f0 !important;
            }
            .dash-dropdown .Select-menu-outer {
                background: rgba(30, 41, 59, 0.95) !important;
                border: 1px solid rgba(148, 163, 184, 0.2) !important;
                border-radius: 10px !important;
                backdrop-filter: blur(10px);
            }
            .dash-dropdown .Select-option {
                color: #e2e8f0 !important;
                background: transparent !important;
            }
            .dash-dropdown .Select-option:hover {
                background: rgba(96, 165, 250, 0.15) !important;
            }
            .dash-dropdown .Select-value-label {
                color: #e2e8f0 !important;
            }
            .js-plotly-plot .plotly .modebar {
                left: 50%;
                transform: translateX(-50%);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""


#layout

#kpi cards
KPI_cards = html.Div([
        html.Div([
            html.H3('Total Revenue'),
            html.P(f"{total_revenue:,.2f} EGP", style={'fontSize':'1.6rem','fontWeight':'700','color':'#60a5fa','margin':'0'})
        ], style={'width': '23%', 'display': 'inline-block', 'background': 'linear-gradient(135deg, rgba(96,165,250,0.15), rgba(96,165,250,0.05))', 'padding': '20px', 'margin': '8px', 'borderRadius': '16px', 'border': '1px solid rgba(96,165,250,0.2)', 'backdropFilter': 'blur(10px)', 'boxShadow': '0 8px 32px rgba(0,0,0,0.3)'}),
        html.Div([
            html.H3('Total Profit'),
            html.P(f"{total_profit:,.2f} EGP", style={'fontSize':'1.6rem','fontWeight':'700','color':'#34d399','margin':'0'})
        ], style={'width': '23%', 'display': 'inline-block', 'background': 'linear-gradient(135deg, rgba(52,211,153,0.15), rgba(52,211,153,0.05))', 'padding': '20px', 'margin': '8px', 'borderRadius': '16px', 'border': '1px solid rgba(52,211,153,0.2)', 'backdropFilter': 'blur(10px)', 'boxShadow': '0 8px 32px rgba(0,0,0,0.3)'}),
        html.Div([
            html.H3('Total Orders'),
            html.P(f"{total_orders:,}", style={'fontSize':'1.6rem','fontWeight':'700','color':'#fbbf24','margin':'0'})
        ], style={'width': '23%', 'display': 'inline-block', 'background': 'linear-gradient(135deg, rgba(251,191,36,0.15), rgba(251,191,36,0.05))', 'padding': '20px', 'margin': '8px', 'borderRadius': '16px', 'border': '1px solid rgba(251,191,36,0.2)', 'backdropFilter': 'blur(10px)', 'boxShadow': '0 8px 32px rgba(0,0,0,0.3)'}),
        html.Div([
            html.H3('Return Rate'),
            html.P(f"{return_rate:.2%}", style={'fontSize':'1.6rem','fontWeight':'700','color':'#f87171','margin':'0'})
        ], style={'width': '23%', 'display': 'inline-block', 'background': 'linear-gradient(135deg, rgba(248,113,113,0.15), rgba(248,113,113,0.05))', 'padding': '20px', 'margin': '8px', 'borderRadius': '16px', 'border': '1px solid rgba(248,113,113,0.2)', 'backdropFilter': 'blur(10px)', 'boxShadow': '0 8px 32px rgba(0,0,0,0.3)'})
    ], style={'textAlign': 'center', 'padding': '10px 0'})


# Insights Section
insights = [
    f"📈 Total revenue reached {total_revenue:,.0f} EGP across {total_orders:,} orders.",
    f"💰 Profit contribution is {total_profit:,.0f} EGP, margin {total_profit/total_revenue:.1%}.",
    f"🔄 Return rate is {return_rate:.1%}, about {int(return_rate*total_orders):,} returned orders.",
    f"🛒 Top category: {category_revenue.loc[category_revenue['revenue_egp'].idxmax(),'category']} with {category_revenue['revenue_egp'].max():,.0f} EGP.",
    f"🌍 Strongest channel: {sales_channel_performance.loc[sales_channel_performance['revenue_egp'].idxmax(),'sales_channel']} contributing {sales_channel_performance['revenue_egp'].max():,.0f} EGP."
]

insight_list = html.Div([
    html.H2("Key Insights", style={'color':'#f1f5f9','marginTop':'0'}),
    html.Ul([html.Li(insight, style={'color':'#cbd5e1','fontSize':'0.95rem','lineHeight':'1.8','marginBottom':'6px'}) for insight in insights], style={'paddingLeft':'20px','margin':'0'})
], style={'margin':'20px 15px','padding':'25px','background':'rgba(30,41,59,0.6)','borderRadius':'16px','border':'1px solid rgba(148,163,184,0.1)','backdropFilter':'blur(10px)','boxShadow':'0 8px 32px rgba(0,0,0,0.2)'})


app.layout = html.Div([
    html.H1('Retail Analysis Dashboard', style={'textAlign':'center'}),
   
   # KPIs
    KPI_cards,
    insight_list,

    #figures
    #figure 1: revenue per quarter with dropdown for region
    html.Div([
        html.H2('Revenue per quarter'),
        dcc.Dropdown(
            id='dropdown_region_revenue',
            options=[{'label': r, 'value': r} for r in df['region'].unique()],
            placeholder="Select a region"
        ),
        dcc.Graph(id='revenue_per_quarter_fig', figure=revenue_by_quarter_bar),
        dcc.Interval(
            id='interval_component_revenue',   
            interval=5000,  # refresh every 5 seconds   
            n_intervals=0
        )
    ], style={'background':'rgba(30,41,59,0.5)','borderRadius':'16px','padding':'20px','margin':'15px 0','border':'1px solid rgba(148,163,184,0.1)','backdropFilter':'blur(10px)','boxShadow':'0 8px 32px rgba(0,0,0,0.2)'}),

   #figure 2: profit per quarter with dropdown for region
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
    ], style={'background':'rgba(30,41,59,0.5)','borderRadius':'16px','padding':'20px','margin':'15px 0','border':'1px solid rgba(148,163,184,0.1)','backdropFilter':'blur(10px)','boxShadow':'0 8px 32px rgba(0,0,0,0.2)'}),

    #figure 3: monthly revenue trend with dropdown for region and category
    html.Div([
        html.H2('Monthly Revenue Trend'),
        dcc.Dropdown(
            id='dropdown_region_monthly',
            options=[{'label': r, 'value': r} for r in df['region'].unique()],
            placeholder="Select a region"
        ),
        dcc.Dropdown(
            id='dropdown_category_monthly',
            options=[{'label': c, 'value': c} for c in df['category'].unique()],
            placeholder="Select a category"
        ),
        dcc.Graph(id='monthly_revenue_trend_fig', figure=monthly_revenue_line),
            dcc.Interval(
                id='interval_component_monthly',   
                interval=5000,  # refresh every 5 seconds   
                n_intervals=0
            )

    ], style={'background':'rgba(30,41,59,0.5)','borderRadius':'16px','padding':'20px','margin':'15px 0','border':'1px solid rgba(148,163,184,0.1)','backdropFilter':'blur(10px)','boxShadow':'0 8px 32px rgba(0,0,0,0.2)'}),


    #figure 4: monthly profit trend with dropdown for region and category 
    html.Div([
        html.H2('Monthly Profit Trend'),
        dcc.Dropdown(
            id='dropdown_region_monthly_profit',
            options=[{'label': r, 'value': r} for r in df['region'].unique()],
            placeholder="Select a region"
        ),
        dcc.Dropdown(
            id='dropdown_category_monthly_profit',
            options=[{'label': c, 'value': c} for c in df['category'].unique()],
            placeholder="Select a category"
        ),
        dcc.Graph(id='monthly_profit_trend_fig', figure=monthly_profit_line),
            dcc.Interval(
                id='interval_component_monthly_profit',   
                interval=5000,  # refresh every 5 seconds   
                n_intervals=0
            )
    ]), 

    #figure 5: category revenue distribution with dropdown for region 
     html.Div([ 
        html.H2('Revenue by Category'),
        dcc.Dropdown(
            id='dropdown_region_category',
            options=[{'label': r, 'value': r} for r in df['region'].unique()],
            placeholder="Select a region"
        ),
        dcc.Graph(id='category_revenue_fig', figure=category_revenue_bar),
            dcc.Interval(
                id='interval_component_category',   
                interval=5000,  # refresh every 5 seconds   
                n_intervals=0
            )         
    ], style={'background':'rgba(30,41,59,0.5)','borderRadius':'16px','padding':'20px','margin':'15px 0','border':'1px solid rgba(148,163,184,0.1)','backdropFilter':'blur(10px)','boxShadow':'0 8px 32px rgba(0,0,0,0.2)'}),

    #figure 6: category profit distribution with dropdown for region
     html.Div([
        html.H2('Profit by Category'),
        dcc.Dropdown(
            id='dropdown_region_category_profit',
            options=[{'label': r, 'value': r} for r in df['region'].unique()],
            placeholder="Select a region"
        ),
        dcc.Graph(id='category_profit_fig', figure=category_profit_bar),
            dcc.Interval(
                id='interval_component_category_profit',   
                interval=5000,  # refresh every 5 seconds   
                n_intervals=0
            ) 
     ], style={'background':'rgba(30,41,59,0.5)','borderRadius':'16px','padding':'20px','margin':'15px 0','border':'1px solid rgba(148,163,184,0.1)','backdropFilter':'blur(10px)','boxShadow':'0 8px 32px rgba(0,0,0,0.2)'}),

    #figure 7: revenue by segment with dropdown for age group
        html.Div([
            html.H2('Revenue by Segment'),
            dcc.Dropdown(
                id='dropdown_age_group_segment',
                options=[{'label': a, 'value': a} for a in df['age_group'].unique()],
                placeholder="Select a age group"
            ),
            dcc.Graph(id='segment_revenue_fig', figure=segment_revenue_pie),
                dcc.Interval(
                    id='interval_component_segment',   
                    interval=5000,  # refresh every 5 seconds   
                    n_intervals=0
                )
        ], style={'background':'rgba(30,41,59,0.5)','borderRadius':'16px','padding':'20px','margin':'15px 0','border':'1px solid rgba(148,163,184,0.1)','backdropFilter':'blur(10px)','boxShadow':'0 8px 32px rgba(0,0,0,0.2)'}),

    #figure 8: revenue by city with dropdown for category
       html.Div([
        html.H2('Revenue by City'),
        dcc.Dropdown(
            id='dropdown_category_city',
            options=[{'label': c, 'value': c} for c in df['category'].unique()],
            placeholder="Select a category"
        ),
        dcc.Graph(id='revenue_by_city_fig', figure=revenue_by_city_treemap),
            dcc.Interval(
                id='interval_component_city',   
                interval=5000,  # refresh every 5 seconds   
                n_intervals=0
            )    
       ], style={'background':'rgba(30,41,59,0.5)','borderRadius':'16px','padding':'20px','margin':'15px 0','border':'1px solid rgba(148,163,184,0.1)','backdropFilter':'blur(10px)','boxShadow':'0 8px 32px rgba(0,0,0,0.2)'}),

    #figure 9: sales channel performance 
    html.Div([
        html.H2('Revenue by Sales Channel'),
        dcc.Graph(id='sales_channel_performance_fig', figure=sales_channel_performance_pie),
            dcc.Interval(
                id='interval_component_sales_channel',   
                interval=5000,  # refresh every 5 seconds   
                n_intervals=0
            )
       ]), 
    #figure 10: revenue by campaign with dropdown for category
    html.Div([
        html.H2('Revenue by Campaign'),
        dcc.Dropdown(
            id='dropdown_category_campaign',
            options=[{'label': c, 'value': c} for c in df['category'].unique()],
            placeholder="Select a category"
        ),
        dcc.Graph(id='revenue_by_campaign_fig', figure=revenue_by_campaign_bar),
            dcc.Interval(
                id='interval_component_campaign',   
                interval=5000,  # refresh every 5 seconds   
                n_intervals=0
            )
    ]), 

        #figure 11: revenue by traffic source with dropdown for category    
        html.Div([
           html.H2('Revenue by Traffic Source'),
           dcc.Dropdown(
               id='dropdown_category_traffic_source',
               options=[{'label': c, 'value': c} for c in df['category'].unique()],
               placeholder="Select a category"
           ),
           dcc.Graph(id='revenue_by_traffic_source_fig', figure=revenue_by_traffic_source_bar),
               dcc.Interval(
                   id='interval_component_traffic_source',   
                   interval=5000,  # refresh every 5 seconds   
                   n_intervals=0
               )
         ], style={'background':'rgba(30,41,59,0.5)','borderRadius':'16px','padding':'20px','margin':'15px 0','border':'1px solid rgba(148,163,184,0.1)','backdropFilter':'blur(10px)','boxShadow':'0 8px 32px rgba(0,0,0,0.2)'}),
        #figure 12: heatmap of profit by category and campaign
        html.Div([
            html.H2('Profit by Category and Campaign'),
            dcc.Graph(id='profit_by_category_campaign_fig', figure=profit_by_category_campaign_heatmap),
                dcc.Interval(
                    id='interval_component_category_campaign',   
                    interval=5000,  # refresh every 5 seconds   
                    n_intervals=0
                )  
        ], style={'background':'rgba(30,41,59,0.5)','borderRadius':'16px','padding':'20px','margin':'15px 0','border':'1px solid rgba(148,163,184,0.1)','backdropFilter':'blur(10px)','boxShadow':'0 8px 32px rgba(0,0,0,0.2)'})       
                       
           
], style={'maxWidth':'1400px','margin':'0 auto','padding':'0 20px 40px 20px'})




# Callbacks for interactivity and live updates




#profit per quarter callback
@app.callback(
    Output('profit_per_region_fig', 'figure'),
    [Input('dropdown_region', 'value'),
     Input('interval_component', 'n_intervals')]
)

def update_profit_per_quarter(selected_region, n_intervals):
    df = pd.read_csv(dataset_path)  # reload to simulate live updates
    if selected_region is None:
        profit_by_quarter = df.groupby('quarter')['profit_egp'].sum().reset_index()
    else:
        filtered_df = df[df['region'] == selected_region]
        profit_by_quarter = filtered_df.groupby('quarter')['profit_egp'].sum().reset_index()
    
    return px.bar(profit_by_quarter, x='quarter', y='profit_egp', template='plotly_dark', color_discrete_sequence=['#34d399'])


#revenue per quarter callback
@app.callback(
    Output('revenue_per_quarter_fig', 'figure'),
    [Input('dropdown_region_revenue', 'value'),
     Input('interval_component_revenue', 'n_intervals')]
)

def update_revenue_per_quarter(selected_region, n_intervals):
    df = pd.read_csv(dataset_path)  # reload to simulate live updates
    if selected_region is None:
        revenue_by_quarter = df.groupby('quarter')['revenue_egp'].sum().reset_index()
    else:
        filtered_df = df[df['region'] == selected_region]
        revenue_by_quarter = filtered_df.groupby('quarter')['revenue_egp'].sum().reset_index()
    return px.bar(revenue_by_quarter, x='quarter', y='revenue_egp', template='plotly_dark', color_discrete_sequence=['#60a5fa'])


#monthly revenue trend callback
@app.callback(
    Output('monthly_revenue_trend_fig', 'figure'),
    [Input('interval_component_monthly', 'n_intervals'),
     Input('dropdown_region_monthly', 'value'),
     Input('dropdown_category_monthly', 'value')]
)
def update_monthly_revenue_trend(n_intervals, selected_region, selected_category):
    df = pd.read_csv(dataset_path)
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

    filtered_df = df.copy()
    if selected_region is not None:
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    if selected_category is not None:
        filtered_df = filtered_df[filtered_df['category'] == selected_category]

    monthly_revenue = (
        filtered_df.groupby(filtered_df['order_date'].dt.to_period('M'))['revenue_egp']
        .sum()
        .reset_index()
    )
    monthly_revenue['order_date'] = monthly_revenue['order_date'].dt.to_timestamp()

    return px.line(monthly_revenue, x='order_date', y='revenue_egp', title='Monthly Revenue Trend', template='plotly_dark', color_discrete_sequence=['#60a5fa'])

#monthly profit trend callback
@app.callback(
    Output('monthly_profit_trend_fig', 'figure'),
    [Input('interval_component_monthly_profit', 'n_intervals'),
     Input('dropdown_region_monthly_profit', 'value'),
     Input('dropdown_category_monthly_profit', 'value')]
)
def update_monthly_profit_trend(n_intervals, selected_region, selected_category):
    df = pd.read_csv(dataset_path)
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

    filtered_df = df.copy()
    if selected_region is not None:
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    if selected_category is not None:
        filtered_df = filtered_df[filtered_df['category'] == selected_category]

    monthly_profit = (
        filtered_df.groupby(filtered_df['order_date'].dt.to_period('M'))['profit_egp']
        .sum()
        .reset_index()
    )
    monthly_profit['order_date'] = monthly_profit['order_date'].dt.to_timestamp()

    return px.line(monthly_profit, x='order_date', y='profit_egp', title='Monthly Profit Trend', template='plotly_dark', color_discrete_sequence=['#34d399'])



#category revenue distribution callback
@app.callback(
    Output('category_revenue_fig', 'figure'),
    [Input('dropdown_region_category', 'value'),
     Input('interval_component_category', 'n_intervals')]
)

def update_category_revenue(selected_region, n_intervals):
    df = pd.read_csv(dataset_path)  # reload to simulate live updates
    if selected_region is None:
        category_revenue = df.groupby('category')['revenue_egp'].sum().reset_index()
    else:
        filtered_df = df[df['region'] == selected_region]
        category_revenue = filtered_df.groupby('category')['revenue_egp'].sum().reset_index()
    return px.bar(category_revenue, x='category', y='revenue_egp', title='Revenue by Category', color='category', template='plotly_dark', color_discrete_sequence=px.colors.sequential.Blues) 


#category profit distribution callback
@app.callback(
    Output('category_profit_fig', 'figure'),
    [Input('dropdown_region_category_profit', 'value'),
     Input('interval_component_category_profit', 'n_intervals')]
)

def update_category_profit(selected_region, n_intervals):
    df = pd.read_csv(dataset_path)  # reload to simulate live updates
    if selected_region is None:
        category_profit = df.groupby('category')['profit_egp'].sum().reset_index()
    else:
        filtered_df = df[df['region'] == selected_region]
        category_profit = filtered_df.groupby('category')['profit_egp'].sum().reset_index()
    return px.bar(category_profit, x='category', y='profit_egp', title='Profit by Category', color='category', template='plotly_dark', color_discrete_sequence=px.colors.sequential.Greens)


#segment revenue callback
@app.callback(
    Output('segment_revenue_fig', 'figure'),
    [Input('dropdown_age_group_segment', 'value'),
     Input('interval_component_segment', 'n_intervals')]
)
def update_segment_revenue(selected_age_group, n_intervals):
    df = pd.read_csv(dataset_path)
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

    filtered_df = df.copy()
    if selected_age_group is not None:
        filtered_df = filtered_df[filtered_df['age_group'] == selected_age_group]

    segment_revenue = filtered_df.groupby('customer_segment')['revenue_egp'].sum().reset_index()
    return px.pie(segment_revenue, names='customer_segment', values='revenue_egp', title='Revenue by Customer Segment', template='plotly_dark')

#revenue by city callback
@app.callback(
    Output('revenue_by_city_fig', 'figure'),
    [Input('dropdown_category_city', 'value'),
     Input('interval_component_city', 'n_intervals')]
)

def update_revenue_by_city(selected_category, n_intervals):
    df = pd.read_csv(dataset_path)  # reload to simulate live updates
    if selected_category is None:
        revenue_by_city = df.groupby('city')['revenue_egp'].sum().reset_index()
    else:
        filtered_df = df[df['category'] == selected_category]
        revenue_by_city = filtered_df.groupby('city')['revenue_egp'].sum().reset_index()
    return px.treemap(revenue_by_city, path=['city'], values='revenue_egp', title='Revenue by City', template='plotly_dark', color_continuous_scale='Blues')


#sales channel performance callback
@app.callback(
    Output('sales_channel_performance_fig', 'figure'),
    [Input('interval_component_sales_channel', 'n_intervals')]
)

def update_sales_channel_performance(n_intervals):
    df = pd.read_csv(dataset_path)  # reload to simulate live updates
    sales_channel_performance = df.groupby('sales_channel')['revenue_egp'].sum().reset_index()
    return px.pie(sales_channel_performance, names='sales_channel', values='revenue_egp', title='Revenue by Sales Channel', template='plotly_dark')


#revenue by campaign callback
@app.callback(
    Output('revenue_by_campaign_fig', 'figure'),
    [Input('dropdown_category_campaign', 'value'),
     Input('interval_component_campaign', 'n_intervals')]
)

def update_revenue_by_campaign(selected_category, n_intervals):
    df = pd.read_csv(dataset_path)  # reload to simulate live updates
    if selected_category is None:
        revenue_by_campaign = df.groupby('campaign')['revenue_egp'].sum().reset_index()
    else:
        filtered_df = df[df['category'] == selected_category]
        revenue_by_campaign = filtered_df.groupby('campaign')['revenue_egp'].sum().reset_index()
    return px.bar(revenue_by_campaign, x='campaign', y='revenue_egp', title='Revenue by Campaign', color='campaign', template='plotly_dark')


#revenue by traffic source callback
@app.callback(
    Output('revenue_by_traffic_source_fig', 'figure'),
    [Input('dropdown_category_traffic_source', 'value'),
     Input('interval_component_traffic_source', 'n_intervals')]
)

def update_revenue_by_traffic_source(selected_category, n_intervals):
    df = pd.read_csv(dataset_path)  # reload to simulate live updates
    if selected_category is None:
        revenue_by_traffic_source = df.groupby('traffic_source')['revenue_egp'].sum().reset_index()
    else:
        filtered_df = df[df['category'] == selected_category]
        revenue_by_traffic_source = filtered_df.groupby('traffic_source')['revenue_egp'].sum().reset_index()
    return px.bar(revenue_by_traffic_source, x='traffic_source', y='revenue_egp', title='Revenue by Traffic Source', color='traffic_source', template='plotly_dark')


#profit by category and campaign heatmap callback
@app.callback(
    Output('profit_by_category_campaign_fig', 'figure'),
    [Input('interval_component_category_campaign', 'n_intervals')]
)

def update_profit_by_category_campaign(n_intervals):
    df = pd.read_csv(dataset_path)  # reload to simulate live updates
    profit_by_category_campaign = df.groupby(['category', 'campaign'])['profit_egp'].sum().reset_index()
    return px.imshow(profit_by_category_campaign.pivot(index='category', columns='campaign', values='profit_egp'), title='Profit by Category and Campaign', color_continuous_scale='Viridis', template='plotly_dark')    


# Run app
app.run()

