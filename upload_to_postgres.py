import pandas as pd
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()

# Database config (edit as per your setup)
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

TABLE_NAME = 'weather_data'

def upload_csv_to_postgres(csv_file):
    try:
        # Read CSV
        df = pd.read_csv(csv_file)

        # Establish connection
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # Drop table if exists and create new one
        cursor.execute(sql.SQL(f"""
            DROP TABLE IF EXISTS {TABLE_NAME};
            CREATE TABLE {TABLE_NAME} (
                city TEXT,
                temperature FLOAT,
                humidity INTEGER,
                pressure INTEGER,
                weather_description TEXT,
                rain_1h FLOAT,
                cloudiness INTEGER,
                wind_speed FLOAT,
                timestamp TIMESTAMP
            );
        """))
        conn.commit()

        # Insert each row
        for _, row in df.iterrows():
            cursor.execute(sql.SQL(f"""
                INSERT INTO {TABLE_NAME} (city, temperature, humidity, pressure, weather_description,
                    rain_1h, cloudiness, wind_speed, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """), tuple(row))

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Data uploaded to PostgreSQL successfully.")

    except Exception as e:
        print(f"❌ Error uploading to PostgreSQL: {e}")

if __name__ == '__main__':
    upload_csv_to_postgres('weather_data.csv')
