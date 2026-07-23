"""
dw_create_modification_case.py

Creates a star schema data warehouse using DuckDB.

This customized version creates:

Dimension tables:
    - dim_customers
    - dim_products
    - dim_stores
    - dim_campaigns

Fact table:
    - fact_sales

Development:
    - Drops and recreates warehouse tables.
    - Intended for development and testing.
    - ETL processes should populate the tables later.

Output:
    artifacts/smart_sales.duckdb


Run command:

uv run python -m bizintel.dw_create_modification.case
"""


# ==========================================================
# === Section 1. Import Dependencies and Constants ==========
# ==========================================================

from pathlib import Path
from typing import Final

from datafun_toolkit.logger import log_path
import duckdb

from bizintel.utils_logger import LOG, log_header

# ==========================================================
# === Declare Constants ====================================
# ==========================================================


# DuckDB stores the entire warehouse in one file.
DW_FILE: Final[Path] = Path("artifacts/smart_sales.duckdb")


# ==========================================================
# === Section 2.1 Create Customer Dimension ================
# ==========================================================


# Dimension tables store descriptive information.
#
# Customer dimension describes WHO made purchases.


def create_dim_customers(conn: duckdb.DuckDBPyConnection) -> None:
    """
    Create the customers dimension table.

    Args:
        conn:
            Open DuckDB connection.

    Returns:
        None
    """

    LOG.info("START create dim_customers")

    conn.execute(
        """
        DROP TABLE IF EXISTS dim_customers
        """
    )

    conn.execute(
        """
        CREATE TABLE dim_customers (

            CustomerID INTEGER PRIMARY KEY,

            Name VARCHAR,

            Region VARCHAR,

            JoinDate DATE

        )
        """
    )

    LOG.info("dim_customers created.")


# ==========================================================
# === Section 2.2 Create Product Dimension ================
# ==========================================================


# Product dimension describes WHAT was purchased.


def create_dim_products(conn: duckdb.DuckDBPyConnection) -> None:
    """
    Create the products dimension table.

    Args:
        conn:
            Open DuckDB connection.

    Returns:
        None
    """

    LOG.info("START create dim_products")

    conn.execute(
        """
        DROP TABLE IF EXISTS dim_products
        """
    )

    conn.execute(
        """
        CREATE TABLE dim_products (

            ProductID INTEGER PRIMARY KEY,

            ProductName VARCHAR,

            Category VARCHAR,

            UnitPrice DOUBLE

        )
        """
    )

    LOG.info("dim_products created.")


# ==========================================================
# === Section 2.3 Create Store Dimension ===================
# ==========================================================


# Store dimension describes WHERE the sale occurred.
#
# It allows analysis by:
#   - store
#   - city
#   - state


def create_dim_stores(conn: duckdb.DuckDBPyConnection) -> None:
    """
    Create the stores dimension table.

    Args:
        conn:
            Open DuckDB connection.

    Returns:
        None
    """

    LOG.info("START create dim_stores")

    LOG.info("Drop existing dim_stores table.")

    conn.execute(
        """
        DROP TABLE IF EXISTS dim_stores
        """
    )

    LOG.info("Create dim_stores table.")

    conn.execute(
        """
        CREATE TABLE dim_stores (

            StoreID INTEGER PRIMARY KEY,

            StoreName VARCHAR,

            City VARCHAR,

            State VARCHAR

        )
        """
    )

    LOG.info("dim_stores created.")


# ==========================================================
# === Section 2.4 Create Campaign Dimension ===============
# ==========================================================


# Campaign dimension describes WHY a sale happened.
#
# It stores marketing campaign information.


def create_dim_campaigns(conn: duckdb.DuckDBPyConnection) -> None:
    """
    Create the campaigns dimension table.

    Args:
        conn:
            Open DuckDB connection.

    Returns:
        None
    """

    LOG.info("START create dim_campaigns")

    LOG.info("Drop existing dim_campaigns table.")

    conn.execute(
        """
        DROP TABLE IF EXISTS dim_campaigns
        """
    )

    LOG.info("Create dim_campaigns table.")

    conn.execute(
        """
        CREATE TABLE dim_campaigns (

            CampaignID INTEGER PRIMARY KEY,

            CampaignName VARCHAR,

            CampaignType VARCHAR,

            StartDate DATE,

            EndDate DATE

        )
        """
    )

    LOG.info("dim_campaigns created.")


# ==========================================================
# === Section 3. Create Fact Sales Table ===================
# ==========================================================


# A fact table stores measurable business events.
#
# Each row represents one transaction.
#
# Foreign keys connect the sales facts to dimensions:
#
# CustomerID  -> dim_customers
# ProductID   -> dim_products
# StoreID     -> dim_stores
# CampaignID  -> dim_campaigns


def create_fact_sales(conn: duckdb.DuckDBPyConnection) -> None:
    """
    Create the sales fact table.

    Args:
        conn:
            Open DuckDB connection.

    Returns:
        None
    """

    LOG.info("START create fact_sales")

    LOG.info("Drop existing fact_sales table.")

    conn.execute(
        """
        DROP TABLE IF EXISTS fact_sales
        """
    )

    LOG.info("Create fact_sales table.")

    conn.execute(
        """
        CREATE TABLE fact_sales (

            TransactionID INTEGER PRIMARY KEY,

            SaleDate DATE,

            CustomerID INTEGER
                REFERENCES dim_customers(CustomerID),

            ProductID INTEGER
                REFERENCES dim_products(ProductID),

            StoreID INTEGER
                REFERENCES dim_stores(StoreID),

            CampaignID INTEGER
                REFERENCES dim_campaigns(CampaignID),

            SaleAmount DOUBLE

        )
        """
    )

    LOG.info("fact_sales created.")


# ==========================================================
# === Section 4. Delete Existing Tables ====================
# ==========================================================


def delete_tables(conn):

    LOG.info("START delete tables....")

    LOG.info("- Dropping fact_sales table if it exists")

    conn.execute("DROP TABLE IF EXISTS fact_sales")

    LOG.info("- Dropping dim_campaigns table if it exists")

    conn.execute("DROP TABLE IF EXISTS dim_campaigns")

    LOG.info("- Dropping dim_stores table if it exists")

    conn.execute("DROP TABLE IF EXISTS dim_stores")

    LOG.info("- Dropping dim_products table if it exists")

    conn.execute("DROP TABLE IF EXISTS dim_products")

    LOG.info("- Dropping dim_customers table if it exists")

    conn.execute("DROP TABLE IF EXISTS dim_customers")

    LOG.info("  All tables deleted.")


# ==========================================================
# === Section 5. Verify Warehouse Schema ===================
# ==========================================================


def verify_schema(conn: duckdb.DuckDBPyConnection) -> None:
    """
    Verify tables created in the warehouse.

    Args:
        conn:
            Open DuckDB connection.

    Returns:
        None
    """

    LOG.info("START verify schema")

    tables = conn.execute(
        """
        SHOW TABLES
        """
    ).fetchall()

    LOG.info(f"Tables in warehouse: {[table[0] for table in tables]}")


# ==========================================================
# === Section 5.1 Verify Row Counts ========================
# ==========================================================


def verify_row_counts(conn: duckdb.DuckDBPyConnection) -> None:
    """
    Verify row counts for all warehouse tables.

    WHY:
        Confirms that the CREATE DW workflow only creates
        empty tables and does not load data.

    Args:
        conn:
            Open DuckDB connection.

    Returns:
        None
    """

    LOG.info("START verify row counts....")

    tables = [
        "dim_customers",
        "dim_products",
        "dim_stores",
        "dim_campaigns",
        "fact_sales",
    ]

    for table in tables:
        LOG.info(f"Checking row count for {table}")

        count = conn.execute(
            f"""
            SELECT COUNT(*)
            FROM {table}
            """
        ).fetchone()[0]

        LOG.info(f"  {table}: {count} rows")


# ==========================================================
# === Section 6. Main Function =============================
# ==========================================================


def main() -> None:
    """
    Main function to create the data warehouse schema.
    """

    log_header(LOG, "BI")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    log_path(LOG, "Data warehouse:", DW_FILE)

    LOG.info("Create the artifacts/ folder if it does not exist")

    DW_FILE.parent.mkdir(parents=True, exist_ok=True)

    LOG.info("Connect to DuckDB - creates the file if it does not exist")

    LOG.info("Connecting to DuckDB data warehouse........")

    conn: duckdb.DuckDBPyConnection = duckdb.connect(str(DW_FILE))

    LOG.info("Created conn: a DuckDB connection object")

    LOG.info("CALL a function to delete tables in reverse order of creation")

    delete_tables(conn)

    LOG.info("CALL a function to create dim_customers........")

    LOG.info("PASS IN conn: the DuckDB connection object")

    create_dim_customers(conn)

    LOG.info("CALL a function to create dim_products........")

    LOG.info("PASS IN conn: the DuckDB connection object")

    create_dim_products(conn)

    LOG.info("CALL a function to create dim_stores........")

    LOG.info("PASS IN conn: the DuckDB connection object")

    create_dim_stores(conn)

    LOG.info("CALL a function to create dim_campaigns........")

    LOG.info("PASS IN conn: the DuckDB connection object")

    create_dim_campaigns(conn)

    LOG.info("CALL a function to create fact_sales........")

    LOG.info("PASS IN conn: the DuckDB connection object")

    create_fact_sales(conn)

    LOG.info("CALL a function to verify the schema........")

    LOG.info("PASS IN conn: the DuckDB connection object")

    verify_schema(conn)

    LOG.info("CALL a function to verify row counts........")

    LOG.info("PASS IN conn: the DuckDB connection object")

    verify_row_counts(conn)

    conn.close()

    LOG.info("Workflow 1-CREATE DW complete")

    LOG.info("========================")

    LOG.info("Executed successfully!")

    LOG.info("========================")


# ==========================================================
# === Section 7. Conditional Execution Guard ===============
# ==========================================================


if __name__ == "__main__":
    main()
