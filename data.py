import pandas as pd
import glob

# --------------------------------------------------
# 1. Load all CSV files
# --------------------------------------------------
files = glob.glob("data/daily_sales_data_*.csv")

df_list = [pd.read_csv(file) for file in files]
df = pd.concat(df_list, ignore_index=True)

# --------------------------------------------------
#
# --------------------------------------------------
#
df['price'] = df['price'].str.replace('$', '', regex=False).astype(float)

#
df['date'] = pd.to_datetime(df['date'])

# --------------------------------------------------
# 
df = df[df['product'] == 'Pink Morsel']

# --------------------------------------------------
# 
# --------------------------------------------------
df['Sales'] = df['price'] * df['quantity']

# --------------------------------------------------
#
# --------------------------------------------------
final_df = df[['Sales', 'date', 'region']]
final_df.columns = ['Sales', 'Date', 'Region']

# ------------------------------
# --------------------------------------------------
final_df.to_csv("data/processed_pink_morsel_sales.csv", index=False)

print("Output file created: processed_pink_morsel_sales.csv")


cutoff_date = pd.to_datetime("2021-01-15")

before_sales = final_df[final_df['Date'] < cutoff_date]['Sales'].sum()
after_sales = final_df[final_df['Date'] >= cutoff_date]['Sales'].sum()

print(f"Total sales BEFORE Jan 15, 2021: ${before_sales:,.2f}")
print(f"Total sales AFTER Jan 15, 2021: ${after_sales:,.2f}")

if after_sales > before_sales:
    print("Sales increased after the price increase.")
else:
    print("Sales decreased after the price increase.")
