import pandas as pd
import os 

c_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(c_dir, 'ecomdata.csv')

df = pd.read_csv(file_path, encoding='ISO-8859-1')


print(df.columns)
print("--- Column Data Types & Non-Null Counts ---")
print(df.info())
print("---------molakhas--------")
print(df[['Quantity', 'UnitPrice']].describe())
print("-----see some quantity and unit price chunks--------")
negative_check = df[(df['Quantity'] < 0) | (df['UnitPrice'] < 0)]
print(negative_check.head(10))

print("----real calc work------")
df_clean = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)].copy()

print(f"Original shape: {df.shape}")
print(f"Cleaned shape: {df_clean.shape}")

print("\nNew Summary Statistics:")
print(df_clean[['Quantity', 'UnitPrice']].describe())

very_cheap = df_clean[df_clean['UnitPrice'] < 0.1]
print(very_cheap[['Description', 'Quantity', 'UnitPrice']].head(10))
print("----date fix------")
df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])

print(df_clean['InvoiceDate'].dtype)

print(df_clean['InvoiceDate'].head())
print("---- the 3 new columns----")

df_clean['Month'] = df_clean['InvoiceDate'].dt.month

df_clean['Day_Name'] = df_clean['InvoiceDate'].dt.day_name()

df_clean['Hour'] = df_clean['InvoiceDate'].dt.hour

print(df_clean[['InvoiceDate', 'Month', 'Day_Name', 'Hour']].head())
print("--------clean description-------")
df_clean['Description'] = df_clean['Description'].str.upper()
df_clean['Description'] = df_clean['Description'].str.strip()

hourly_sales = df_clean['Hour'].value_counts().sort_index()

print("---hour calc---")
print(hourly_sales)
print(df.columns)
print(df.info())
print("----filling missings in des and price---")
desc_map = df_clean.groupby('StockCode')['Description'].first()
price_map = df_clean.groupby('StockCode')['UnitPrice'].median()

df_clean['Description'] = df_clean['Description'].fillna(df_clean['StockCode'].map(desc_map))
df_clean['UnitPrice'] = df_clean['UnitPrice'].fillna(df_clean['StockCode'].map(price_map))

before_drop = len(df_clean)
df_clean = df_clean.dropna(subset=['Description', 'UnitPrice'], how='all')
after_drop = len(df_clean)

print(f"Rows removed because both Description and UnitPrice were missing: {before_drop - after_drop}")
print("--- Check for missing values after imputation ---")
print(df_clean.info())
print("Minimum Quantity:", df_clean['Quantity'].min())
print("Maximum Quantity:", df_clean['Quantity'].max())
df_clean['Total_Sales'] = df_clean['Quantity'] * df_clean['UnitPrice']

print("--- Top 5 highest value transactions ---")
print(df_clean[['Description', 'Quantity', 'UnitPrice', 'Total_Sales']].sort_values(by='Total_Sales', ascending=False).head())

# Filling missing CustomerIDs with 0 to represent 'Guest' transactions
df_clean['CustomerID'] = df_clean['CustomerID'].fillna(0)

df_clean['CustomerID'] = df_clean['CustomerID'].astype(int)
print(df_clean.info())
df_clean.to_csv('cleaned1_ecommerecedata.csv', index=False)