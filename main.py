import matplotlib as plt
import numpy as np
import pandas as pd
import seaborn as sns

Customers = pd.read_csv(r"C:\Users\Paul Dolan\Downloads\UCD Project\CUSTOMER.csv")
Orders_Fact = pd.read_csv(r"C:\Users\Paul Dolan\Downloads\UCD Project\ORDER_FACT.csv")
Product_Dim = pd.read_csv(r"C:\Users\Paul Dolan\Downloads\UCD Project\PRODUCT_DIM.csv")

# Checking to see if there is any blank values in any of the Customers columns
Customers.info()
Customers.dropna(axis=1, inplace=True)

# Counting missing values in each column in Orders_Fact table
print(Orders_Fact.isna().sum())
Orders_Fact['Discount'] = Orders_Fact['Discount'].fillna(0)
print(Orders_Fact.isna().sum())

# Using a dictionary and replace() to map to proper country names
Customers['Country'].replace({'US': 'United States', 'AU': 'Australia', 'CA': 'Canada',
                                                       'DE': 'Germany', 'IL': 'Israel', 'TR': 'Turkey',
                                                       'SA': 'South Africa'}, inplace=True)
print(Customers['Country'])

# iterate through each row and select productID and Product Name
for index, row in Product_Dim.iterrows():
    print(row['Product_ID'], row['Product_Name'])

# using numpy aggregate functions to get the mean. The data type needs to right for it tot work
print(Orders_Fact['Customer_ID'].mean())

max_retail_price = Orders_Fact['Total_Retail_Price'].max()
print(max_retail_price)