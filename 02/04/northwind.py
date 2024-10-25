import mysql.connector as connector
import pandas as pd
import matplotlib.pyplot as plt

# Create connection to the MySQL database
db = connector.connect(
    host="localhost", 
    user="baht",  
    password="", 
    database="northwind",  
    use_pure=True
)


# Retrieve tables from the database
orders = pd.read_sql("select * from orders",db)
employees = pd.read_sql("select * from employees",db)
shippers = pd.read_sql("select * from shippers",db)

# close database connection
db.close()

# Group orders by ShipCountry, count orderID's in each group, reset/create a new index, count, with the size of each group.
oBcountry = orders.groupby("ShipCountry")["OrderID"].count().reset_index(name="count")

# Join the tables orders and shippers together with ShipVia on ShipperID, 
# then group joined table by company name, 
# and reset/create a new index, count, with the size of each group.
oBshipper = pd.merge(orders, shippers, left_on="ShipVia", right_on="ShipperID").groupby("CompanyName").size().reset_index(name="count")


# convert OrderDate column in orders from string to DateTime.
orders['OrderDate'] = pd.to_datetime(orders["OrderDate"])      
# Create a new column with DateTime converted to PeriodIndex ( ndarray which month and year they fall in )             
orders['year_month'] = orders["OrderDate"].dt.to_period(('M'))    
# Group orders by PeriodIndex, reset/create a new index, count, with the size of each group.      
oBtime = orders.groupby(['year_month']).size().reset_index(name="count")   
# Convert PeriodIndex to timestamp for plotting
oBtime['year_month'] = oBtime['year_month'].dt.to_timestamp()


# Create bar chart showing the amount of orders to each country
plt.figure(figsize=(15, 5))
plt.bar(oBcountry["ShipCountry"], oBcountry["count"], color='skyblue')
plt.title('Orders by Shipping country')
plt.ylabel('Count')
plt.xticks(rotation=45) 
plt.tight_layout()

# Create bar chart showing the amount of orders shipped by each shipping company
plt.figure(figsize=(6, 5))
plt.bar(oBshipper["CompanyName"], oBshipper["count"], color='skyblue')
plt.title('Orders by Shipper')
plt.ylabel('Count')
plt.tight_layout()

# Create a line chart showing the amount of monthly orders over time.
plt.figure(figsize=(7, 7))
plt.plot(oBtime["year_month"], oBtime["count"], marker='o', linestyle='-', color='b') 
plt.title('Monthly Orders Over Time')
plt.xlabel('Year-Month')
plt.ylabel('Orders')
plt.xticks(rotation=45) 
plt.grid(True)
plt.tight_layout()

# Show all the charts
plt.show()