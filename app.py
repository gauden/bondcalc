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

# Function to calculate total return in both absolute dollars and percentage terms
def calculate_total_return(face_value, price, coupon_rate, years, markup, withholding_tax):
    # Adjust price for markup in dollars
    adjusted_price = price + markup
    
    # Total coupon payments over the bond's life
    total_coupon_payments = coupon_rate * face_value * years
    
    # Apply withholding tax to coupon payments
    total_coupon_payments_after_tax = total_coupon_payments * (1 - withholding_tax / 100)
    
    # Capital gain (or loss) at maturity
    capital_gain = face_value - adjusted_price
    
    # Calculate total return in absolute dollar terms
    total_return_absolute = total_coupon_payments_after_tax + capital_gain
    
    # Calculate total return in percentage terms
    total_return_percentage = (total_return_absolute / adjusted_price) * 100
    
    return total_return_absolute, total_return_percentage

# Streamlit app setup
st.title("Bond Yield to Maturity and Total Return Calculator")

# Inputs from the user
price = st.number_input("Current Price of the Bond", value=1000.0)
face_value = st.number_input("Face Value of the Bond", value=1000.0)
coupon_rate = st.number_input("Annual Interest Rate (Coupon Rate) as a percentage", value=5.0) / 100
years = st.number_input("Years until Maturity", value=5)
markup = st.number_input("Markup on Purchase (in dollars)", value=12.0)
withholding_tax = st.number_input("Withholding Tax (in percentage, defaults to 15%)", value=15.0)

# Calculate Yield to Maturity (YTM)
ytm = calculate_ytm(face_value, coupon_rate, price, years)
ytm_percentage = ytm * 100  # Convert to percentage

# Calculate Total Return in both absolute and percentage terms
total_return_absolute, total_return_percentage = calculate_total_return(face_value, price, coupon_rate, years, markup, withholding_tax)

# Display the results
st.write(f"Yield to Maturity (YTM): {ytm_percentage:.2f}%")
st.write(f"Total Return (after withholding tax and markup): ${total_return_absolute:.2f} ({total_return_percentage:.2f}%)")
