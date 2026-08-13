import os
import subprocess

import requests
import streamlit as st

# Get the API URL from environment variable (set in Hugging Face secrets)
API_URL = os.getenv("API_URL", "http://api:8000")

# --- Fetch Live Data Button ---
if st.button("🌤️ Fetch Live Data & Recalculate Score"):
    with st.spinner("Fetching live weather data..."):
        try:
            # 1. Run the data ingestor script
            # Note: On Hugging Face, use "python" directly, not "poetry run"
            result = subprocess.run(
                ["python", "src/data_ingestor.py"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                st.success("✅ Live data inserted successfully!")

                # 2. Trigger re-validation on the backend
                with st.spinner("Re-running validation..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/run-validation",
                            timeout=60
                        )
                        if response.status_code == 200:
                            st.success("✅ Validation re-run! Refresh the page to see the new Trust Score.")
                            st.info("🔄 Click the refresh button in your browser or press F5.")
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
