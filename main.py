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
