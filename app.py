import streamlit as st
import numpy as np

# Function to calculate Yield to Maturity
def calculate_ytm(face_value, coupon_rate, price, years):
    coupon_payment = coupon_rate * face_value
    ytm = np.irr([-price] + [coupon_payment] * years + [face_value + coupon_payment])
    return ytm

# Function to calculate total return
def calculate_total_return(face_value, price, coupon_rate, years):
    total_coupon_payments = coupon_rate * face_value * years
    capital_gain = face_value - price
    total_return = (total_coupon_payments + capital_gain) / price
    return total_return * 100  # Return as a percentage

# Streamlit app setup
st.title("Bond Yield to Maturity and Total Return Calculator")

# Inputs from the user
price = st.number_input("Current Price of the Bond", value=1000.0)
face_value = st.number_input("Face Value of the Bond", value=1000.0)
coupon_rate = st.number_input("Annual Interest Rate (Coupon Rate) as a percentage", value=5.0) / 100
years = st.number_input("Years until Maturity", value=5)

# Calculate Yield to Maturity (YTM)
ytm = calculate_ytm(face_value, coupon_rate, price, years)
ytm_percentage = ytm * 100  # Convert to percentage

# Calculate Total Return
total_return = calculate_total_return(face_value, price, coupon_rate, years)

# Display the results
st.write(f"Yield to Maturity (YTM): {ytm_percentage:.2f}%")
st.write(f"Total Return: {total_return:.2f}%")
