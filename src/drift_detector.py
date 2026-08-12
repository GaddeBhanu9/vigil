"""
Pillar 5: Statistical Drift Detection
Detects if the distribution of incoming data has changed significantly.
Uses KS-Test (Numeric) and Chi-Squared Test (Categorical).
"""
import os
import pandas as pd
import numpy as np
from scipy import stats
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

def load_and_split_data():
    """
    Loads customer data and splits it into Reference (old) and Current (new) batches.
    Uses 'Signup_Date' to determine the split point.
    """
    print("📂 Loading data from Neon...")
    df = pd.read_sql("SELECT * FROM customers", engine)
    
    # Convert Signup_Date to datetime (format: DD/MM/YYYY)
    df['Signup_Date'] = pd.to_datetime(df['Signup_Date'], format='%d/%m/%Y', errors='coerce')
    
    # Sort by date to simulate time-series data
    df = df.sort_values('Signup_Date')
    
    # Split into Reference (first 50%) and Current (last 50%)
    split_idx = len(df) // 2
    reference = df.iloc[:split_idx]
    current = df.iloc[split_idx:]
    
    print(f"📊 Reference batch: {len(reference)} rows (Older dates)")
    print(f"📊 Current batch: {len(current)} rows (Newer dates)")
    return reference, current

def run_drift_tests(ref, cur):
    """
    Runs KS-Test (Numeric) and Chi-Squared Test (Categorical) between two batches.
    Returns a dictionary with drift results.
    """
    report = {"drift_detected": False, "results": []}
    
    # 1. Numeric Columns -> Kolmogorov-Smirnov (KS) Test
    numeric_cols = ['Age', 'purchase_amount', 'feedback_score']
    print("\n" + "=" * 60)
    print("📊 NUMERIC DRIFT (KS-Test)")
    print("=" * 60)
    
    for col in numeric_cols:
        if col in ref.columns and col in cur.columns:
            # Drop nulls for the test
            ref_clean = ref[col].dropna()
            cur_clean = cur[col].dropna()
            
            if len(ref_clean) > 0 and len(cur_clean) > 0:
                stat, p_value = stats.ks_2samp(ref_clean, cur_clean)
                is_drift = p_value < 0.05  # If p < 0.05, distributions are significantly different
                report["results"].append({
                    "column": col, 
                    "test": "KS-Test", 
                    "p_value": p_value,
                    "drift": is_drift
                })
                status = "🚨 DRIFT" if is_drift else "✅ Stable"
                print(f"{col}: {status} (p-value: {p_value:.4f})")
    
    # 2. Categorical Columns -> Chi-Squared Test
    categorical_cols = ['Country', 'Gender']
    print("\n" + "=" * 60)
    print("📊 CATEGORICAL DRIFT (Chi-Squared)")
    print("=" * 60)
    
    for col in categorical_cols:
        if col in ref.columns and col in cur.columns:
            # Create contingency table
            ref_counts = ref[col].value_counts()
            cur_counts = cur[col].value_counts()
            
            # Align indices
            all_categories = sorted(set(ref_counts.index).union(cur_counts.index))
            ref_aligned = ref_counts.reindex(all_categories, fill_value=0)
            cur_aligned = cur_counts.reindex(all_categories, fill_value=0)
            
            if ref_aligned.sum() > 0 and cur_aligned.sum() > 0:
                stat, p_value, dof, expected = stats.chi2_contingency([ref_aligned, cur_aligned])
                is_drift = p_value < 0.05
                report["results"].append({
                    "column": col, 
                    "test": "Chi-Squared", 
                    "p_value": p_value,
                    "drift": is_drift
                })
                status = "🚨 DRIFT" if is_drift else "✅ Stable"
                print(f"{col}: {status} (p-value: {p_value:.4f})")
    
    # Check if ANY drift was detected
    if any(r["drift"] for r in report["results"]):
        report["drift_detected"] = True
    
    return report

def main():
    print("\n" + "=" * 60)
    print("🔬 PROJECT VIGIL - PILLAR 5: DRIFT DETECTION")
    print("=" * 60)
    
    # 1. Load and split data
    reference, current = load_and_split_data()
    
    # 2. Run statistical tests
    report = run_drift_tests(reference, current)
    
    # 3. Final Summary
    print("\n" + "=" * 60)
    print("📋 FINAL DRIFT REPORT")
    print("=" * 60)
    
    if report["drift_detected"]:
        print("🚨 DATA DRIFT DETECTED! The distribution of some features has changed.")
        print("📌 Action: Consider retraining your models or alerting the data team.")
    else:
        print("✅ No significant drift detected. Data distribution is stable.")
    
    print("\nDetailed Results:")
    for result in report["results"]:
        status = "🚨 Drift" if result["drift"] else "✅ Stable"
        print(f"   - {result['column']} ({result['test']}): {status} (p={result['p_value']:.4f})")

if __name__ == "__main__":
    main()