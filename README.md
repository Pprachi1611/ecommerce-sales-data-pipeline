# E-Commerce Sales Data Pipeline

A Python-based ETL pipeline that generates, validates, transforms, and loads e-commerce sales data into PostgreSQL for analytical querying.

## Project Overview

This project demonstrates an end-to-end data engineering workflow using a simulated e-commerce dataset.

The pipeline extracts raw CSV data, performs data quality checks, transforms the data, and loads the processed records into a PostgreSQL database. SQL queries are then used to analyze sales, customers, products, orders, and payments.

## Architecture

```text
       Sample Data Generation
                 |
                 v
          Raw CSV Files
                 |
                 v
       Data Quality Inspection
                 |
                 v
        Data Transformation
                 |
                 v
       Processed CSV Files
                 |
                 v
        PostgreSQL Database
                 |
                 v
         SQL Analytics
```

## Technology Stack

- **Python** – ETL pipeline development
- **Pandas** – Data cleaning and transformation
- **PostgreSQL** – Relational database
- **SQLAlchemy** – Python-to-database connectivity
- **psycopg2** – PostgreSQL driver
- **python-dotenv** – Environment variable management
- **Git and GitHub** – Version control

## Dataset

The project generates synthetic e-commerce data consisting of five CSV files:

| Dataset | Records |
|---|---:|
| Customers | 100 |
| Products | 30 |
| Orders | 250 |
| Order Items | 633 |
| Payments | 250 |

The data includes customer details, product information, orders, order items, and payment records.

## ETL Workflow

### 1. Extract

Generates sample e-commerce data and stores the raw CSV files in `data/raw/`.

### 2. Inspect

Checks for missing values, duplicate records, invalid values, and broken foreign key references.

### 3. Transform

Cleans and standardizes the datasets, removes invalid and duplicate records, converts data types, validates relationships, and calculates order-item line totals.

The transformed CSV files are saved in `data/processed/`.

### 4. Load

Loads the processed datasets into PostgreSQL in the correct dependency order.

The loader checks whether the target tables already contain records. If they do, it safely skips loading instead of deleting or overwriting existing data.

### 5. Orchestrate

The master ETL script executes the individual stages and reports their execution status.

### 6. Logging

Centralized logging records pipeline activity, stage completion, warnings, and errors in `logs/etl_pipeline.log`.

## Database Schema

The PostgreSQL database contains five related tables:

- `customers`
- `products`
- `orders`
- `order_items`
- `payments`

Primary keys and foreign key constraints maintain relationships between the datasets. Additional constraints validate important fields such as quantities, prices, and payment statuses.

## SQL Analytics

The project includes analytical queries to explore:

- Total order-item sales value
- Monthly sales trends
- Top-selling products
- Highest-value customers
- Order and payment status distributions
- Payment methods
- Average order value
- Sales by product category
- Sales by customer city
- Successful payment collections
- Monthly successful collections
- Returns and refunds

## Project Structure

```text
ecommerce-sales-etl/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│
├── logs/
│
├── sql/
│   └── schema.sql
│
├── src/
│   ├── __init__.py
│   ├── db_config.py
│   ├── etl_pipeline.py
│   ├── generate_sample_data.py
│   ├── inspect_data.py
│   ├── load_data.py
│   ├── logger_config.py
│   └── transform_data.py
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup and Execution

### Prerequisites

- Python 3.10 or later
- PostgreSQL
- Git

### 1. Clone the repository

```bash
git clone https://github.com/Pprachi1611/ecommerce-sales-data-pipeline.git
cd ecommerce-sales-data-pipeline
```

### 2. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a reference.

Configure your PostgreSQL connection details:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ecommerce_db
POSTGRES_USER=ecommerce_user
POSTGRES_PASSWORD=your_password
```

Do not commit your `.env` file or expose database credentials.

### 5. Create the database schema

Create the `ecommerce_db` database in PostgreSQL and execute:

```text
sql/schema.sql
```

### 6. Run the ETL pipeline

```bash
python -u src/etl_pipeline.py
```

The pipeline generates data, validates it, transforms it, and attempts to load it into PostgreSQL.

**Note:** The loader uses safe-load behavior. If database tables already contain records, it skips the load to preserve existing data. For a fresh database, the initial load inserts the generated records.

## Logging

Pipeline execution logs are stored locally at:

```text
logs/etl_pipeline.log
```

The logs directory is excluded from Git.

## Current Project Scope

This project currently demonstrates a local ETL workflow using synthetic data, Python, Pandas, and PostgreSQL. It is designed as a learning and portfolio project and does not use a live e-commerce API or production customer data.

## Future Improvements

- Schedule pipeline execution using Apache Airflow.
- Add automated tests using Pytest.
- Introduce incremental data loading.
- Add data transformation models using dbt.
- Containerize the application using Docker.
- Deploy the pipeline and database to AWS.
- Build a sales analytics dashboard.

## Author

**Prachi Patil**

Computer Engineering | Aspiring Data Engineer

[GitHub Repository](https://github.com/Pprachi1611/ecommerce-sales-data-pipeline)