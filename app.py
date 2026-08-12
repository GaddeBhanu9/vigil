"""
Project VIGIL - Main Dashboard
Consumes data from FastAPI backend.
"""
import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Project VIGIL", layout="wide")
st.title("🛡️ Project VIGIL")
st.caption("Autonomous AI Data Quality & Observability Platform")

API_URL = "http://localhost:8000"

# --- 1. Check API Connection ---
try:
    response = requests.get(f"{API_URL}/", timeout=3)
    if response.status_code == 200:
        st.success("✅ Connected to FastAPI Backend!")
    else:
        st.error(f"⚠️ API returned status {response.status_code}")
        st.stop()
except requests.exceptions.ConnectionError:
    st.error("🚨 Cannot connect to FastAPI. Please run: `poetry run uvicorn src.api:app --reload`")
    st.stop()
except Exception as e:
    st.error(f"❌ Unexpected error: {e}")
    st.stop()

# --- 2. Fetch Trust Score ---
try:
    response = requests.get(f"{API_URL}/trust-score", timeout=5)
    if response.status_code == 200:
        report = response.json()
    else:
        st.error("Failed to fetch report.")
        st.stop()
except Exception as e:
    st.error(f"Error fetching trust score: {e}")
    st.stop()

# --- 3. Metrics Row ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("📋 GX Score", f"{report['success_rate']:.1f}%")
col2.metric("🧠 AI Trust Score", f"{report['data_trust_score']:.2f}%")
col3.metric("✅ Passed", report['passed_expectations'])
col4.metric("❌ Failed", report['failed_expectations'])

st.divider()

# --- 4. Drift Detection ---
st.subheader("📊 Data Drift Status")
try:
    drift_response = requests.get(f"{API_URL}/drift", timeout=10)
    if drift_response.status_code == 200:
        drift_data = drift_response.json()
        if drift_data.get("drift_detected"):
            st.warning("⚠️ Data Drift Detected!")
            if "results" in drift_data:
                drift_df = pd.DataFrame(drift_data["results"])
                st.dataframe(drift_df, use_container_width=True)
        else:
            st.success("✅ No significant data drift detected.")
    else:
        st.info("Drift check currently unavailable.")
except:
    st.info("Drift check currently unavailable.")

st.divider()

# --- 5. Auto-Healing Recommendations ---
st.subheader("🔧 Auto-Healing Recommendations")
issues = [
    {"Issue": "Age has negative or >120", "Fix": "UPDATE customers SET \"Age\" = NULL WHERE \"Age\" < 0 OR \"Age\" > 120;", "Status": "✅ Safe"},
    {"Issue": "Email has NULL values", "Fix": "UPDATE customers SET email = 'unknown@example.com' WHERE email IS NULL;", "Status": "✅ Safe"},
    {"Issue": "CustomerID duplicates", "Fix": "-- Manual review required", "Status": "⚠️ Blocked"},
]
st.dataframe(pd.DataFrame(issues), use_container_width=True)

st.success("✅ Dashboard loaded successfully!")