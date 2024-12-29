import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the saved best model, scaler, and label encoder
with open('best_weather_model.pkl', 'rb') as f:
    best_model = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('weather_label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

# Function to take user input for prediction
def get_user_input():
    st.title("Weather Prediction")

    st.markdown("""
        ### Instructions
        Please enter the weather data for your city, and then click **Predict** to get the weather condition prediction.
    """)

    city = st.text_input("City", "Mumbai")

    temperature = st.number_input("Temperature (°C)", min_value=-50.0, max_value=60.0, value=30.0)
    humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=70.0)
    pressure = st.number_input("Pressure (hPa)", min_value=900.0, max_value=1100.0, value=1015.0)
    wind_speed = st.number_input("Wind Speed (km/h)", min_value=0.0, max_value=200.0, value=15.0)
    rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=500.0, value=0.0)

    # Return the data as a dictionary
    return {
        'City': city,
        'Temperature (°C)': temperature,
        'Humidity (%)': humidity,
        'Pressure (hPa)': pressure,
        'Wind Speed (km/h)': wind_speed,
        'Rainfall (mm)': rainfall
    }

# Get user input
user_input = get_user_input()

# Create a button for prediction
if st.button("Predict"):
    try:
        # Check if the input is valid
        if user_input:
            # Convert user input into a DataFrame
            new_data = pd.DataFrame([user_input])

            # Retain the 'City' column for output
            city_column = new_data['City']

            # Exclude 'City' column before scaling and predicting
            new_data_features = new_data[['Temperature (°C)', 'Humidity (%)', 'Pressure (hPa)', 'Wind Speed (km/h)', 'Rainfall (mm)']]

            # Scale the features
            new_data_scaled = scaler.transform(new_data_features)

            # Predict the weather condition using the best model
            predicted_weather = best_model.predict(new_data_scaled)

            # Decode the predicted weather condition
            predicted_condition = label_encoder.inverse_transform([int(predicted_weather)])[0]

            # Display the result to the user with a larger font size and inside a box
            st.markdown(f"""
            <div style="background-color: #f1f1f1; padding: 15px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                <h3 style="color: #3E8E41; font-size: 24px; font-weight: bold;">📅 The predicted weather condition is:</h3>
                <h2 style="color: #1E4D2B; font-size: 28px; font-weight: bold;">**{predicted_condition}**</h2>
            </div>
            """, unsafe_allow_html=True)

            # Weather condition advice in a more prominent box with icons and larger text
            if predicted_condition == "Thunderstorms":
                st.markdown(f"""
                <div style="background-color: #ffcccc; padding: 15px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <h3 style="color: #e60000; font-size: 20px; font-weight: bold;">⚡ **Thunderstorms** detected!</h3>
                    <p style="font-size: 18px;">Please stay indoors and stay safe!</p>
                </div>
                """, unsafe_allow_html=True)
            elif predicted_condition == "Partly Cloudy":
                st.markdown(f"""
                <div style="background-color: #ffeb99; padding: 15px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <h3 style="color: #ff9933; font-size: 20px; font-weight: bold;">🌤️ **Partly Cloudy** - A pleasant day!</h3>
                    <p style="font-size: 18px;">It's a great day for outdoor activities!</p>
                </div>
                """, unsafe_allow_html=True)
            elif predicted_condition == "Rainy":
                st.markdown(f"""
                <div style="background-color: #cce0ff; padding: 15px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <h3 style="color: #0066cc; font-size: 20px; font-weight: bold;">🌧️ **Rainy** weather expected!</h3>
                    <p style="font-size: 18px;">Don't forget your umbrella!</p>
                </div>
                """, unsafe_allow_html=True)
            elif predicted_condition == "Cloudy":
                st.markdown(f"""
                <div style="background-color: #d6d6d6; padding: 15px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <h3 style="color: #555555; font-size: 20px; font-weight: bold;">☁️ **Cloudy** day ahead</h3>
                    <p style="font-size: 18px;">No immediate rain expected.</p>
                </div>
                """, unsafe_allow_html=True)
            elif predicted_condition == "Clear":
                st.markdown(f"""
                <div style="background-color: #b3e6cc; padding: 15px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <h3 style="color: #33cc33; font-size: 20px; font-weight: bold;">🌞 **Clear** weather ahead!</h3>
                    <p style="font-size: 18px;">Great day to enjoy the sunshine!</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background-color: #fff3e6; padding: 15px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                    <h3 style="color: #ff9933; font-size: 20px; font-weight: bold;">🤷 Weather condition is uncertain based on the data</h3>
                </div>
                """, unsafe_allow_html=True)

            # Save the prediction result and user input to a CSV file
            user_input['Predicted Weather Condition'] = predicted_condition  # Add predicted condition to the user input data
            prediction_result = pd.DataFrame([user_input])

            # Append the result to a CSV file
            prediction_result.to_csv('weather_predictions.csv', mode='a', header=False, index=False)

            st.success(f"Prediction saved to `weather_predictions.csv`")

            # Display extra notes for the user
            st.markdown("""
                ### Notes:
                - The model predicts weather conditions based on temperature, humidity, pressure, wind speed, and rainfall.
                - Ensure that your input data is accurate for better predictions.
                - This model is trained on historical data and may not be suitable for real-time weather forecasting.
            """)

        else:
            st.error("Please provide all required inputs before predicting.")
    
    except ValueError:
        st.write("🚨 Error: Please enter valid numerical values for all inputs.")
