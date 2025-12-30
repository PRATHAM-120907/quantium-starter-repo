import pandas as pd
import glob
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# ==================================================
# DATA PROCESSING
# ==================================================

# Load all CSV files
files = glob.glob("data/daily_sales_data_*.csv")
df = pd.concat([pd.read_csv(file) for file in files], ignore_index=True)

# Normalize column names and values
df.columns = df.columns.str.strip().str.lower()
df['product'] = df['product'].astype(str).str.strip().str.lower()
df['region'] = df['region'].astype(str).str.strip().str.lower()
df['price'] = df['price'].str.replace('$', '', regex=False).astype(float)
df['date'] = pd.to_datetime(df['date'])

# Filter Pink Morsel
pink_df = df[df['product'] == 'pink morsel']

# Create Sales column
pink_df['sales'] = pink_df['price'] * pink_df['quantity']

# Final formatted data
final_df = pink_df[['sales', 'date', 'region']]
final_df.columns = ['Sales', 'Date', 'Region']
final_df = final_df.sort_values(by='Date')

# ==================================================
# DASH APP
# ==================================================

app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        'fontFamily': 'Arial, sans-serif',
        'backgroundColor': '#f4f6f8',
        'padding': '20px'
    },
    children=[

        # Header
        html.H1(
            "Pink Morsel Sales Visualiser",
            style={
                'textAlign': 'center',
                'color': '#2c3e50'
            }
        ),

        html.P(
            "Explore Pink Morsel sales over time and assess the impact of the "
            "price increase on 15 January 2021.",
            style={
                'textAlign': 'center',
                'color': '#555',
                'fontSize': '16px'
            }
        ),

        # Radio Buttons
        html.Div(
            style={
                'textAlign': 'center',
                'marginBottom': '20px'
            },
            children=[
                html.Label(
                    "Filter by Region:",
                    style={
                        'fontWeight': 'bold',
                        'marginRight': '10px'
                    }
                ),
                dcc.RadioItems(
                    id='region-filter',
                    options=[
                        {'label': 'All', 'value': 'all'},
                        {'label': 'North', 'value': 'north'},
                        {'label': 'East', 'value': 'east'},
                        {'label': 'South', 'value': 'south'},
                        {'label': 'West', 'value': 'west'}
                    ],
                    value='all',
                    inline=True,
                    style={
                        'fontSize': '14px'
                    }
                )
            ]
        ),

        # Graph
        html.Div(
            style={
                'backgroundColor': 'white',
                'padding': '15px',
                'borderRadius': '8px',
                'boxShadow': '0px 4px 10px rgba(0,0,0,0.1)'
            },
            children=[
                dcc.Graph(id='sales-line-chart')
            ]
        )
    ]
)

# ==================================================
# CALLBACK
# ==================================================

@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_chart(selected_region):
    if selected_region == 'all':
        filtered_df = final_df
    else:
        filtered_df = final_df[final_df['Region'] == selected_region]

    fig = px.line(
        filtered_df,
        x='Date',
        y='Sales',
        title='Pink Morsel Sales Over Time',
        labels={
            'Date': 'Date',
            'Sales': 'Sales ($)'
        }
    )

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return fig


# ==================================================
# RUN SERVER
# ==================================================

if __name__ == "__main__":
    app.run_server(debug=True)
