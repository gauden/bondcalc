import streamlit as st
import numpy as np

# Function to calculate Yield to Maturity using Newton's method
def calculate_ytm(face_value, coupon_rate, price, years, guess=0.05):
    coupon_payment = coupon_rate * face_value
    # Define a tolerance level and maximum iterations for the iterative process
    tolerance = 1e-6
    max_iterations = 1000
    ytm = guess  # Initial guess for YTM

    for _ in range(max_iterations):
        # Calculate the price using the current YTM guess
        price_guess = sum([coupon_payment / (1 + ytm) ** t for t in range(1, years + 1)]) + face_value / (1 + ytm) ** years

        # Check if the current guess is close enough to the actual price
        if abs(price_guess - price) < tolerance:
            return ytm

        # Derivative of the price function to adjust the guess
        price_derivative = sum([-t * coupon_payment / (1 + ytm) ** (t + 1) for t in range(1, years + 1)]) - years * face_value / (1 + ytm) ** (years + 1)

        # Newton's method formula to update the guess
        ytm = ytm - (price_guess - price) / price_derivative

    return ytm  # Return the approximated YTM

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
