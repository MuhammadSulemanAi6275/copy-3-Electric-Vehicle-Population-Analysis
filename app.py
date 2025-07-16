# app.py

import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load model and features
model = joblib.load("Electric_Range_Model.pkl")
features = joblib.load("model_features.pkl")

# Page settings
st.set_page_config(layout="wide", page_title="EV Range Predictor")

# Custom CSS styling
st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        h1 {
            color: #00ff99;
            text-align: center;
        }
        h2, h3, .stMarkdown {
            color: #00c3ff;
        }
        .stNumberInput label, .stSelectbox label {
            color: white !important;
        }
        .stButton > button {
            background-color: #00796B;
            color: white;
            border: none;
        }
        .big-prediction {
            font-size: 32px;
            color: #39ff14;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Centered title
st.markdown("<h1 style='color: white; text-align: center;'>🔋 Electric Vehicle Range Predictor</h1>", unsafe_allow_html=True)

st.markdown("<h6 style='text-align: right; color: White;'>Developed by <strong>Muhammad Suleman Shah</strong></h4>", unsafe_allow_html=True)

# Input form
st.subheader("🚘 Enter Vehicle Information")

input_dict = {feature: 0 for feature in features}

# --- Numeric Inputs ---
col1, col2, col3 = st.columns(3)

with col1:
    input_dict['Model Year'] = st.number_input("📅 Model Year", 2010, 2025, 2018)

with col2:
    input_dict['Base MSRP'] = st.number_input("💰 Base MSRP ($) [Manufacturer’s Suggested Retail Price]", 10000, 150000, 40000)

with col3:
    input_dict['Legislative District'] = st.number_input("🏛️ Legislative District [Which the vehicle is registered]", 1, 50, 30)

# --- Categorical Inputs ---
col4, col5 = st.columns(2)

with col4:
    make = st.selectbox("🚗 Make", ["TESLA", "NISSAN", "KIA", "AUDI", "CHEVROLET", "JEEP", "FORD", "FIAT", "PORSCHE"])

with col5:
    model_name = st.selectbox("📍 Model", ["MODEL 3", "LEAF", "SOUL", "E-TRON", "BOLT EV", "WRANGLER", "F-150", "500", "CAYENNE"])

# Encode selected categorical features
for col in features:
    if f"Make_{make}" == col:
        input_dict[col] = 1
    if f"Model_{model_name}" == col:
        input_dict[col] = 1

# --- Predict ---
st.markdown("---")
if st.button("🚀 Predict Electric Range"):
    input_df = pd.DataFrame([input_dict])
    prediction = model.predict(input_df)[0]

    # Big, centered prediction output
    st.markdown("### 📊 Predicted Electric Range")
    st.markdown(f"""
        <div style='text-align: center; padding: 10px;'>
            <span style='font-size: 40px; color: #39ff14; font-weight: bold;'>{int(prediction)} miles</span>
        </div>
    """, unsafe_allow_html=True)

    # Reaction message
    st.markdown("---")
    if prediction >= 100:
        st.markdown("### 🥳 **HURRAAAA! This EV has an excellent range. You're good to go!** 🎉")
    else:
        st.markdown("### 😢 **Oops! The range is low. Consider another model.**")
