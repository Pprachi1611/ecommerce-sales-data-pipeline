
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"


def test_processed_files_exist():
    """Check that all five processed CSV files exist."""
    expected_files = [
        "customers.csv",
        "products.csv",
        "orders.csv",
        "order_items.csv",
        "payments.csv",
    ]

    for filename in expected_files:
        assert (DATA_DIR / filename).exists(), f"{filename} is missing"


def test_no_duplicate_primary_keys():
    """Check primary keys for duplicate records."""
    primary_keys = {
        "customers.csv": "customer_id",
        "products.csv": "product_id",
        "orders.csv": "order_id",
        "order_items.csv": "item_id",
        "payments.csv": "payment_id",
    }

    for filename, key in primary_keys.items():
        df = pd.read_csv(DATA_DIR / filename)

        assert key in df.columns, f"{key} column missing in {filename}"

        assert not df[key].duplicated().any(), (
            f"Duplicate values found in {filename}: {key}"
        )


def test_no_missing_required_values():
    """Check that required columns contain no missing values."""
    required_columns = {
        "customers.csv": ["customer_id", "email"],
        "products.csv": ["product_id", "product_name", "unit_price"],
        "orders.csv": ["order_id", "customer_id", "order_date"],
        "order_items.csv": [
            "item_id",
            "order_id",
            "product_id",
            "quantity",
            "unit_price",
            "line_total",
        ],
        "payments.csv": [
            "payment_id",
            "order_id",
            "amount",
            "payment_status",
        ],
    }

    for filename, columns in required_columns.items():
        df = pd.read_csv(DATA_DIR / filename)

        assert all(column in df.columns for column in columns), (
            f"Required columns missing in {filename}"
        )

        assert not df[columns].isnull().any().any(), (
            f"Missing required values found in {filename}"
        )


def test_positive_sales_values():
    """Check that quantities, prices, and totals are positive."""
    df = pd.read_csv(DATA_DIR / "order_items.csv")

    assert (df["quantity"] > 0).all()
    assert (df["unit_price"] > 0).all()
    assert (df["line_total"] > 0).all()


def test_line_total_calculation():
    """Verify quantity multiplied by unit price."""
    df = pd.read_csv(DATA_DIR / "order_items.csv")

    expected_total = df["quantity"] * df["unit_price"]

    assert (
        (df["line_total"] - expected_total).abs() < 0.000001
    ).all()

def test_foreign_key_integrity():
    """Check that all foreign keys reference existing records."""

    customers = pd.read_csv(DATA_DIR / "customers.csv")
    products = pd.read_csv(DATA_DIR / "products.csv")
    orders = pd.read_csv(DATA_DIR / "orders.csv")
    order_items = pd.read_csv(DATA_DIR / "order_items.csv")
    payments = pd.read_csv(DATA_DIR / "payments.csv")

    # Orders must reference existing customers
    assert orders["customer_id"].isin(
        customers["customer_id"]
    ).all()

    # Order items must reference existing orders and products
    assert order_items["order_id"].isin(
        orders["order_id"]
    ).all()

    assert order_items["product_id"].isin(
        products["product_id"]
    ).all()

    # Payments must reference existing orders
    assert payments["order_id"].isin(
        orders["order_id"]
    ).all()
