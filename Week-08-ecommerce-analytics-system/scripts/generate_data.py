""" Generates 4 realistic-messy CSV files for the E-Commerce Order Analytics 
mini project: customers.csv, products.csv, orders.csv, order_items.csv  """
import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
random.seed(42)  # so results are reproducible when i test

OUT = ""

# how many rows we want
NUM_CUSTOMERS = 600
NUM_PRODUCTS = 550
NUM_ORDERS = 3000
NUM_ORDER_ITEMS = 3000


# --------------------------------------------------
# STEP 1: customers.csv
# --------------------------------------------------
customer_types = ["REGULAR", "VIP", "PREMIUM"]
customers = []

for i in range(1, NUM_CUSTOMERS + 1):
    name = fake.name()
    email = name.lower().replace(" ", ".") + str(random.randint(1, 99)) + "@example.com"
    ctype = random.choice(customer_types)
    customers.append([i, name, email, ctype])

# now mess up ~2% of the emails so they're invalid
num_bad_emails = int(NUM_CUSTOMERS * 0.02)
bad_email_rows = random.sample(customers, num_bad_emails)
for row in bad_email_rows:
    email = row[2]
    if "@" in email:
        # randomly remove the @ or the domain
        if random.random() < 0.5:
            row[2] = email.replace("@", "")  # no @ anymore
        else:
            row[2] = email.split("@")[0] + "@"  # no domain

with open(OUT + "customers.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["customer_id", "name", "email", "type"])
    w.writerows(customers)


# --------------------------------------------------
# STEP 2: products.csv
# --------------------------------------------------
products = []
for i in range(1, NUM_PRODUCTS + 1):
    pname = fake.word().capitalize() + " item"
    price = round(random.uniform(50, 5000), 2)
    products.append([i, pname, price])

# mess up some product names - extra spaces 
num_messy_names = int(NUM_PRODUCTS * 0.05)
messy_rows = random.sample(products, num_messy_names)
for row in messy_rows:
    n = row[1]
    r = random.random()
    if r < 0.25:
        row[1] = "  " + n          # leading spaces
    elif r < 0.5:
        row[1] = n + "   "         # trailing spaces
    elif r < 0.75:
        row[1] = n.upper()         # ALL CAPS
    else:
        row[1] = n.lower()         # all lowercase

with open(OUT + "products.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["product_id", "name", "price"])
    w.writerows(products)


# --------------------------------------------------
# STEP 3: orders.csv
# --------------------------------------------------
valid_customer_ids = [row[0] for row in customers]
statuses = ["PLACED", "SHIPPED", "DELIVERED", "RETURNED"]

orders = []
base_date = datetime(2025, 1, 1)
for i in range(1, NUM_ORDERS + 1):
    cust_id = random.choice(valid_customer_ids)
    d = base_date + timedelta(days=random.randint(0, 550))
    date_str = d.strftime("%Y-%m-%d")
    status = random.choice(statuses)
    orders.append([i, cust_id, date_str, status])

# 5% of orders get NULL customer_id
num_null_cust = int(NUM_ORDERS * 0.05)
for row in random.sample(orders, num_null_cust):
    row[1] = ""  # empty = null when read as csv

# some orders get date in DD-MM-YYYY format instead of YYYY-MM-DD
num_bad_dates = int(NUM_ORDERS * 0.04)
for row in random.sample(orders, num_bad_dates):
    parts = row[2].split("-")  # yyyy, mm, dd
    row[2] = parts[2] + "-" + parts[1] + "-" + parts[0]  # flip to dd-mm-yyyy

with open(OUT + "orders.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["order_id", "customer_id", "date", "status"])
    w.writerows(orders)


# --------------------------------------------------
# STEP 4: order_items.csv
# --------------------------------------------------
valid_order_ids = [row[0] for row in orders]
valid_product_ids = [row[0] for row in products]

order_items = []
for _ in range(NUM_ORDER_ITEMS):
    oid = random.choice(valid_order_ids)
    pid = random.choice(valid_product_ids)
    qty = random.randint(1, 5)
    order_items.append([oid, pid, qty])

# 3% negative quantity
num_negative = int(NUM_ORDER_ITEMS * 0.03)
for row in random.sample(order_items, num_negative):
    row[2] = -row[2]

with open(OUT + "order_items.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["order_id", "product_id", "quantity"])
    w.writerows(order_items)


print("done, files are in", OUT)
print("bad emails:", num_bad_emails)
print("messy product names:", num_messy_names)
print("null customer ids:", num_null_cust)
print("bad date format:", num_bad_dates)
print("negative qty:", num_negative)
# total row counts for each file 
print()
print("total rows in customers.csv:", len(customers))
print("total rows in products.csv:", len(products))
print("total rows in orders.csv:", len(orders))
print("total rows in order_items.csv:", len(order_items))
 
