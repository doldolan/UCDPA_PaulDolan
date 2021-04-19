import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from bokeh.io import output_file,show, curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource,HoverTool
# import geopandas as gpd
import folium

Customers = pd.read_csv(r"C:\Users\Paul Dolan\Downloads\UCD Project\CUSTOMER.csv")


# Creating a function to cleanse the csv file and keeping the changes
def data_clean(path):
    new_data = pd.read_csv(path)
    new_data.drop_duplicates(inplace=True)
    new_data.fillna('Unknown', inplace=True)
    return new_data

# Running my function on Customers csv
data_clean(r"C:\Users\Paul Dolan\Downloads\UCD Project\CUSTOMER.csv")

# Looking at the first few rows of data
print(Customers.head())

# Printing the unique countries from customers table
print(Customers.Country.unique())

# Creating a dictionary to replace the 2 letter country names to full country names and saving the changes
# into the same table
Customers['Country'].replace({'US': 'United States', 'AU': 'Australia', 'CA': 'Canada',
                              'DE': 'Germany', 'IL': 'Israel', 'TR': 'Turkey',
                              'ZA': 'South Africa'}, inplace=True)
# Checking to see if my dictionary worked
print(Customers.Country.unique())

# Checking for any columns that are blank and dropping them and keeping the changes to the existing table
Customers.info()
Customers.dropna(axis=1, inplace=True)
Customers.info()


# Loading in Orders Fact table
Orders_Fact = pd.read_csv(r"C:\Users\Paul Dolan\Downloads\UCD Project\ORDER_FACT.csv")

# Looking at column information in the table
print(Orders_Fact.info())

# I noticed there was blanks in the Discount column so I wanted to get a count of how many
print(Orders_Fact.isna().sum())

# Replacing the blanks with 0s in the Discount column & checking to see if the .fillna function worked
Orders_Fact['Discount'] = Orders_Fact['Discount'].fillna(0)
print(Orders_Fact.isna().sum())

# Adding in a year and month column for the Order Dates ahead of the visuals
Orders_Fact['Order_Year'] = pd.DatetimeIndex(Orders_Fact['Order_Date']).year
Orders_Fact['Order_Month'] = pd.DatetimeIndex(Orders_Fact['Order_Date']).month

# Creating a new column and using numpy to compare the order date and delivery date to see if they match
Orders_Fact['Same_Day_Delivery'] = np.where(Orders_Fact['Order_Date'] == Orders_Fact['Delivery_Date'], 'Yes', 'No')
print(Orders_Fact.head())

# Using numpy to see what Employee processed the most orders
print(np.max(Orders_Fact['Employee_ID']))

# Creating a loop to see how many orders have over 3 quantities and printing the result
count = 0
for largequantity in Orders_Fact['Quantity']:
    if (largequantity > 3):
        count += 1
print(count, 'orders where they have over 3 quantities')


# Loading in Product table
Product_Dim = pd.read_csv(r"C:\Users\Paul Dolan\Downloads\UCD Project\PRODUCT_DIM.csv")
Product_Dim.info()

# Finding out which Product Line is the most popular and printing the first 30
print(Product_Dim['Product_Line'].value_counts().idxmax())

# Looping through the table to match up
for index, row in Product_Dim.iloc[:30].iterrows():
    print(row['Product_ID'], row['Product_Name'])


# Joining the Orders Fact and the Products Dim table
Product_Ordered = pd.merge(Orders_Fact, Product_Dim)
print(Product_Ordered.info())

# Joining the Orders Fact and the Customers table
Customers_Orders = pd.merge(Orders_Fact, Customers)
print(Customers_Orders.info())

# The Total Retail price column had a $ in front of the number and I needed to remove them and change the format so I
# could use in my charts
Product_Ordered["Total_Retail_Price"] = Product_Ordered["Total_Retail_Price"].str.replace('$', '')
Product_Ordered["Total_Retail_Price"].str.strip()
Product_Ordered["Total_Retail_Price"] = pd.to_numeric(Product_Ordered["Total_Retail_Price"], errors='coerce')


# First visual
productsalesyear = Product_Ordered.groupby("Order_Year")["Product_Group"].count()
Years = Product_Ordered.Order_Year.unique()

sns.set(style="ticks")
sns.set_palette("nipy_spectral")

productsalesyear.plot(kind="line", linewidth=4, cmap='tab10')
plt.xticks(Years)
plt.xlabel("Year")
plt.ylabel("Total Orders")
plt.title('Year by Year Orders')
plt.show()

# Second visual
prodmonth = Product_Ordered.groupby("Order_Month")["Quantity"].count()
Months = Orders_Fact.Order_Month.unique()


plt.plot(Months, prodmonth, linestyle="--", alpha=0.7)
plt.xticks(Months)
plt.xlabel("Month")
plt.ylabel("Quantities")
plt.title('Total Order Quantities Month by Month')
plt.grid()
plt.show()

# Third visual
sns.set(style="whitegrid")
sns.set_palette("colorblind")

fig, ax = plt.subplots()
sns.countplot(x='Product_Line', data=Product_Ordered, order=Product_Ordered['Product_Line'].value_counts().index)
ax.set_xlabel("Product Line")
ax.set_ylabel("Orders")
ax.set_title("Total Product Lines Sold")
plt.show()

# Fourth visual
product_sales = Product_Ordered.groupby("Product_Category")["Total_Retail_Price"].sum()

sns.set_style("dark")
sns.set_palette("dark")

product_sales.plot.barh(figsize=(8, 8))
plt.xlabel("Total Revenue", fontweight="bold", fontsize="12")
plt.ylabel("Product Category", fontweight="bold", fontsize="12")
plt.title('Sales by Product Categories', fontweight="bold", fontsize="18")
plt.show()

# Fifth visual
sns.set_style("whitegrid")
sns.set_palette("brg")

CustSeg = sns.catplot(x="Country", kind="count", data=Customers_Orders, hue="Gender")
plt.xticks(rotation=90)
CustSeg.fig.suptitle("Customer Gender by Country")
CustSeg.set(ylabel="Total Orders")
plt.show()

# Bokeh Chart
source = ColumnDataSource(Product_Ordered)

hover = HoverTool(tooltips = [("Product Line", "@Product_Line"), ("Product", "@Product_Name"), ("Price",
"@CostPrice_Per_Unit")], mode="hline")

curdoc().theme = "light_minimal"
plot = figure(tools=[hover, "crosshair", "wheel_zoom","box_select"])
plot.circle(x="Order_Year", y="Total_Retail_Price", source=source, selection_color="red", hover_color= "blue",
            alpha=0.7)
output_file("Product Orders Detail.html")
show(plot)


# Geospatial Analysis
IrelandCovidStats = gpd.read_file(r'C:\Users\Paul Dolan\Downloads\
UCD Project\Covid19CountyStatisticsHPSCIreland.geojson')

# Making sure the file is using the standard coordinate reference system like Google Maps
IrelandCovidStats.to.crs(3857)

# Creating a starting point of the Ireland map
Irelandmap = folium.map(location=[53.1424, 7.6921], zoom_start=2, tiles="Stamen Terrain")

# Building a for loop to get the multiple latitude and longitude points from dataframe and adding it the map
for i in range(0, len(IrelandCovidStats)):
    folium.Marker(
        location=[IrelandCovidStats.iloc[i]['lat'], IrelandCovidStats.iloc[i]['long']],
        popup=IrelandCovidStats.iloc[i]['CountyName']).add_to(Irelandmap)

display(Irelandmap)
