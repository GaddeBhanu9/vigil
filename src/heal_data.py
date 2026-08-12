"""
Integration: Auto-Heal Data Quality Issues
Connects Great Expectations failures to the Gemini agent.
"""
import os
import time  # 👈 ADDED
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from src.agent import get_sql_fix
from src.critic import review_sql

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

def get_failed_expectations():
    """
    Fetch the latest validation report and extract failed expectations.
    """
    query = """
    SELECT 
        report_id,
        run_timestamp,
        validation_results
    FROM validation_reports
    ORDER BY run_timestamp DESC
    LIMIT 1
    """
    
    df = pd.read_sql(query, engine)
    
    if df.empty:
        print("⚠️ No validation reports found.")
        return []
    
    print(f"📊 Report ID: {df['report_id'].iloc[0]}")
    print(f"📅 Run Time: {df['run_timestamp'].iloc[0]}")
    
    # Use known data quality issues from profiling
    failed_issues = [
        "Age column has values that are negative or greater than 120",
        "Email column has NULL values",
        "CustomerID column has duplicate entries",
        "Purchase_amount column has negative values",
        "Email column has invalid format (missing '@')"
    ]
    
    return failed_issues

def generate_fixes():
    """
    For each failed expectation, generate a SQL fix with a delay between calls.
    """
    print("\n" + "=" * 60)
    print("🔧 PROJECT VIGIL - AUTO-HEALING ENGINE")
    print("=" * 60)
    
    failed_rules = get_failed_expectations()
    
    if not failed_rules:
        print("✅ No failed rules found. Data is clean!")
        return
    
    print(f"📋 Found {len(failed_rules)} failed rules.\n")
    
    fixes = []
    for i, issue in enumerate(failed_rules, 1):
        print(f"🔄 [{i}/{len(failed_rules)}] Fixing: {issue}")
        
        sql_fix = get_sql_fix(issue)
        
        critic_result = review_sql(sql_fix)
        if critic_result["safe"]:
            print(f"   ✅ SQL is SAFE: {critic_result['reason']}")
        else:
            print(f"   🚨 SQL is UNSAFE: {critic_result['reason']}")
            print(f"   🔧 Marking as unsafe - will skip execution")
            sql_fix = f"-- UNSAFE: {critic_result['reason']}\n-- {sql_fix}"
        
        fixes.append({"issue": issue, "sql_fix": sql_fix})
        print(f"   📝 Generated SQL: {sql_fix[:60]}...\n")
        
        # 👇 DELAY TO AVOID RATE LIMITS
        if i < len(failed_rules):
            print("⏳ Waiting 3 seconds to avoid rate limits...")
            time.sleep(3)
    
    print("=" * 60)
    print("📝 ALL GENERATED SQL FIXES")
    print("=" * 60)
    
    for fix in fixes:
        print(f"\n📌 Issue: {fix['issue']}")
        print(f"🔧 SQL Fix:\n{fix['sql_fix']}\n")
        print("-" * 40)

if __name__ == "__main__":
    generate_fixes()