"""# TaxiFareModel front"""

import streamlit as st
import requests
from math import sin, cos, sqrt, atan2

KM_TO_MILES = 0.621371

def compute_dist(lon1, lat1, lon2, lat2):
    """Compute the ride distance in km"""
    R = 6373.0
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R*c

# @TODO
# split date/time
# add map

st.text("Please fill in with your needs:")
# date  = st.date_input
# input = st.time_input
pickup_datetime   = st.text_input("Pick-up date and time (%YYYY-%MM-%DD %HH:%mm:%SS, US/Eastern time):", "2009-12-31 23:59:59")
pickup_longitude  = st.number_input("Pick-up longitude:",  value=-73.950, step=0.001, format="%.3f", min_value=-180., max_value=180.)
pickup_latitude   = st.number_input("Pick-up latitude:",   value=+40.750, step=0.001, format="%.3f", min_value=-90.,  max_value=90.)
dropoff_longitude = st.number_input("Drop-off longitude:", value=-73.990, step=0.001, format="%.3f", min_value=-180., max_value=180.)
dropoff_latitude  = st.number_input("Drop-off latitude:",  value=+40.950, step=0.001, format="%.3f", min_value=-90.,  max_value=90.)
passenger_count   = st.number_input("Passenger count:",    value=1, min_value=0, max_value=69)
st.text("Note that in the pick-up/drop-off coordinates, the +/- buttons are ~100m strides")

distance = compute_dist(pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude)
unit = "km"
if st.checkbox("Use miles", key="chbox_use_miles"):
    distance *= KM_TO_MILES
    unit = "mile"
st.write(f"Ride distance: {distance:.2f} {unit}")

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
    response = requests.get(URL, params)
    response.raise_for_status()
    fare_pred = response.json()["fare"]
    st.write(f"This ride should cost around ${fare_pred:.2f}")
