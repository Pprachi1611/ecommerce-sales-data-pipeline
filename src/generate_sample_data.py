
import csv
import random
from pathlib import Path
from datetime import date, timedelta

# Make generated data reproducible
random.seed(42)

# Project directory and output directory
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)


def write_csv(filename, records, columns):
    """Write records into a CSV file."""
    filepath = RAW_DIR / filename

    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(records)

    print(f"Created {filename}: {len(records)} records")


# ----------------------------------
# 1. Generate customers
# ----------------------------------

cities = [
    "Pune", "Mumbai", "Delhi", "Bangalore",
    "Hyderabad", "Chennai", "Nagpur", "Nashik"
]

customers = []

for i in range(1, 101):
    customers.append({
        "customer_id": f"C{i:03d}",
        "customer_name": f"Customer {i}",
        "email": f"customer{i}@example.com",
        "city": random.choice(cities),
        "signup_date": (
            date(2025, 1, 1)
            + timedelta(days=random.randint(0, 364))
        ).isoformat()
    })


# ----------------------------------
# 2. Generate products
# ----------------------------------

product_catalog = [
    ("Laptop", "Electronics", 55000),
    ("Smartphone", "Electronics", 25000),
    ("Headphones", "Electronics", 1800),
    ("Keyboard", "Accessories", 1200),
    ("Mouse", "Accessories", 650),
    ("Monitor", "Electronics", 12000),
    ("Backpack", "Fashion", 1500),
    ("T-Shirt", "Fashion", 600),
    ("Jeans", "Fashion", 1800),
    ("Shoes", "Fashion", 2500),
    ("Watch", "Accessories", 3200),
    ("Water Bottle", "Home", 450),
    ("Coffee Maker", "Home", 2800),
    ("Table Lamp", "Home", 950),
    ("Office Chair", "Furniture", 6500),
    ("Desk", "Furniture", 8000),
    ("Book", "Books", 350),
    ("Notebook", "Stationery", 120),
    ("Pen Set", "Stationery", 180),
    ("Printer", "Electronics", 8500),
    ("Tablet", "Electronics", 18000),
    ("Power Bank", "Electronics", 1400),
    ("USB Drive", "Accessories", 550),
    ("Bluetooth Speaker", "Electronics", 2200),
    ("Sunglasses", "Fashion", 1100),
    ("Wallet", "Fashion", 750),
    ("Bedsheet", "Home", 1300),
    ("Mixer Grinder", "Home", 3500),
    ("Running Shoes", "Fashion", 3000),
    ("Webcam", "Electronics", 1900)
]

products = []

for i, (name, category, price) in enumerate(product_catalog, 1):
    products.append({
        "product_id": f"P{i:03d}",
        "product_name": name,
        "category": category,
        "unit_price": price
    })


# ----------------------------------
# 3. Generate orders and order items
# ----------------------------------

order_statuses = [
    "Delivered", "Shipped", "Processing",
    "Cancelled", "Returned"
]

orders = []
order_items = []
payments = []

for i in range(1, 251):

    order_id = f"O{i:04d}"
    customer = random.choice(customers)

    order_date = (
        date(2026, 1, 1)
        + timedelta(days=random.randint(0, 287))
    )

    order_status = random.choices(
        order_statuses,
        weights=[50, 20, 15, 10, 5]
    )[0]

    orders.append({
        "order_id": order_id,
        "customer_id": customer["customer_id"],
        "order_date": order_date.isoformat(),
        "order_status": order_status
    })

    # Select 1 to 4 different products
    selected_products = random.sample(
        products,
        random.randint(1, 4)
    )

    order_total = 0

    for product in selected_products:

        quantity = random.randint(1, 3)
        price = product["unit_price"]

        item_total = quantity * price
        order_total += item_total

        order_items.append({
            "item_id": f"I{len(order_items) + 1:04d}",
            "order_id": order_id,
            "product_id": product["product_id"],
            "quantity": quantity,
            "unit_price": price
        })

    # ----------------------------------
    # 4. Generate payment
    # ----------------------------------

    if order_status == "Returned":
        payment_status = "Refunded"
    elif order_status == "Cancelled":
        payment_status = "Failed"
    elif order_status == "Processing":
        payment_status = "Pending"
    else:
        payment_status = "Paid"

    payment_date = order_date + timedelta(
        days=random.randint(0, 2)
    )

    payments.append({
        "payment_id": f"PAY{i:04d}",
        "order_id": order_id,
        "payment_date": payment_date.isoformat(),
        "payment_method": random.choice([
            "UPI", "Credit Card", "Debit Card", "Net Banking"
        ]),
        "amount": round(order_total, 2),
        "payment_status": payment_status
    })


# ----------------------------------
# 5. Save all CSV files
# ----------------------------------

write_csv(
    "customers.csv",
    customers,
    ["customer_id", "customer_name", "email", "city", "signup_date"]
)

write_csv(
    "products.csv",
    products,
    ["product_id", "product_name", "category", "unit_price"]
)

write_csv(
    "orders.csv",
    orders,
    ["order_id", "customer_id", "order_date", "order_status"]
)

write_csv(
    "order_items.csv",
    order_items,
    ["item_id", "order_id", "product_id", "quantity", "unit_price"]
)

write_csv(
    "payments.csv",
    payments,
    ["payment_id", "order_id", "payment_date",
     "payment_method", "amount", "payment_status"]
)

print("\nAll e-commerce CSV files generated successfully!")
