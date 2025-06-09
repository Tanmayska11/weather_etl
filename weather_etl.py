import requests
import pandas as pd
import os
from datetime import datetime
from upload_to_postgres import upload_csv_to_postgres
from send_email import send_email_notification
from send_email import send_email_notification_no_update
from dotenv import load_dotenv

load_dotenv()

# CONFIG: Replace with your actual API key from OpenWeatherMap
API_KEY = os.getenv('API_KEY')


# List of 20 German cities with coordinates
cities = [
    {"name": "Munich", "lat": 48.137154, "lon": 11.576124},
    {"name": "Berlin", "lat": 52.5200, "lon": 13.4050},
    {"name": "Hamburg", "lat": 53.5511, "lon": 9.9937},
    {"name": "Frankfurt", "lat": 50.1109, "lon": 8.6821},
    {"name": "Cologne", "lat": 50.9375, "lon": 6.9603},
    {"name": "Stuttgart", "lat": 48.7758, "lon": 9.1829},
    {"name": "Düsseldorf", "lat": 51.2277, "lon": 6.7735},
    {"name": "Leipzig", "lat": 51.3397, "lon": 12.3731},
    {"name": "Dresden", "lat": 51.0504, "lon": 13.7373},
    {"name": "Nuremberg", "lat": 49.4521, "lon": 11.0767},
    {"name": "Hanover", "lat": 52.3759, "lon": 9.7320},
    {"name": "Bremen", "lat": 53.0793, "lon": 8.8017},
    {"name": "Essen", "lat": 51.4556, "lon": 7.0116},
    {"name": "Dortmund", "lat": 51.5136, "lon": 7.4653},
    {"name": "Bochum", "lat": 51.4818, "lon": 7.2162},
    {"name": "Wuppertal", "lat": 51.2562, "lon": 7.1508},
    {"name": "Bonn", "lat": 50.7374, "lon": 7.0982},
    {"name": "Mannheim", "lat": 49.4875, "lon": 8.4660},
    {"name": "Karlsruhe", "lat": 49.0069, "lon": 8.4037},
    {"name": "Augsburg", "lat": 48.3705, "lon": 10.8978}
]

def extract(lat, lon):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}'
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")    
    return response.json()

def transform(data):
    return {
        'city': data.get('name'),
        'temperature': data['main'].get('temp'),
        'humidity': data['main'].get('humidity'),
        'pressure': data['main'].get('pressure'),
        'weather_description': data['weather'][0].get('description'),
        'rain_1h': data.get('rain', {}).get('1h', 0),
        'cloudiness': data['clouds'].get('all'),
        'wind_speed': data['wind'].get('speed'),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def load(data_list):
    df_new = pd.DataFrame(data_list)

    if os.path.exists('weather_data.csv'):
        df_old = pd.read_csv('weather_data.csv')
        # Compare new data with old data
        if df_new.equals(df_old):
            print("No update in data.")
            return False  # Data NOT updated
    # Save new data (overwrite existing)
    df_new.to_csv('weather_data.csv', index=False)
    print("Data updated and saved to CSV.")
    return True  # Data updated


def main():
    all_data = []
    for city in cities:
        try:
            raw_data = extract(city["lat"], city["lon"])
            clean_data = transform(raw_data)
            all_data.append(clean_data)
            print(f"✅ {clean_data['city']} saved.")
        except Exception as e:
            print(f"❌ Error with {city['name']}: {e}")

    if all_data:
        updated = load(all_data)
        
        if updated:
            upload_csv_to_postgres('weather_data.csv')
            # Send email notification that data was updated
            send_email_notification('weather_data.csv', os.getenv('EMAIL'))
        else:
           
            send_email_notification_no_update(os.getenv('EMAIL'))# Data not updated - send different email (optional)

    else:
        print("⚠️ No data collected from any city. Sending failure email...")
        
        send_email_notification_no_update(os.getenv('EMAIL'))      

if __name__ == '__main__':
    main()
    
    
