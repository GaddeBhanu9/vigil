"""
Load messy customer data into Neon PostgreSQL database.
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def load_csv_to_postgres():
    """
    Read the messy customer data CSV and load it into PostgreSQL.
    """
    # 1. Get database connection
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL not found in .env file")

    engine = create_engine(database_url)

    # 2. Read the CSV file
    csv_path = "data/messy_customer_data.csv"
    print(f"📂 Reading CSV from: {csv_path}")

    df = pd.read_csv(csv_path)
    print(f"📊 Loaded {len(df)} rows and {len(df.columns)} columns")
    print(f"📋 Columns: {list(df.columns)}")

    # 3. Preview the data (first 5 rows)
    print("\n🔍 Preview of the data:")
    print(df.head())

    # 4. Create the table in PostgreSQL (if it doesn't exist)
    table_name = "customers"

    # Drop the table if it exists (so we start fresh)
    with engine.connect() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE"))
        conn.commit()
        print(f"🗑️ Dropped existing table '{table_name}' (if it existed)")

    # 5. Load the DataFrame into PostgreSQL
    print(f"⏳ Loading data into PostgreSQL table '{table_name}'...")
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"✅ Successfully loaded {len(df)} rows into '{table_name}'")

    # 6. Verify the data was loaded
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        count = result.fetchone()[0]
        print(f"🔢 Verification: {count} rows in the table")

        # Show column names
        result = conn.execute(text(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position
        """))
        print("\n📋 Table schema:")
        for row in result:
            print(f"   - {row[0]}: {row[1]}")


if __name__ == "__main__":
    load_csv_to_postgres()