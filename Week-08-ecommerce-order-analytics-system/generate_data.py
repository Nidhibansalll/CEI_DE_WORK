# Creates customers.csv, products.csv, orders.csv, order_items.csv with some intentional data issues (missing ids, bad dates, bad emails, etc.)
import random, os
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
random.seed(42)
Faker.seed(42)
# output directory for raw data files
RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

N_CUSTOMERS, N_PRODUCTS, N_ORDERS = 600, 550, 1500
CATEGORIES = {
    "Electronics": ["Mobiles", "Laptops", "Accessories", "Cameras"],
    "Clothing": ["Men", "Women", "Kids", "Footwear"],
    "Home": ["Kitchen", "Furniture", "Decor", "Bedding"],
    "Books": ["Fiction", "Non-Fiction", "Academic", "Comics"],
}
STATUS_POOL = ["DELIVERED"]*45 + ["SHIPPED"]*20 + ["PLACED"]*15 + ["CANCELLED"]*10 + ["RETURNED"]*10
CUSTOMER_TYPE_POOL = ["REGULAR"]*65 + ["PREMIUM"]*25 + ["VIP"]*10
REGIONS = ["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"]

def messy(text):
    r = random.random()
    if r < 0.4: return f"  {text}  "
    if r < 0.7: return text.upper()
    return text.lower()

def customers():
    rows = []
    for cid in range(1, N_CUSTOMERS + 1):
        name = fake.name()
        email = f"{name.split()[0].lower()}.{name.split()[-1].lower()}{cid}@{fake.free_email_domain()}"
        if random.random() < 0.02:  # 2% invalid emails
            email = email.replace("@", "") if random.random() < 0.5 else email.split("@")[0]
        reg = fake.date_between(start_date=datetime(2023, 1, 1), end_date=datetime(2025, 12, 31))
        rows.append([cid, name, email, reg.strftime("%Y-%m-%d"), random.choice(CUSTOMER_TYPE_POOL)])
    df = pd.DataFrame(rows, columns=["customer_id", "customer_name", "email", "registration_date", "customer_type"])
    df.to_csv(os.path.join(RAW_DIR, "customers.csv"), index=False)
    print("customers.csv ->", len(df), "rows")
    return df

def products():
    rows = []
    for pid in range(1, N_PRODUCTS + 1):
        cat = random.choice(list(CATEGORIES))
        sub = random.choice(CATEGORIES[cat])
        noun = sub[:-1] if sub.endswith("s") else sub
        name = f"{fake.word().title()} {noun}"
        if random.random() < 0.10:  # messy names
            name = messy(name)
        rows.append([pid, name, cat, sub, round(random.uniform(100, 15000), 2)])
    df = pd.DataFrame(rows, columns=["product_id", "product_name", "category", "subcategory", "cost_price"])
    df.to_csv(os.path.join(RAW_DIR, "products.csv"), index=False)
    print("products.csv ->", len(df), "rows")
    return df

def orders(cust_df):
    reg_map = dict(zip(cust_df.customer_id, cust_df.registration_date))
    cust_ids = cust_df.customer_id.tolist()
    start, end = datetime(2024, 1, 1), datetime(2026, 6, 30)
    rows = []
    for oid in range(1, N_ORDERS + 1):
        cid = random.choice(cust_ids)
        reg = datetime.strptime(reg_map[cid], "%Y-%m-%d")
        lo = max(start, reg) if max(start, reg) < end else start
        dt = lo + timedelta(seconds=random.randint(0, int((end - lo).total_seconds())))
        date_str = dt.strftime("%d-%m-%Y") if random.random() < 0.06 else dt.strftime("%Y-%m-%d %H:%M:%S")
        final_cid = "" if random.random() < 0.05 else cid
        rows.append([oid, final_cid, date_str, random.choice(STATUS_POOL), random.choice(REGIONS)])

    # for the last 2 rows, set order_date to a future date (to test date validation)
    for r in rows[-2:]:
        r[2] = (datetime.now() + timedelta(days=random.randint(10, 60))).strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame(rows, columns=["order_id", "customer_id", "order_date", "status", "region_code"])
    df.to_csv(os.path.join(RAW_DIR, "orders.csv"), index=False)
    print("orders.csv ->", len(df), "rows")
    return df

def order_items(orders_df, products_df):
    order_ids = orders_df.order_id.tolist()
    product_ids = products_df.product_id.tolist()
    rows, iid = [], 1
    for oid in order_ids:
        for pid in random.sample(product_ids, k=random.randint(1, 4)):
            qty = random.randint(1, 5)
            roll = random.random()
            if roll < 0.03: qty = -qty        # return
            elif roll < 0.035: qty = 0        # rare zero-qty row
            price = round(random.uniform(150, 20000), 2)
            disc = round(random.uniform(100, 150), 1) if random.random() < 0.003 else round(random.uniform(0, 40), 1)
            rows.append([iid, oid, pid, qty, price, disc])
            iid += 1

    # 12 orphan rows: order_id that was never created above
    for _ in range(12):
        rows.append([iid, max(order_ids) + random.randint(1000, 9999), random.choice(product_ids),
                     random.randint(1, 3), round(random.uniform(150, 20000), 2), round(random.uniform(0, 40), 1)])
        iid += 1

    # 15 exact duplicate rows 
    for original in random.sample(rows, 15):
        dup = original.copy()
        dup[0] = iid
        rows.append(dup)
        iid += 1

    df = pd.DataFrame(rows, columns=["item_id", "order_id", "product_id", "quantity", "unit_price", "discount_percent"])
    df.to_csv(os.path.join(RAW_DIR, "order_items.csv"), index=False)
    print("order_items.csv ->", len(df), "rows (12 orphan, 15 duplicate)")
    return df

if __name__ == "__main__":
    c = customers()
    p = products()
    o = orders(c)
    order_items(o, p)
    print("Done. Files are in!")
