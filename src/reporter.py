"""
Data Trust Score reporting and history tracking for Project VIGIL.
Saves validation results to the database for historical tracking.
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from src.agent import get_sql_fix
from sqlalchemy import create_engine, text
from src.validator import run_validation

load_dotenv()


def save_validation_results(validation_result):
    """
    Save validation results to the database.
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL not found in .env file")

    engine = create_engine(database_url)

    # Extract statistics
    stats = validation_result["statistics"]
    total = stats["evaluated_expectations"]
    passed = stats["successful_expectations"]
    failed = stats["unsuccessful_expectations"]
    success_rate = stats["success_percent"]

    # Data Trust Score = Success Rate (rounded to 2 decimals)
    data_trust_score = round(success_rate, 2)

    # Convert validation results to JSON
    results_json = json.dumps(validation_result, default=str)

    # Insert into database
    with engine.connect() as conn:
        insert_query = text("""
            INSERT INTO validation_reports (
                run_timestamp,
                total_expectations,
                passed_expectations,
                failed_expectations,
                success_rate,
                data_trust_score,
                validation_results
            ) VALUES (
                :timestamp,
                :total,
                :passed,
                :failed,
                :success_rate,
                :data_trust_score,
                :results_json
            )
        """)

        conn.execute(
            insert_query,
            {
                "timestamp": datetime.utcnow(),
                "total": total,
                "passed": passed,
                "failed": failed,
                "success_rate": success_rate,
                "data_trust_score": data_trust_score,
                "results_json": results_json,
            }
        )
        conn.commit()

    print(f"\n Validation results saved to database!")
    print(f" Data Trust Score: {data_trust_score}%")


def get_latest_report():
    """
    Get the most recent Data Trust Score.
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL not found in .env file")

    engine = create_engine(database_url)

    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT 
                report_id,
                run_timestamp,
                total_expectations,
                passed_expectations,
                failed_expectations,
                data_trust_score
            FROM validation_reports
            ORDER BY run_timestamp DESC
            LIMIT 1
        """))

        row = result.fetchone()
        if row:
            print("\n LATEST DATA TRUST SCORE")
            print("=" * 60)
            print(f"Report ID: {row[0]}")
            print(f"Timestamp: {row[1]}")
            print(f"Total Expectations: {row[2]}")
            print(f"Passed: {row[3]}")
            print(f"Failed: {row[4]}")
            print(f"Data Trust Score: {row[5]}%")
            return row
        else:
            print("No validation reports found.")
            return None


def run_full_report():
    """
    Run validation, save results, and show the latest report.
    """
    print("\n" + "=" * 60)
    print(" PROJECT VIGIL - FULL REPORT")
    print("=" * 60)

    # 1. Run validation
    validation_result = run_validation()

    # 2. Save results to database
    save_validation_results(validation_result)

    # 3. Show latest report
    get_latest_report()

    print("\n" + "=" * 60)
    print(" Report Complete!")
    print("=" * 60)


if __name__ == "__main__":
    run_full_report()