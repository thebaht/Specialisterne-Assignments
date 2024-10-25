import mysql.connector as connector
import pandas as pd
import matplotlib.pyplot as plt

# Create a connection to the MySQL database
db = connector.connect(
    host="localhost",  # The host where your MySQL server is running
    user="baht",  # Your MySQL username
    password="",  # Your MySQL password
    database="northwind",  # The name of the database you want to connect to
    use_pure=True
)



orders = pd.read_sql("select * from orders",db)
employees = pd.read_sql("select * from employees",db)
shippers = pd.read_sql("select * from shippers",db)
db.close()


oBcountry = orders.groupby("ShipCountry")["OrderID"].count().reset_index(name="count")

oBshipper = pd.merge(orders, shippers, left_on="ShipVia", right_on="ShipperID").groupby("CompanyName").size().reset_index(name="count")

orders['OrderDate'] = pd.to_datetime(orders["OrderDate"])
orders['year_month'] = orders["OrderDate"].dt.to_period(('M'))
oBtime = orders.groupby(['year_month']).size().reset_index(name="count")
oBtime['year_month'] = oBtime['year_month'].dt.to_timestamp()



plt.figure(figsize=(15, 5))
plt.bar(oBcountry["ShipCountry"], oBcountry["count"], color='skyblue')
plt.title('Orders by Shipping country')
plt.ylabel('Count')
plt.xticks(rotation=45) 
plt.tight_layout()



plt.figure(figsize=(6, 5))
plt.bar(oBshipper["CompanyName"], oBshipper["count"], color='skyblue')
plt.title('Orders by Shipper')
plt.ylabel('Count')
plt.tight_layout()


plt.figure(figsize=(7, 7))
plt.plot(oBtime["year_month"], oBtime["count"], marker='o', linestyle='-', color='b')  # 'o' for circle markers
plt.title('Monthly Orders Over Time')
plt.xlabel('Year-Month')
plt.ylabel('Orders')
plt.xticks(rotation=45) 
plt.grid(True)
plt.tight_layout()

plt.show()