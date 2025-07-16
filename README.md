# 🗺️ ETA Prediction Module – Vellore Region (Dataset Link Given Below)

This module provides Estimated Time of Arrival (ETA) predictions for routes within the Vellore region. Based on historical travel time data, users can input a start and destination location to view the estimated travel time along with a route map. Since we can't remember the random numbers for latitude and longitude of certain region I've made sure to convert them into names of regions using "geocode photon'.

---

## ✅ Features

- 📍 **User Input for Start and Destination Points**
- ⏱️ **Accurate ETA Calculation** using historical data obtained using OpenStreetMap and using the model trained using LightGBM Algorithm.
- 🗺️ **Map Visualization** for the selected route using Folium
- 🧭 **Standalone Module** – No integration with alert systems
- 📊 Designed for **Vellore-specific datasets**
- ** Tweaks the value of ETA according to time of day, week of the day and highly congested hours**

  **Dataset** :
  **https://www.kaggle.com/datasets/sonsas/vellore-region-latitude-and-longitude**
  
