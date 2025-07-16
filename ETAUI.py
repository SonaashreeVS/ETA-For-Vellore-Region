import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib
from haversine import haversine
import folium
import requests
import os
from datetime import datetime
model = joblib.load(r"C:\Users\sonaa\eta_lightgbm_model.pkl")  # Update path if needed
#Vellore Region 
def is_within_vellore(lat, lng):
    return 12.85 <= lat <= 13.05 and 79.00 <= lng <= 79.30
# Photon
def geocode_photon(address):
    bbox = "79.00,13.05,79.30,12.85"
    url = f"https://photon.komoot.io/api/?q={address}&limit=1&bbox={bbox}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data["features"]:
            coords = data["features"][0]["geometry"]["coordinates"]
            return coords[1], coords[0]  # lat, lng
    except:
        return None
    return None
def get_congestion_label():
    now = datetime.now()
    hour = now.hour
    day = now.weekday()  # 0 = Monday, 6 = Sunday
    if day < 5 and (8 <= hour <= 11 or 17 <= hour <= 20):
        return "🔴 High Congestion (Weekday Rush Hour)"
     
    elif day < 5 and (7 <= hour < 8 or 15 <= hour < 17):
        return "🟠 Moderate Congestion (Weekday Moderate)"
    elif day >= 5 and (10 <= hour <= 13 or 18 <= hour <= 21):
        return "🟡 Weekend Busy"
    else:
        return "🟢 Low Congestion (Off-Peak)"
     
def predict_eta(start_lat, start_lng, end_lat, end_lng):
    h_km = haversine((start_lat, start_lng), (end_lat, end_lng))
    data = pd.DataFrame([{
        'start_lat': start_lat,
        'start_lng': start_lng,
        'end_lat': end_lat,
        'end_lng': end_lng,
        'haversine_km': h_km
    }])
    eta_seconds = model.predict(data)[0]
    return round(eta_seconds, 2), round(h_km, 2)
st.set_page_config(page_title="Vellore ETA Predictor", layout="centered")
st.title("🕒 ETA Predictor for Vellore")
st.markdown("Enter **start** and **end addresses** in Vellore. We’ll predict travel time.")
# Input 
start_address = st.text_input("📍 Start Address", "VIT Vellore")
end_address = st.text_input("End Address", "Katpadi Junction")
# Predict 
if st.button("Predict ETA"):
    start_coords = geocode_photon(start_address)
    end_coords = geocode_photon(end_address)

    if not start_coords or not end_coords:
        st.error("Unable to geocode one or both addresses. Please refine them.")
    else:
        s_lat, s_lng = start_coords
        e_lat, e_lng = end_coords

        if not (is_within_vellore(s_lat, s_lng) and is_within_vellore(e_lat, e_lng)):
            st.error("We're not providing rides to that region yet!")
        else:
            eta, dist = predict_eta(s_lat, s_lng, e_lat, e_lng)
            congestion = get_congestion_label()

            st.success(f"🕒 ETA: **{eta / 60:.2f} minutes**")
            st.info(f"Haversine Distance: **{dist:.2f} km**")
            st.warning(f"🚦 Traffic: {congestion}")

            # Map
            m = folium.Map(location=[(s_lat + e_lat) / 2, (s_lng + e_lng) / 2], zoom_start=13)
            folium.Marker([s_lat, s_lng], popup="Start", icon=folium.Icon(color='green')).add_to(m)
            folium.Marker([e_lat, e_lng], popup="End", icon=folium.Icon(color='red')).add_to(m)
            folium.PolyLine(locations=[[s_lat, s_lng], [e_lat, e_lng]], color='blue').add_to(m)

            map_path = "temp_map.html"
            m.save(map_path)
            with open(map_path, "r", encoding="utf-8") as f:
                map_html = f.read()
            components.html(map_html, height=500)
            os.remove(map_path)
