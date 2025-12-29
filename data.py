import pandas as pd
import glob
import dash
from dash import dcc, html
import plotly.express as px

# ==================================================
# PART 1: DATA PROCESSING
# ==================================================

# Load all CSV files
files = glob.glob("data/daily_sales_data_*.csv")
df = pd.concat([pd.read_csv(file) for file in files], ignore_index=True)

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Clean and normalize data
df['product'] = df['product'].astype(str).str.strip().str.lower()
df['price'] = df['price'].str.replace('$', '', regex=False).astype(float)
df['date'] = pd.to_datetime(df['date'])

# Filter only Pink Morsel
pink_df = df[df['product'] == 'pink morsel']

# Create Sales column
pink_df['sales'] = pink_df['price'] * pink_df['quantity']

# Final formatted DataFrame
final_df = pink_df[['sales', 'date', 'region']]
final_df.columns = ['Sales', 'Date', 'Region']

# Save processed CSV
final_df.to_csv("data/processed_pink_morsel_sales.csv", index=False)

print("✅ processed_pink_morsel_sales.csv created successfully")
print(final_df.head())

# ==================================================
# PART 2: DASH VISUALISER
# ==================================================

# Sort by date
final_df = final_df.sort_values(by='Date')

# Create line chart
fig = px.line(
    final_df,
    x='Date',
    y='Sales',
    color='Region',
    title='Pink Morsel Sales Before and After Price Increase',
    labels={
        'Date': 'Date',
        'Sales': 'Sales ($)',
        'Region': 'Region'
    }
)

# Dash app
app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(
            "Pink Morsel Sales Visualiser",
            style={'textAlign': 'center'}
        ),

        html.P(
            "This visualisation shows Pink Morsel sales over time. "
            "The price increase occurred on 15 January 2021. "
            "From the chart, it is clear whether sales were higher before or after the increase.",
            style={'textAlign': 'center'}
        ),

        dcc.Graph(
            figure=fig
        )
    ]
)

# Run server
if __name__ == "__main__":
    app.run(debug=True)
