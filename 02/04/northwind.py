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

cursor = db.cursor()

orders = pd.read_sql("select * from orders",db)
employees = pd.read_sql("select * from employees",db)

db.close()


bEC = pd.merge(orders, employees, on="EmployeeID", how="inner").groupby("Country").size().reset_index(name="count")


bSC = orders.groupby("ShipCountry")["OrderID"].count().reset_index(name="count")


plt.figure(figsize=(18, 5))

plt.subplot(1, 1, 1)
plt.bar(bSC["ShipCountry"], bSC["count"], color='skyblue')
plt.title('Orders by Shipping country')
plt.ylabel('Count')
plt.tight_layout()

plt.figure(figsize=(4, 5))
plt.subplot(1, 1, 1)
plt.bar(bEC["Country"], bEC["count"], color='skyblue')
plt.title('Orders by Employee country')
plt.ylabel('Count')
plt.tight_layout()


plt.show()