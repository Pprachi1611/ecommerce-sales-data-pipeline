
import pandas as pd
from pathlib import Path

# ----------------------------------
# 1. Define project directories
# ----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# ----------------------------------
# 2. Load raw CSV files
# ----------------------------------

customers = pd.read_csv(RAW_DIR / "customers.csv")
products = pd.read_csv(RAW_DIR / "products.csv")
orders = pd.read_csv(RAW_DIR / "orders.csv")
order_items = pd.read_csv(RAW_DIR / "order_items.csv")
payments = pd.read_csv(RAW_DIR / "payments.csv")

print("Raw datasets loaded successfully!")


# ----------------------------------
# 3. Standardize text columns
# ----------------------------------

def clean_text(df):
    """Remove unwanted spaces from text columns."""

    for column in df.select_dtypes(include=["object", "str"]).columns:
        df[column] = df[column].str.strip()

    return df


datasets = [
    customers, products, orders, order_items, payments
]

for df in datasets:
    clean_text(df)


# ----------------------------------
# 4. Remove duplicate records
# ----------------------------------

customers = customers.drop_duplicates(
    subset=["customer_id"]
)

products = products.drop_duplicates(
    subset=["product_id"]
)

orders = orders.drop_duplicates(
    subset=["order_id"]
)

order_items = order_items.drop_duplicates(
    subset=["item_id"]
)

payments = payments.drop_duplicates(
    subset=["payment_id"]
)


# ----------------------------------
# 5. Convert date columns
# ----------------------------------

customers["signup_date"] = pd.to_datetime(
    customers["signup_date"], errors="coerce"
)

orders["order_date"] = pd.to_datetime(
    orders["order_date"], errors="coerce"
)

payments["payment_date"] = pd.to_datetime(
    payments["payment_date"], errors="coerce"
)


# ----------------------------------
# 6. Convert numeric columns
# ----------------------------------

products["unit_price"] = pd.to_numeric(
    products["unit_price"], errors="coerce"
)

order_items["quantity"] = pd.to_numeric(
    order_items["quantity"], errors="coerce"
)

order_items["unit_price"] = pd.to_numeric(
    order_items["unit_price"], errors="coerce"
)

payments["amount"] = pd.to_numeric(
    payments["amount"], errors="coerce"
)


# ----------------------------------
# 7. Remove invalid records
# ----------------------------------

# Remove records with missing required values
customers = customers.dropna(
    subset=["customer_id", "customer_name", "city", "signup_date"]
)

products = products.dropna(
    subset=["product_id", "product_name", "category", "unit_price"]
)

orders = orders.dropna(
    subset=["order_id", "customer_id", "order_date", "order_status"]
)

order_items = order_items.dropna(
    subset=["item_id", "order_id", "product_id", "quantity", "unit_price"]
)

payments = payments.dropna(
    subset=[
        "payment_id", "order_id", "payment_date",
        "payment_method", "amount", "payment_status"
    ]
)

# Remove invalid numeric values
products = products[products["unit_price"] > 0]

order_items = order_items[
    (order_items["quantity"] > 0) &
    (order_items["unit_price"] > 0)
]

payments = payments[payments["amount"] > 0]


# ----------------------------------
# 8. Validate foreign key relationships
# ----------------------------------

orders = orders[
    orders["customer_id"].isin(customers["customer_id"])
]

order_items = order_items[
    order_items["order_id"].isin(orders["order_id"])
]

order_items = order_items[
    order_items["product_id"].isin(products["product_id"])
]

payments = payments[
    payments["order_id"].isin(orders["order_id"])
]

# Keep only one payment per order
payments = payments.drop_duplicates(
    subset=["order_id"]
)


# ----------------------------------
# 9. Calculate order item total
# ----------------------------------

order_items["line_total"] = (
    order_items["quantity"] * order_items["unit_price"]
)


# ----------------------------------
# 10. Save processed datasets
# ----------------------------------

processed_datasets = {
    "customers": customers,
    "products": products,
    "orders": orders,
    "order_items": order_items,
    "payments": payments
}

print("\n========== TRANSFORMATION SUMMARY ==========\n")

for name, df in processed_datasets.items():

    output_file = PROCESSED_DIR / f"{name}.csv"

    df.to_csv(output_file, index=False)

    print(f"{name}.csv")
    print(f"Records: {len(df)}")
    print(f"Saved to: {output_file}")
    print("-" * 40)


print("\nAll datasets transformed successfully!")
