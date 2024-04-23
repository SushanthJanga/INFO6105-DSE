import streamlit as st
import requests
import pickle

# Define functions to interact with the server
def get_location_names():
    try:
        response = requests.get("http://127.0.0.1:5000/get_location_names")
        response.raise_for_status()  # Raise an exception for HTTP errors
        # with open("model/banglore_home_prices_model.pickle", "rb") as f:
        #     location_names = pickle.load(f)
        # return location_names
        data = response.json()
        return data["locations"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching location names: {e}")
        return []

def predict_home_price(total_sqft, location, bhk, bath):
    try:
        payload = {
            "total_sqft": total_sqft,
            "location": location,
            "bhk": bhk,
            "bath": bath
        }
        response = requests.post("http://127.0.0.1:5000/predict_home_price", data=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data["estimated_price"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error predicting home price: {e}")
        return None

# Streamlit app layout
def main():
    st.title("Bangalore Home Price Prediction")
    
    # Input fields
    total_sqft = st.number_input("Area (Square Feet)", value=1000)
    bhk = st.radio("BHK", [1, 2, 3, 4, 5], index=1)
    bath = st.radio("Bath", [1, 2, 3, 4, 5], index=1)
    location_names = get_location_names()
    if not location_names:
        st.error("Failed to fetch location names. Please check the server.")
        return
    location = st.selectbox("Location", options=location_names)
    
    # Prediction button
    if st.button("Estimate Price"):
        estimated_price = predict_home_price(total_sqft, location, bhk, bath)
        if estimated_price is not None:
            st.write(f"Estimated Price: {estimated_price} Lakhs")

if __name__ == "__main__":
    main()
