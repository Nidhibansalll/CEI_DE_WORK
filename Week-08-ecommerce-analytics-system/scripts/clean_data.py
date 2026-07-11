import re
import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
CLEAN_DIR = BASE_DIR / "data" / "cleaned"
REPORT_DIR = BASE_DIR / "output" / "sample_reports"

CLEAN_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def fix_date(value):
    # our raw data has dates in 2 formats:
    #   good:  2026-07-10  (YYYY-MM-DD)
    #   bad:   10-07-2026  (DD-MM-YYYY)
    value = str(value).strip()
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        pass
    try:
        return datetime.strptime(value, "%d-%m-%Y")
    except ValueError:
        pass
    return None


def clean_orders():
    """
    1. clean_orders()
    - fixes dates that are in DD-MM-YYYY format back to YYYY-MM-DD
    - handles NULL customer_id 
    """
    df = pd.read_csv(RAW_DIR / "orders.csv")

    total_rows = len(df)

    # customer_id is blank/NaN for some rows(messy data)
    null_customer_mask = df["customer_id"].isna()
    null_customer_count = int(null_customer_mask.sum())

    # fix dates
    fixed_dates = []
    bad_format_count = 0
    for val in df["date"]:
        parsed = fix_date(val)
        if parsed is None:
            fixed_dates.append(None)
            continue
        # if the original string wasn't already YYYY-MM-DD, count it as "fixed"
        if str(val).strip() != parsed.strftime("%Y-%m-%d"):
            bad_format_count += 1
        fixed_dates.append(parsed.strftime("%Y-%m-%d"))

    df["date"] = fixed_dates

    df.to_csv(CLEAN_DIR / "orders_clean.csv", index=False)

    stats = {
        "total_rows": total_rows,
        "null_customer_id_rows": null_customer_count,
        "bad_date_format_fixed": bad_format_count,
    }
    return df, stats


def clean_products():
    """
    2. clean_products()
    - trims extra spaces off product names
    - converts everything to Title Case
    """
    df = pd.read_csv(RAW_DIR / "products.csv")
    total_rows = len(df)

    before = df["name"].copy()

    # - extra leading/trailing spaces
    # - ALL CAPS or all lowercase 
    had_whitespace_issue = before != before.str.strip()
    had_case_issue = (before.str.strip() == before.str.strip().str.upper()) | \
                      (before.str.strip() == before.str.strip().str.lower())
    names_fixed = int((had_whitespace_issue | had_case_issue).sum())

    df["name"] = df["name"].str.strip().str.title()

    df.to_csv(CLEAN_DIR / "products_clean.csv", index=False)

    stats = {
        "total_rows": total_rows,
        "names_fixed": names_fixed,
    }
    return df, stats


def validate_emails():
    """
    3. validate_emails()
    - checks every customer email against a simple regex
    - returns the list of customer_ids that have a bad email
    - also saves customers_clean.csv 
    """
    df = pd.read_csv(RAW_DIR / "customers.csv")

    invalid_mask = ~df["email"].astype(str).apply(lambda e: bool(EMAIL_REGEX.match(e.strip())))
    bad_customer_ids = df.loc[invalid_mask, "customer_id"].tolist()

    df["email_valid"] = ~invalid_mask
    df.to_csv(CLEAN_DIR / "customers_clean.csv", index=False)

    stats = {
        "total_rows": len(df),
        "invalid_emails": len(bad_customer_ids),
    }
    return bad_customer_ids, stats


def check_referential_integrity():
    """
    4. check_referential_integrity()
    - finds order_items rows where the order_id doesn't actually exist in orders.csv 
    - also flags negative quantities while we're in here, since that's a data quality issue too
    """
    orders = pd.read_csv(RAW_DIR / "orders.csv")
    items = pd.read_csv(RAW_DIR / "order_items.csv")

    valid_order_ids = set(orders["order_id"])
    orphan_mask = ~items["order_id"].isin(valid_order_ids)
    orphan_rows = items.loc[orphan_mask]

    negative_qty_rows = items[items["quantity"] < 0]

    # keeping only the rows with a real order_id 
    clean_items = items.loc[~orphan_mask].copy()
    clean_items.to_csv(CLEAN_DIR / "order_items_clean.csv", index=False)

    stats = {
        "total_rows": len(items),
        "orphaned_order_id_rows": int(orphan_mask.sum()),
        "negative_quantity_rows": int((items["quantity"] < 0).sum()),
    }
    return orphan_rows, stats


def write_report(all_stats):
    lines = ["# Data Quality Report", "", f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ""]
    for section, stats in all_stats.items():
        lines.append(f"## {section}")
        for key, value in stats.items():
            lines.append(f"- {key}: {value}")
        lines.append("")

    report_path = REPORT_DIR / "data_quality_report.md"
    report_path.write_text("\n".join(lines))
    return report_path


def main():
    print("cleaning orders...")
    _, orders_stats = clean_orders()
    print(orders_stats)

    print("cleaning products...")
    _, products_stats = clean_products()
    print(products_stats)

    print("checking emails...")
    bad_ids, email_stats = validate_emails()
    print(email_stats)

    print("checking referential integrity...")
    _, integrity_stats = check_referential_integrity()
    print(integrity_stats)

    report_path = write_report({
        "Orders": orders_stats,
        "Products": products_stats,
        "Customer Emails": email_stats,
        "Order Items": integrity_stats,
    })

    print()
    print("cleaned files saved to:", CLEAN_DIR)
    print("report saved to:", report_path)


if __name__ == "__main__":
    main()
