import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load the dataset
df = pd.read_csv('Online Retail Dataset.csv', encoding='ISO-8859-1')
# Preview the data

print(df.head())

# Check data types and nulls
df.info()
# Summary statistics
df.describe()
# Count missing values
df.isnull().sum()

# Drop rows with missing CustomerID
df_clean = df.dropna(subset=['CustomerID']).copy()
# Filter out non-positive quantities (returns) and zero unit prices
df_clean = df_clean[(df_clean['Quantity'] > 0) & (df_clean['UnitPrice'] > 0)].copy()
# Create TotalPrice feature
df_clean['TotalPrice'] = df_clean['Quantity'] * df_clean['UnitPrice']
# Convert InvoiceDate to datetime format with explicit mixed handling
df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'], format='mixed')
# Extract Year and Month into new columns
df_clean['InvoiceYear'] = df_clean['InvoiceDate'].dt.year
df_clean['InvoiceMonth'] = df_clean['InvoiceDate'].dt.month
monthly_sales = df_clean.groupby(['InvoiceYear',
'InvoiceMonth'])['TotalPrice'].sum().reset_index()
# Convert InvoiceYear to string for discrete line hue encoding
monthly_sales['InvoiceYear'] = monthly_sales['InvoiceYear'].astype(str)
plt.figure(figsize=(10, 6))
sns.lineplot(data=monthly_sales, x='InvoiceMonth', y='TotalPrice', hue='InvoiceYear',
marker='o')
plt.title('Monthly Revenue Trend')
plt.xlabel('Month')
plt.ylabel('Total Revenue (£)')
plt.tight_layout()
plt.show()

country_sales = (df_clean.groupby('Country')['TotalPrice']
 .sum()
 .sort_values(ascending=False)
 .head(10))
plt.figure(figsize=(10, 6))
sns.barplot(x=country_sales.values, y=country_sales.index,
 hue=country_sales.index, palette='viridis', legend=False)
plt.title('Top 10 Countries by Revenue')
plt.xlabel('Revenue (£)')
plt.ylabel('Country')
plt.tight_layout()
plt.show()


