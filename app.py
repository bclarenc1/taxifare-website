"""# TaxiFareModel front"""

import streamlit as st
import requests
import pandas as pd
from math import sin, cos, sqrt, atan2, radians

KM_TO_MILES = 0.621371

def compute_dist(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """Compute the ride distance in km"""
    R = 6373.0
    lon1 = radians(lon1); lat1 = radians(lat1)
    lon2 = radians(lon2); lat2 = radians(lat2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

st.title("(Ill-trained) ride fare estimator")
st.markdown("## Please fill in with your needs:")

st.markdown("### Time")
pickup_date = st.date_input("Pick-up date", format="YYYY-MM-DD")
pickup_time = st.time_input("Pick-up time", step=60)
pickup_datetime   = f"{pickup_date} {pickup_time}"
st.markdown("### Places")
pickup_longitude  = st.number_input("Pick-up longitude:",  value=-73.950, step=0.001, format="%.3f", min_value=-180., max_value=180.)
pickup_latitude   = st.number_input("Pick-up latitude:",   value=+40.750, step=0.001, format="%.3f", min_value=-90.,  max_value=90.)
dropoff_longitude = st.number_input("Drop-off longitude:", value=-73.990, step=0.001, format="%.3f", min_value=-180., max_value=180.)
dropoff_latitude  = st.number_input("Drop-off latitude:",  value=+40.950, step=0.001, format="%.3f", min_value=-90.,  max_value=90.)

route_df = pd.DataFrame({"lon":[pickup_longitude, dropoff_longitude],
                         "lat":[pickup_latitude, dropoff_latitude],
                         "color":[(255,0,0), (0,255,0)]})
st.map(route_df, latitude="lat", longitude="lon", size=20, color="color")
st.markdown(":red[start point] -> :green[end point]")
distance = compute_dist(pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude)
unit = "km"
if st.checkbox("Use miles", key="chbox_use_miles"):
    distance *= KM_TO_MILES
    unit = "mile" if distance == 1. else "miles"
st.write(f"Ride distance: {distance:.2f} {unit}")

st.markdown("### For whom")
passenger_count   = st.number_input("Passenger count:",    value=1, min_value=0, max_value=69)

st.markdown("### >> Results")
URL = "https://taxifare-743320960469.europe-west1.run.app/predict"
# LEWAGON_URL = "https://taxifare.lewagon.ai/predict"

params = {
    "pickup_datetime":   pickup_datetime,
    "pickup_longitude":  pickup_longitude,
    "pickup_latitude":   pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude":  dropoff_latitude,
    "passenger_count":   passenger_count}

if st.button("Estimate ride fare", key="btn_predict"):
    if passenger_count == 0:
        msg = "What do you mean, no passengers?"
    else:
        response = requests.get(URL, params)
        response.raise_for_status()
        fare_pred = response.json()["fare"]
        msg = f"This ride should cost around **${fare_pred:.2f}**"
        if passenger_count > 1:
            msg += f" ({fare_pred/passenger_count:.2f} per passenger)"
    st.markdown(msg)
