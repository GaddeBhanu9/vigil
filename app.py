import os
import subprocess
import sys
import requests
import streamlit as st
from datetime import datetime

# Page config
st.set_page_config(page_title="Project VIGIL", layout="wide")

# Get the API URL from environment variable
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("🛡️ Project VIGIL")
st.caption("Autonomous AI Data Quality & Observability Platform")

# --- Fetch Trust Score ---
try:
    response = requests.get(f"{API_URL}/trust-score", timeout=120)
    if response.status_code == 200:
        report = response.json()
    else:
        st.error("Failed to fetch report.")
        st.stop()
except Exception as e:
    st.error(f"Error fetching trust score: {e}")
    st.stop()

# --- Metrics Row (WITH REPORT ID) ---
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("📋 GX Score", f"{report['success_rate']:.1f}%")
col2.metric("🧠 AI Trust Score", f"{report['data_trust_score']:.2f}%")
col3.metric("✅ Passed", report['passed_expectations'])
col4.metric("❌ Failed", report['failed_expectations'])
col5.metric("🆔 Report ID", report['report_id'])  # 👈 This proves it updated!

# --- Persistent Last Update Message ---
if "last_update" in st.session_state:
    st.success(st.session_state["last_update"])
elif "last_error" in st.session_state:
    st.warning(st.session_state["last_error"])

st.divider()

# --- Fetch Live Data Button ---
if st.button("🌤️ Fetch Live Data & Recalculate Score"):
    with st.spinner("Fetching live weather data..."):
        try:
            env = os.environ.copy()
            result = subprocess.run(
                [sys.executable, "src/data_ingestor.py"],
                capture_output=True,
                text=True,
                timeout=30,
                env=env
            )

            if result.returncode == 0:
                st.success("✅ Live data inserted successfully!")

                # Trigger re-validation
                with st.spinner("Re-running validation..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/run-validation",
                            timeout=300
                        )
                        if response.status_code == 200:
                            st.session_state["last_update"] = f"✅ Validation completed at {datetime.now().strftime('%H:%M:%S')}"
                            st.session_state.pop("last_error", None)
                            # Refresh the page to show the new Report ID
                            st.query_params["refresh"] = str(datetime.now().timestamp())
                            st.rerun()
                        elif response.status_code == 429:
                            st.session_state["last_error"] = "⚠️ Gemini API quota exceeded (429). Auto-healing will work tomorrow."
                            st.rerun()
                        else:
                            st.warning(f"⚠️ Validation triggered but returned status: {response.status_code}")
                    except requests.exceptions.ConnectionError:
                        st.error("🚨 Cannot connect to backend. Is the API running?")
                    except Exception as e:
                        st.error(f"❌ Error during validation: {e}")
            else:
                st.error(f"❌ Failed to fetch data: {result.stderr}")

        except subprocess.TimeoutExpired:
            st.error("⏰ Data fetch timed out. Please try again.")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")