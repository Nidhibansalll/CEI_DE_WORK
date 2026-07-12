"""
test_edge_cases.py
-------------------
Author: Nidhi
Project: E-Commerce Order Analytics System (Celebal Intern Mini Project)

Part 5 of the brief asked for test cases (as Python functions) that verify
what happens for 4 specific edge cases. I'm not using pytest here - I kept
it as plain functions with assert + print, run directly with
`python3 test_edge_cases.py`, so anyone reviewing this can run it without
installing another dependency, and can see WHY each case passed just by
reading the printed explanation.

Each test explains, in the print statement, what our system actually does
about that edge case (not just whether the code crashes).
"""

import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from clean_data import (
    clean_orders, clean_products, clean_order_items,
    check_referential_integrity,
)

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def test_orphan_order_id():
    """1. What happens when order_items has an order_id not in orders?"""
    orders = pd.read_csv(os.path.join(RAW_DIR, "orders.csv"))
    order_items = pd.read_csv(os.path.join(RAW_DIR, "order_items.csv"))

    orphans = check_referential_integrity(order_items, orders)

    assert len(orphans) > 0, "expected the generator's intentional orphan rows to be detected"
    cleaned = clean_order_items(order_items, orphans)
    assert not cleaned["order_id"].isin(orphans["order_id"]).any(), \
        "orphan rows should be excluded from the cleaned order_items"

    print(f"[PASS] test_orphan_order_id: found {len(orphans)} orphan rows "
          f"(order_id not present in orders.csv). Our system flags them in the "
          f"data quality report and EXCLUDES them from the cleaned data, "
          f"because an item with no parent order would break every revenue join.")


def test_discount_over_100():
    """2. What happens when discount_percent > 100?"""
    order_items = pd.read_csv(os.path.join(RAW_DIR, "order_items.csv"))
    bad_rows = order_items[order_items["discount_percent"] > 100]

    assert len(bad_rows) > 0, "expected the generator's intentional bad-discount rows to exist"
    empty_orphans = pd.DataFrame(columns=order_items.columns)
    cleaned = clean_order_items(order_items, empty_orphans)
    max_discount_after = cleaned["discount_percent"].max()

    assert max_discount_after <= 100, "discount_percent should be capped at 100 after cleaning"
    print(f"[PASS] test_discount_over_100: found {len(bad_rows)} rows with discount_percent > 100. "
          f"Our system flags them and CAPS them at 100 (rather than deleting the row, "
          f"since the rest of that line item - quantity, price - is still valid data), "
          f"max discount after cleaning = {max_discount_after}%.")


def test_zero_quantity():
    """3. What happens when quantity is 0?"""
    order_items = pd.read_csv(os.path.join(RAW_DIR, "order_items.csv"))
    zero_rows = order_items[order_items["quantity"] == 0]

    empty_orphans = pd.DataFrame(columns=order_items.columns)
    cleaned = clean_order_items(order_items, empty_orphans)
    zero_rows_after = cleaned[cleaned["quantity"] == 0]

    # dedupe can also remove a zero-qty row if it's an exact duplicate, so we
    # check "still present, not silently wiped out" rather than an exact count
    assert len(zero_rows) > 0, "expected the generator's intentional zero-quantity rows to exist"
    assert len(zero_rows_after) > 0, "zero-quantity rows should be kept (not all deleted just for being zero)"
    print(f"[PASS] test_zero_quantity: found {len(zero_rows)} rows with quantity = 0. "
          f"Our system KEEPS these rows (they don't affect revenue since quantity*price=0, "
          f"and dropping them would hide a possible upstream data-entry bug), but flags "
          f"them in the data quality report so a human can investigate.")


def test_future_order_date():
    """4. What happens when order_date is in the future?"""
    orders = pd.read_csv(os.path.join(RAW_DIR, "orders.csv"))
    cleaned = clean_orders(orders)

    future_orders = cleaned[cleaned["order_date"] > pd.Timestamp.now()]

    assert len(future_orders) > 0, "expected the generator's intentional future-dated orders to exist"
    print(f"[PASS] test_future_order_date: found {len(future_orders)} orders with a future "
          f"order_date (order_ids: {list(future_orders['order_id'])}). Our system does NOT "
          f"delete these - a future date could be a legitimate pre-order/scheduled order - "
          f"but it DOES flag them in the data quality report so the business can decide "
          f"whether that's expected or a bug in the source system.")


def test_negative_quantity_is_treated_as_return():
    """Bonus: negative quantity should be preserved (it means a return), not deleted or made positive."""
    order_items = pd.read_csv(os.path.join(RAW_DIR, "order_items.csv"))
    neg_rows = order_items[order_items["quantity"] < 0]
    empty_orphans = pd.DataFrame(columns=order_items.columns)
    cleaned = clean_order_items(order_items, empty_orphans)
    neg_rows_after = cleaned[cleaned["quantity"] < 0]

    assert len(neg_rows_after) == len(neg_rows), "negative quantity rows (returns) must be preserved as-is"
    print(f"[PASS] test_negative_quantity_is_treated_as_return: {len(neg_rows)} return rows "
          f"preserved with their original negative quantity (used later in Q5/Q6 return-rate analysis).")


def test_duplicate_order_items_are_removed():
    """Bonus: exact duplicate line items (same order+product+qty+price+discount) should be deduped."""
    order_items = pd.read_csv(os.path.join(RAW_DIR, "order_items.csv"))
    dedup_cols = ["order_id", "product_id", "quantity", "unit_price", "discount_percent"]
    n_dupes_before = order_items.duplicated(subset=dedup_cols, keep="first").sum()

    empty_orphans = pd.DataFrame(columns=order_items.columns)
    cleaned = clean_order_items(order_items, empty_orphans)
    n_dupes_after = cleaned.duplicated(subset=dedup_cols, keep="first").sum()

    assert n_dupes_before > 0, "expected the generator's intentional duplicate rows to exist"
    assert n_dupes_after == 0, "cleaned order_items should have no exact duplicates left"
    print(f"[PASS] test_duplicate_order_items_are_removed: found {n_dupes_before} exact duplicate rows "
          f"(same order_id+product_id+quantity+unit_price+discount_percent). Our system keeps the first "
          f"occurrence and drops the rest, since these look like double-submitted / re-run ETL rows, "
          f"not genuinely separate purchases.")


if __name__ == "__main__":
    print("Running edge case tests for E-Commerce Order Analytics System\n" + "-" * 60)
    test_orphan_order_id()
    test_discount_over_100()
    test_zero_quantity()
    test_future_order_date()
    test_negative_quantity_is_treated_as_return()
    test_duplicate_order_items_are_removed()
    print("-" * 60)
    print("All edge case tests passed.")
