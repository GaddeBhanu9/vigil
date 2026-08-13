"""
Project VIGIL - FastAPI Backend
Serves Data Trust Score, Drift Detection, and Anomalies.
"""
import os
import json
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Import the drift detector function
from src.drift_detector import load_and_split_data, run_drift_tests
print("🚀 Starting FastAPI backend...")
load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

app = FastAPI(title="Project VIGIL API", version="2.0")

# Allow Streamlit to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "🛡️ Project VIGIL API is running"}

@app.get("/trust-score")
def get_trust_score():
    """Fetch the latest Data Trust Score."""
    query = """
    SELECT 
        report_id, run_timestamp, total_expectations, 
        passed_expectations, failed_expectations, 
        success_rate, data_trust_score, validation_results
    FROM validation_reports
    ORDER BY run_timestamp DESC LIMIT 1
    """
    df = pd.read_sql(query, engine)
    if df.empty:
        raise HTTPException(status_code=404, detail="No reports found")
    return df.iloc[0].to_dict()

@app.get("/drift")
def get_drift_report():
    """
    Run the drift detection and return the results as JSON.
    """
    try:
        # Load and split data
        reference, current = load_and_split_data()
        
        # Run statistical tests
        report = run_drift_tests(reference, current)
        
        return {
            "status": "success",
            "drift_detected": report["drift_detected"],
            "results": report["results"]
        }
    except Exception as e:
        return {
            "status": "error",
            "drift_detected": False,
            "message": str(e)
        }

@app.get("/anomalies")
def get_anomalies():
    """
    Return the top anomalous customers from the Autoencoder.
    """
    try:
        # Load the cleaned data with anomaly scores
        df = pd.read_csv('data/cleaned_customers.csv')
        
        # If the file doesn't have the AE column, return a message
        if 'AE_Reconstruction_Error' not in df.columns:
            return {"status": "warning", "message": "Anomaly scores not found. Run the Autoencoder notebook first."}
        
        # Top 10 anomalies
        top_anomalies = df.nlargest(10, 'AE_Reconstruction_Error')
        return {
            "status": "success",
            "total_customers": len(df),
            "top_anomalies": top_anomalies[['CustomerID', 'Age_scaled', 'Purchase_scaled', 'AE_Reconstruction_Error']].to_dict(orient='records')
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/run-validation")
def trigger_validation():
    """Trigger a new Great Expectations validation run and save results."""
    try:
        from src.reporter import run_full_report
        # This runs validation AND saves the results to the database
        run_full_report()
        return {"status": "success", "message": "Validation completed and saved to database"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

