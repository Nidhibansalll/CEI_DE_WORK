"""
A command-line tool that:
1. Asks for report type (daily/weekly/monthly)
2. Asks for a date range (or lets daily/weekly/monthly pick a sensible
   default range automatically if the user just presses Enter)
3. Connects to ecommerce.db
4. Prints total orders, revenue, unique customers, top 3 products, and
   a % change comparison against the immediately preceding period of
   the same length
"""

import sqlite3
import argparse
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "ecommerce.db")


def get_period_from_type(report_type: str):
    """
    If the user picks daily/weekly/monthly but doesn't give explicit
    dates, I build a default range ending on the most recent order date
    in the database.
    """
    conn = sqlite3.connect(DB_PATH)
    max_date = conn.execute("SELECT MAX(order_date) FROM orders").fetchone()[0]
    conn.close()
    end = datetime.strptime(max_date.split(" ")[0], "%Y-%m-%d")

    if report_type == "daily":
        start = end
    elif report_type == "weekly":
        start = end - timedelta(days=6)
    else:  # monthly
        start = end - timedelta(days=29)

    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


def previous_period(start_str: str, end_str: str):
    """Given a date range, returns the immediately preceding range of the
    same length, used for the % change comparison."""
    start = datetime.strptime(start_str, "%Y-%m-%d")
    end = datetime.strptime(end_str, "%Y-%m-%d")
    length = (end - start).days + 1
    prev_end = start - timedelta(days=1)
    prev_start = prev_end - timedelta(days=length - 1)
    return prev_start.strftime("%Y-%m-%d"), prev_end.strftime("%Y-%m-%d")


def pct_change(current, previous):
    if previous in (0, None):
        return None
    return round(100.0 * (current - previous) / previous, 2)


def summarise_period(conn, start_date, end_date):
    """Runs all the aggregate queries needed for one period and returns a dict."""
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(DISTINCT o.order_id),
               COALESCE(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)), 0),
               COUNT(DISTINCT o.customer_id)
        FROM orders o
        LEFT JOIN order_items oi ON oi.order_id = o.order_id AND oi.quantity > 0
        WHERE DATE(o.order_date) BETWEEN ? AND ?
    """, (start_date, end_date))
    total_orders, total_revenue, unique_customers = cur.fetchone()

    cur.execute("""
        SELECT p.product_name, SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)) AS rev
        FROM order_items oi
        JOIN orders o ON o.order_id = oi.order_id
        JOIN products p ON p.product_id = oi.product_id
        WHERE DATE(o.order_date) BETWEEN ? AND ? AND oi.quantity > 0
        GROUP BY p.product_name
        ORDER BY rev DESC
        LIMIT 3
    """, (start_date, end_date))
    top_products = cur.fetchall()

    return {
        "total_orders": total_orders,
        "total_revenue": round(total_revenue or 0, 2),
        "unique_customers": unique_customers,
        "top_products": top_products,
    }


def print_report(report_type, start_date, end_date):
    conn = sqlite3.connect(DB_PATH)

    current = summarise_period(conn, start_date, end_date)
    prev_start, prev_end = previous_period(start_date, end_date)
    previous = summarise_period(conn, prev_start, prev_end)

    conn.close()

    lines = []
    lines.append("=" * 60)
    lines.append(f"{report_type.upper()} REPORT: {start_date} to {end_date}")
    lines.append("=" * 60)
    lines.append(f"Total Orders     : {current['total_orders']}")
    lines.append(f"Total Revenue    : Rs. {current['total_revenue']:,.2f}")
    lines.append(f"Unique Customers : {current['unique_customers']}")
    lines.append("")
    lines.append("Top 3 Products:")
    if current["top_products"]:
        for i, (name, rev) in enumerate(current["top_products"], start=1):
            lines.append(f"  {i}. {name} - Rs. {rev:,.2f}")
    else:
        lines.append("  (no product sales in this period)")
    lines.append("")
    lines.append(f"Comparison with previous period ({prev_start} to {prev_end}):")
    orders_change = pct_change(current["total_orders"], previous["total_orders"])
    revenue_change = pct_change(current["total_revenue"], previous["total_revenue"])
    lines.append(f"  Orders change  : {orders_change if orders_change is not None else 'N/A'}%")
    lines.append(f"  Revenue change : {revenue_change if revenue_change is not None else 'N/A'}%")
    lines.append("=" * 60)

    report_text = "\n".join(lines)
    print(report_text)
    return report_text


def main():
    parser = argparse.ArgumentParser(description="E-Commerce order summary report tool")
    parser.add_argument("--type", choices=["daily", "weekly", "monthly"], help="Report type")
    parser.add_argument("--start", help="Start date YYYY-MM-DD")
    parser.add_argument("--end", help="End date YYYY-MM-DD")
    parser.add_argument("--save", help="Optional path to save the report as a text file")
    args = parser.parse_args()

    report_type = args.type
    if not report_type:
        report_type = input("Enter report type (daily/weekly/monthly): ").strip().lower()
        while report_type not in ("daily", "weekly", "monthly"):
            report_type = input("Please type daily, weekly or monthly: ").strip().lower()

    start_date, end_date = args.start, args.end
    if not start_date or not end_date:
        default_start, default_end = get_period_from_type(report_type)
        user_start = input(f"Start date [default {default_start}]: ").strip()
        user_end = input(f"End date [default {default_end}]: ").strip()
        start_date = user_start or default_start
        end_date = user_end or default_end

    report_text = print_report(report_type, start_date, end_date)

    if args.save:
        os.makedirs(os.path.dirname(args.save), exist_ok=True)
        with open(args.save, "w") as f:
            f.write(report_text)
        print(f"\n(saved to {args.save})")


if __name__ == "__main__":
    main()
