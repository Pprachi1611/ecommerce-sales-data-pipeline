
from pathlib import Path
import sys
import pandas as pd
from sqlalchemy import text
from db_config import engine

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

TABLES = {
    "customers": ["signup_date"],
    "products": [],
    "orders": ["order_date"],
    "order_items": [],
    "payments": ["payment_date"]
}


class SafeSkip(Exception):
    """Raised when database records already exist."""


def main():
    try:
        print("Starting CSV to PostgreSQL loading...\n")

        dataframes = {}

        # Read all processed CSV files.
        for table_name, date_columns in TABLES.items():
            file_path = PROCESSED_DIR / f"{table_name}.csv"

            if not file_path.exists():
                raise FileNotFoundError(file_path)

            df = pd.read_csv(file_path)

            if df.empty:
                raise ValueError(f"{table_name}.csv is empty")

            for column in date_columns:
                df[column] = pd.to_datetime(
                    df[column], errors="raise"
                ).dt.date

            dataframes[table_name] = df
            print(f"Loaded {len(df)} records from {table_name}.csv")

        # Check tables and insert everything in one transaction.
        with engine.begin() as connection:

            for table_name in TABLES:
                count = connection.execute(
                    text(f"SELECT COUNT(*) FROM public.{table_name}")
                ).scalar_one()

                if count > 0:
                    raise SafeSkip(
                        f"Table '{table_name}' already contains records."
                    )

            for table_name, df in dataframes.items():
                df.to_sql(
                    name=table_name,
                    con=connection,
                    schema="public",
                    if_exists="append",
                    index=False,
                    method="multi",
                    chunksize=1000
                )

                print(f"Inserted {len(df)} records into {table_name}")

            print("\nDatabase row count verification:")

            for table_name, df in dataframes.items():
                db_count = connection.execute(
                    text(f"SELECT COUNT(*) FROM public.{table_name}")
                ).scalar_one()

                print(
                    f"{table_name}: CSV = {len(df)}, "
                    f"Database = {db_count}"
                )

                if db_count != len(df):
                    raise RuntimeError(
                        f"Row count mismatch in {table_name}"
                    )

        print("\nAll datasets loaded successfully!")
        return 0

    except SafeSkip as error:
        print("\nDATABASE LOADING SKIPPED SAFELY.")
        print(error)
        print("Existing database records were preserved.")
        return 2

    except Exception as error:
        print("\nDATA LOADING FAILED!")
        print(f"{type(error).__name__}: {error}")
        return 1

    finally:
        engine.dispose()


if __name__ == "__main__":
    sys.exit(main())
