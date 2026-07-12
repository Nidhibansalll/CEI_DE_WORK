# Reads the messy CSVs from data/raw/, cleans them, writes cleaned versions to data/cleaned/, and writes a data quality report of everything found.
import os, re
import pandas as pd
from datetime import datetime

# output directories for cleaned data and reports
RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
CLEAN_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "cleaned")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
os.makedirs(CLEAN_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

issues = {}
def log(section, msg):
    issues.setdefault(section, []).append(msg)

def parse_order_date(val):
    if pd.isna(val) or str(val).strip() == "":
        return pd.NaT
    val = str(val).strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%d-%m-%Y"):
        try:
            return datetime.strptime(val, fmt)
        except ValueError:
            continue
    return pd.NaT

def clean_orders(df):
    df = df.copy()
    df["order_date"] = df["order_date"].apply(parse_order_date)
    bad = df["order_date"].isna().sum()
    if bad:
        log("orders", f"{bad} order_date values unparseable, set to NaT")

    df["customer_id"] = df["customer_id"].replace(["", "NULL", "null"], pd.NA).astype("Int64")
    n_missing = df["customer_id"].isna().sum()
    log("orders", f"{n_missing} orders missing customer_id ({n_missing/len(df):.1%})")

    future = df[df["order_date"] > pd.Timestamp.now()]
    if len(future):
        log("orders", f"{len(future)} orders have a future order_date (ids: {list(future['order_id'])})")
    return df

def clean_products(df):
    df = df.copy()
    before = df["product_name"].copy()
    df["product_name"] = df["product_name"].str.strip().str.title()
    n_changed = (before != df["product_name"]).sum()
    log("products", f"{n_changed} product_name values normalised (spacing/case)")
    return df

def clean_customers(df):
    df = df.copy()
    df["customer_name"] = df["customer_name"].str.strip()
    return df

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def validate_emails(df):
    invalid = ~df["email"].astype(str).apply(lambda e: bool(EMAIL_RE.match(e.strip())))
    ids = df.loc[invalid, "customer_id"].tolist()
    log("customers", f"{len(ids)} customers have an invalid email format")
    return ids

def check_referential_integrity(order_items_df, orders_df):
    valid_ids = set(orders_df["order_id"])
    orphans = order_items_df[~order_items_df["order_id"].isin(valid_ids)]
    if len(orphans):
        log("order_items", f"{len(orphans)} order_items rows reference an order_id not in orders.csv (item_ids: {list(orphans['item_id'])})")
    return orphans

def dedupe_order_items(df):
    cols = ["order_id", "product_id", "quantity", "unit_price", "discount_percent"]
    dup = df.duplicated(subset=cols, keep="first")
    if dup.sum():
        log("order_items", f"{dup.sum()} exact duplicate order_items rows removed (kept first occurrence)")
    return df[~dup]

def clean_order_items(df, orphans):
    df = df.copy()
    df = df[~df["item_id"].isin(orphans["item_id"])]
    df = dedupe_order_items(df)

    neg = df[df["quantity"] < 0]
    log("order_items", f"{len(neg)} rows have negative quantity (returns, kept as-is)")

    zero = df[df["quantity"] == 0]
    if len(zero):
        log("order_items", f"{len(zero)} rows have quantity = 0 (kept, flagged for review)")

    bad_disc = df[(df["discount_percent"] < 0) | (df["discount_percent"] > 100)]
    if len(bad_disc):
        log("order_items", f"{len(bad_disc)} rows had discount_percent outside 0-100, capped")
        df["discount_percent"] = df["discount_percent"].clip(0, 100)
    return df

def main():
    customers = pd.read_csv(os.path.join(RAW_DIR, "customers.csv"))
    products = pd.read_csv(os.path.join(RAW_DIR, "products.csv"))
    orders = pd.read_csv(os.path.join(RAW_DIR, "orders.csv"))
    order_items = pd.read_csv(os.path.join(RAW_DIR, "order_items.csv"))

    customers_clean = clean_customers(customers)
    invalid_emails = validate_emails(customers_clean)
    products_clean = clean_products(products)
    orders_clean = clean_orders(orders)
    orphans = check_referential_integrity(order_items, orders_clean)
    order_items_clean = clean_order_items(order_items, orphans)

    customers_clean.to_csv(os.path.join(CLEAN_DIR, "customers_clean.csv"), index=False)
    products_clean.to_csv(os.path.join(CLEAN_DIR, "products_clean.csv"), index=False)
    orders_clean.to_csv(os.path.join(CLEAN_DIR, "orders_clean.csv"), index=False)
    order_items_clean.to_csv(os.path.join(CLEAN_DIR, "order_items_clean.csv"), index=False)

    print(f"Cleaned rows -> customers {len(customers_clean)}, products {len(products_clean)}, "
          f"orders {len(orders_clean)}, order_items {len(order_items_clean)} (dropped {len(orphans)} orphans)")

    report_path = os.path.join(OUTPUT_DIR, "data_quality_report.txt")
    with open(report_path, "w") as f:
        f.write(f"DATA QUALITY REPORT\nGenerated: {datetime.now()}\n{'='*60}\n\n")
        for section, msgs in issues.items():
            f.write(f"[{section.upper()}]\n")
            for m in msgs:
                f.write(f"  - {m}\n")
            f.write("\n")
        f.write(f"[EMAIL VALIDATION]\n  - invalid customer emails: {invalid_emails}\n")
    print("Report written to", report_path)

    for section, msgs in issues.items():
        print(f"[{section}]")
        for m in msgs:
            print(" -", m)


if __name__ == "__main__":
    main()
