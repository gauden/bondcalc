import streamlit as st
import numpy as np


# Function to calculate Yield to Maturity using Newton's method
def calculate_ytm(face_value, coupon_rate, price, years, guess=0.05):
    coupon_payment = coupon_rate * face_value
    tolerance = 1e-6
    max_iterations = 1000
    ytm = guess  # Initial guess for YTM

    for _ in range(max_iterations):
        price_guess = (
            sum([coupon_payment / (1 + ytm) ** t for t in range(1, years + 1)])
            + face_value / (1 + ytm) ** years
        )
        if abs(price_guess - price) < tolerance:
            return ytm
        price_derivative = sum(
            [-t * coupon_payment / (1 + ytm) ** (t + 1) for t in range(1, years + 1)]
        ) - years * face_value / (1 + ytm) ** (years + 1)
        ytm = ytm - (price_guess - price) / price_derivative

    return ytm


# Function to calculate total return in both absolute dollars and percentage terms
def calculate_total_return(
    face_value, price, coupon_rate, years, markup, withholding_tax
):
    adjusted_price = price + markup
    total_coupon_payments = coupon_rate * face_value * years
    total_coupon_payments_after_tax = total_coupon_payments * (
        1 - withholding_tax / 100
    )
    capital_gain = face_value - adjusted_price
    total_return_absolute = total_coupon_payments_after_tax + capital_gain
    total_return_percentage = (total_return_absolute / adjusted_price) * 100
    return total_return_absolute, total_return_percentage


# Function to calculate annualised return (absolute and percentage)
def calculate_annualised_return(total_return_absolute, total_return_percentage, years):
    annualised_absolute = total_return_absolute / years
    annualised_percentage = (
        (1 + total_return_percentage / 100) ** (1 / years) - 1
    ) * 100
    return annualised_absolute, annualised_percentage


# Streamlit app setup
st.title("Bond Yield to Maturity and Total Return Calculator")

# Data Entry Section
with st.form("data_entry_form"):
    st.header("Enter Bond Details")
    price = st.number_input("Current Price of the Bond", value=1000.0)
    face_value = st.number_input("Face Value of the Bond", value=1000.0)
    coupon_rate = (
        st.number_input("Annual Interest Rate (Coupon Rate) as a percentage", value=5.0)
        / 100
    )
    years = st.number_input("Years until Maturity", value=5)
    markup = st.number_input("Markup on Purchase (in dollars)", value=12.0)
    withholding_tax = st.number_input(
        "Withholding Tax (in percentage, defaults to 15%)", value=15.0
    )

    # Submit button to calculate
    calculate_button = st.form_submit_button("Calculate")

# Results Section - Only show if the button is pressed
if calculate_button:
    # Calculate Yield to Maturity (YTM)
    ytm = calculate_ytm(face_value, coupon_rate, price, years)
    ytm_percentage = ytm * 100  # Convert to percentage

    # Calculate Total Return in both absolute and percentage terms
    total_return_absolute, total_return_percentage = calculate_total_return(
        face_value, price, coupon_rate, years, markup, withholding_tax
    )

    # Calculate Annualised Returns
    annualised_absolute, annualised_percentage = calculate_annualised_return(
        total_return_absolute, total_return_percentage, years
    )

    # Display Results
    st.header("Results")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Yield to Maturity (YTM)", f"{ytm_percentage:.2f}%")
    with col2:
        st.metric("Total Return (Absolute)", f"${total_return_absolute:.2f}")
    with col3:
        st.metric("Total Return (Percentage)", f"{total_return_percentage:.2f}%")
    with col4:
        st.metric("Annualised Return (Absolute)", f"${annualised_absolute:.2f}")
    with col5:
        st.metric("Annualised Return (Percentage)", f"{annualised_percentage:.2f}%")

    # Display a summary table of data entered
    st.subheader("Summary of Data Entered")
    summary_data = {
        "Current Price": [f"${price:.2f}"],
        "Face Value": [f"${face_value:.2f}"],
        "Coupon Rate": [f"{coupon_rate * 100:.2f}%"],
        "Years to Maturity": [years],
        "Markup": [f"${markup:.2f}"],
        "Withholding Tax": [f"{withholding_tax:.2f}%"],
    }
    st.table(summary_data)
