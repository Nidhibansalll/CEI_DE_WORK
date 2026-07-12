# Part 5 - Edge Case Handling
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from clean_data import clean_orders, clean_order_items, check_referential_integrity

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

def test_orphan_order_id():
    # Q1 - order_items with an order_id that doesn't exist in orders
    orders = pd.read_csv(os.path.join(RAW_DIR, "orders.csv"))
    items = pd.read_csv(os.path.join(RAW_DIR, "order_items.csv"))

    orphans = check_referential_integrity(items, orders)
    assert len(orphans) > 0, "no orphan rows found, generator should have made some"

    cleaned = clean_order_items(items, orphans)
    assert not cleaned["order_id"].isin(orphans["order_id"]).any()

    print(f"[PASS] orphan order_id -> found {len(orphans)} rows, dropped them since "
          f"they can't be tied to a real order (would break revenue joins otherwise)")


def test_discount_over_100():
    # Q2 - discount_percent going above 100
    items = pd.read_csv(os.path.join(RAW_DIR, "order_items.csv"))
    bad = items[items["discount_percent"] > 100]
    assert len(bad) > 0

    empty = pd.DataFrame(columns=items.columns)
    cleaned = clean_order_items(items, empty)
    max_disc = cleaned["discount_percent"].max()
    assert max_disc <= 100

    print(f"[PASS] discount > 100 -> found {len(bad)} rows, capped at 100 instead of "
          f"deleting (rest of the row - qty, price - is still fine)")


def test_zero_quantity():
    # Q3 - quantity = 0
    items = pd.read_csv(os.path.join(RAW_DIR, "order_items.csv"))
    zero_before = items[items["quantity"] == 0]

    empty = pd.DataFrame(columns=items.columns)
    cleaned = clean_order_items(items, empty)
    zero_after = cleaned[cleaned["quantity"] == 0]

    assert len(zero_before) > 0
    assert len(zero_after) > 0

    print(f"[PASS] quantity = 0 -> found {len(zero_before)} rows, kept them (0 qty means "
          f"0 revenue anyway, but deleting could hide a real data entry bug)")


def test_future_order_date():
    # Q4 - order_date in the future
    orders = pd.read_csv(os.path.join(RAW_DIR, "orders.csv"))
    cleaned = clean_orders(orders)

    future = cleaned[cleaned["order_date"] > pd.Timestamp.now()]
    assert len(future) > 0

    print(f"[PASS] future order_date -> found {len(future)} orders "
          f"(ids: {list(future['order_id'])}), kept + flagged since it could be a "
          f"real scheduled order, not necessarily bad data")


if __name__ == "__main__":
    print("Running edge case tests...\n" + "-" * 55)
    test_orphan_order_id()
    test_discount_over_100()
    test_zero_quantity()
    test_future_order_date()
    print("-" * 55)
    print("all tests passed")
