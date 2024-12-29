import csv
import random
from datetime import datetime, timedelta

# List of cities in India for simulation
cities = [
    "Mumbai", "Delhi", "Kolkata", "Chennai", "Bangalore",
    "Hyderabad", "Kochi", "Pune", "Ahmedabad", "Jaipur"
]

# Weather conditions to simulate
weather_conditions = [
    "Clear", "Cloudy", "Rain", "Partly Cloudy", "Thunderstorms", "Heavy Rain"
]

# Function to generate random weather data
def generate_weather_data():
    city = random.choice(cities)
    date = datetime.now() - timedelta(days=random.randint(0, 30))
    date_str = date.strftime("%Y-%m-%d")
    temperature = round(random.uniform(20.0, 35.0), 1)  # Temperature in Celsius
    humidity = random.randint(50, 90)  # Humidity percentage
    pressure = random.randint(1005, 1025)  # Pressure in hPa
    wind_speed = random.randint(5, 20)  # Wind speed in km/h
    rainfall = round(random.uniform(0.0, 15.0), 1)  # Rainfall in mm
    condition = random.choice(weather_conditions)  # Weather condition

    return {
        "Date": date_str,
        "City": city,
        "Temperature (°C)": temperature,
        "Humidity (%)": humidity,
        "Pressure (hPa)": pressure,
        "Wind Speed (km/h)": wind_speed,
        "Rainfall (mm)": rainfall,
        "Weather Condition": condition
    }

# Create CSV file with UTF-8 encoding and write 1000 entries
with open("india_weather_data.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=[
        "Date", "City", "Temperature (°C)", "Humidity (%)", 
        "Pressure (hPa)", "Wind Speed (km/h)", "Rainfall (mm)", "Weather Condition"
    ])
    
    writer.writeheader()

    for _ in range(1000):
        data = generate_weather_data()
        writer.writerow(data)

print("CSV file 'india_weather_data.csv' with 1000 entries created successfully.")
