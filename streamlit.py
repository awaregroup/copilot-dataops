# Import Required Libraries
import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
import joblib

# Load the pre-trained model and scaler
model = joblib.load('xgb_model.pkl')
scaler = joblib.load('scaler.pkl')

# Define Streamlit App Layout
st.title('Duration Prediction App')
st.write('Enter the entry time and fuel litres to predict the duration.')

# Input fields for entry_time and fuel_litres
entry_time = st.number_input('Entry Time', min_value=0.0, step=0.1)
fuel_litres = st.number_input('Fuel Litres', min_value=0.0, step=0.1)

# Button to trigger prediction
if st.button('Predict Duration'):
    # Scale the input features
    input_features = np.array([[entry_time, 0, fuel_litres]])
    scaled_features = scaler.transform(input_features)
    
    # Make prediction using the XGBoost model
    prediction = model.predict(scaled_features[:, [0, 2]])
    
    # Display the prediction
    st.write(f'Predicted Duration: {prediction[0]:.2f} minutes')