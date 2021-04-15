import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import bokeh.io
import bokeh.plotting
import bokeh.palettes

Customers = pd.read_csv(r"C:\Users\Paul Dolan\Downloads\UCD Project\CUSTOMER.csv")


# Creating a function to cleanse the csv file and keeping the changes
def data_clean(path):
    new_data = pd.read_csv(path)
    new_data.drop_duplicates(inplace=True)
    new_data.fillna('Unknown', inplace=True)
    return new_data


print(Customers.head())

# Running my function on Customers csv
data_clean(r"C:\Users\Paul Dolan\Downloads\UCD Project\CUSTOMER.csv")

# Getting the unique countries from customers table
print(Customers.Country.unique())

# Creating a dictionary to replace the 2 letter country names to full country names
Customers['Country'].replace({'US': 'United States', 'AU': 'Australia', 'CA': 'Canada',
                              'DE': 'Germany', 'IL': 'Israel', 'TR': 'Turkey',
                              'ZA': 'South Africa'}, inplace=True)
# Checking to see if there is full country names
print(Customers.Country.unique())

# Checking for any columns that are blank and dropping them and keeping the changes to Customers
Customers.info()
Customers.dropna(axis=1, inplace=True)
Customers.info()

# Loading in Orders Fact table
Orders_Fact = pd.read_csv(r"C:\Users\Paul Dolan\Downloads\UCD Project\ORDER_FACT.csv")

# Looking at columns in table
print(Orders_Fact.info())

Orders_Fact['Order_Year'] = pd.DatetimeIndex(Orders_Fact['Order_Date']).year
Orders_Fact['Order_Month'] = pd.DatetimeIndex(Orders_Fact['Order_Date']).month

print(Orders_Fact.Order_Year.unique())

print(Orders_Fact.info())

# I noticed there was blanks in the table so I wanted to get a sense of how many
print(Orders_Fact.isna().sum())

# Replacing the blanks with 0s in the Discount column & checking to see if the .fillna function worked
Orders_Fact['Discount'] = Orders_Fact['Discount'].fillna(0)
print(Orders_Fact.isna().sum())

# Creating a new column and using numpy to compare the order date and delivery date to see if they match
Orders_Fact['Same_Day_Delivery'] = np.where(Orders_Fact['Order_Date'] == Orders_Fact['Delivery_Date'], 'Yes', 'No')
print(Orders_Fact.head())

# Using numpy to see what Employee processed the most orders
print(np.max(Orders_Fact['Employee_ID']))

# Creating a loop to see how many orders have over 3 quantities
count = 0
for largequantity in Orders_Fact['Quantity']:
    if (largequantity > 3):
        count += 1
print(count, 'orders where they have over 3 quantities')

Product_Dim = pd.read_csv(r"C:\Users\Paul Dolan\Downloads\UCD Project\PRODUCT_DIM.csv")
Product_Dim.info()

# Finding out which Product Line is the most popular
print(Product_Dim['Product_Line'].value_counts().idxmax())

# Looping through the table to match up
for index, row in Product_Dim.iterrows():
    print(row['Product_ID'], row['Product_Name'])

# Joining the Orders Fact and the Products Dim table
#Product_Ordered = Orders_Fact.merge(Product_Dim, on='Product_ID', how='left')
Product_Ordered = pd.merge(Orders_Fact, Product_Dim)
print(Product_Ordered.info())

# First visualisaztion
sns.set(style="whitegrid")
sns.set_palette("colorblind")

fig, ax = plt.subplots()
sns.countplot(x='Product_Line', data=Product_Ordered, order=Product_Ordered['Product_Line'].value_counts().index)
ax.set_ylabel("Orders Sold")
ax.set_title("Total Product Lines Sold")
plt.show()
fig.savefig('Viz1.jpg')

# Second visualisation

# Sports = Product_Ordered['Product_Category'].isin(['Golf', 'Soccer'])

#sportsproduct = ["American Football", "Baseball", "Basket Ball", "Darts", "Golf", "Golf Clothes", "Gymnastic Clothing",
                 #"Jogging", "Racket Sports", "Soccer", "Tennis", "Winter Sports"]

