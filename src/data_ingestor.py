"""
Live Data Ingestor for Project VIGIL (No Pandas, No SQLAlchemy)
Uses raw SQL with psycopg2 to insert data.
"""
import os
import requests
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def insert_live_data():
    """Fetch live weather and insert into Neon using raw SQL."""
    # Connect to database
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    # Fetch live weather from Open-Meteo
    url = "https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.1&current_weather=true"
    data = requests.get(url).json()
    weather = data["current_weather"]

    # Insert using raw SQL (no pandas)
    cur.execute("""
        INSERT INTO customers 
        (CustomerID, Name, Gender, Age, City, Signup_Date, Last_purchase_date, 
         purchase_amount, feedback_score, email, Phone_number, Country)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        f"LIVE_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        f"Weather_{weather['temperature']:.1f}C",
        "M" if weather["temperature"] > 10 else "F",
        int(abs(weather["temperature"]) * 1.5) + 20,
        "London",
        datetime.now().strftime("%d/%m/%Y"),
        datetime.now().strftime("%d/%m/%Y"),
        abs(weather["temperature"]) * 10,
        int(abs(weather["windspeed"]) % 10) + 1,
        f"weather_{weather['temperature']:.1f}@live.com",
        f"0{int(abs(weather['temperature'])*100)}",
        "UK"
    ))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Inserted live data successfully!")

if __name__ == "__main__":
    insert_live_data()