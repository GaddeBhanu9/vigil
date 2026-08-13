"""
Live Data Ingestor for Project VIGIL
Fetches real-time weather data and inserts it into the customers table.
"""
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

def fetch_live_weather():
    """Fetch current weather for London."""
    url = "https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.1&current_weather=true"
    response = requests.get(url)
    data = response.json()

    weather = data["current_weather"]

    new_row = {
        "CustomerID": f"LIVE_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "Name": f"Weather_{weather['temperature']:.1f}C",
        "Gender": "M" if weather["temperature"] > 10 else "F",
        "Age": int(abs(weather["temperature"]) * 1.5) + 20,
        "City": "London",
        "Signup_Date": datetime.now().strftime("%d/%m/%Y"),
        "Last_purchase_date": datetime.now().strftime("%d/%m/%Y"),
        "purchase_amount": abs(weather["temperature"]) * 10,
        "feedback_score": int(abs(weather["windspeed"]) % 10) + 1,
        "email": f"weather_{weather['temperature']:.1f}@live.com",
        "Phone_number": f"0{int(abs(weather['temperature'])*100)}",
        "Country": "UK"
    }
    return new_row

def insert_live_data():
    """Fetch live data and insert into Neon."""
    new_row = fetch_live_weather()
    df = pd.DataFrame([new_row])
    df.to_sql("customers", engine, if_exists="append", index=False)
    print(f"✅ Inserted live data: {new_row['Name']}")

if __name__ == "__main__":
    insert_live_data()
