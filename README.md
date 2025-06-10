# 🌤️ Weather Data ETL Pipeline

This project is an **ETL (Extract, Transform, Load)** pipeline built with Python to collect weather data for German cities using an API, transform it into a clean format, and load it into both a CSV file and a PostgreSQL database. The project also includes **email alert functionality** and **task scheduling via Windows Task Scheduler**.

---

## 🗂️ Folder Structure

weather_etl/
├── venv/ # Python virtual environment
├── .env # Environment file to store API keys and credentials
├── .gitignore # Git ignore file for sensitive and unnecessary files
├── README.md # Project documentation (you're reading it!)
├── requirements.txt # Required Python packages
├── run_weather_etl.bat # Batch file for Windows Task Scheduler automation
├── send_email.py # Script to send email alerts
├── upload_to_postgres.py # Loads cleaned data into PostgreSQL
├── weather_data.csv # Output CSV file containing weather data
├── weather_etl.py # Main ETL script (extract, transform, and coordinate)


---

## 📦 Requirements

Create a virtual environment and install the required packages:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

## Required Libraries

requests
pandas
psycopg2
python-dotenv
smtplib


🔐 Environment Variables
Create a .env file with the following contents:

WEATHER_API_KEY=your_openweather_api_key
EMAIL_SENDER=youremail@example.com
EMAIL_PASSWORD=your_email_app_password
EMAIL_RECEIVER=receiver@example.com
DB_HOST=localhost
DB_NAME=weather_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_PORT=5432


⚙️ How It Works

weather_etl.py
Calls weather API to fetch data for German cities

Transforms and cleans the data
Writes the data to weather_data.csv

upload_to_postgres.py
Connects to a PostgreSQL database

Inserts the cleaned data into a weather_data table

send_email.py
Checks for extreme weather values

Sends alerts using email (SMTP)

run_weather_etl.bat
Batch file to run the entire ETL process

Used with Windows Task Scheduler for automation

🗃️ PostgreSQL Table Schema
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100),
    temperature FLOAT,
    humidity INT,
    pressure INT,
    weather_description VARCHAR(255),
    timestamp TIMESTAMP
);


📅 Task Scheduling (Windows)
To automate your ETL process:

Open Task Scheduler on Windows

Create a new Basic Task

Set the trigger (e.g., daily/hourly)

For the action:

Choose Start a program

Browse and select run_weather_etl.bat

This will run your ETL pipeline automatically based on the chosen schedule.

📤 Sample Email Alert
You will receive an email alert like this when conditions are met:

Subject: ⚠️ Weather Alert
Body: Extreme temperature detected in Munich: 39°C. Take precautions.

🚀 Manual Run
To manually execute the full pipeline:


python weather_etl.py
python upload_to_postgres.py
python send_email.py

Or
run the batch file:
run_weather_etl.bat


📌 Author
Tanmay Khairnar
Backend Developer → Data Analyst
LinkedIn | GitHub

