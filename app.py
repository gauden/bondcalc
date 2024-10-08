import streamlit as st
import numpy as np

# Function to calculate Yield to Maturity using Newton's method
def calculate_ytm(face_value, coupon_rate, price, years, guess=0.05):
    coupon_payment = coupon_rate * face_value
    tolerance = 1e-6
    max_iterations = 1000
    ytm = guess  # Initial guess for YTM

    for _ in range(max_iterations):
        price_guess = sum([coupon_payment / (1 + ytm) ** t for t in range(1, years + 1)]) + face_value / (1 + ytm) ** years
        if abs(price_guess - price) < tolerance:
            return ytm
        price_derivative = sum([-t * coupon_payment / (1 + ytm) ** (t + 1) for t in range(1, years + 1)]) - years * face_value / (1 + ytm) ** (years + 1)
        ytm = ytm - (price_guess - price) / price_derivative

    return ytm

# Function to calculate total return in both absolute dollars and percentage terms
def calculate_total_return(face_value, price, coupon_rate, years, markup, withholding_tax):
    adjusted_price = price + markup
    total_coupon_payments = coupon_rate * face_value * years
    total_coupon_payments_after_tax = total_coupon_payments * (1 - withholding_tax / 100)
    capital_gain = face_value - adjusted_price
    total_return_absolute = total_coupon_payments_after_tax + capital_gain
    total_return_percentage = (total_return_absolute / adjusted_price) * 100
    total_return_annualized_percentage = (1 + total_return_percentage / 100) ** (1 / years) - 1
    total_return_annualized_absolute = total_return_absolute / years
    return total_return_absolute, total_return_annualized_absolute, total_return_percentage, total_return_annualized_percentage

# Streamlit app setup
st.title("Bond Yield to Maturity and Total Return Calculator")

# Step 1: Data Entry
if 'show_results' not in st.session_state:
    st.session_state['show_results'] = False

def reset_results():
    st.session_state['show_results'] = False

with st.expander("Data Entry", expanded=not st.session_state['show_results']):
    price = st.number_input("Current Price of the Bond", value=1000.0, on_change=reset_results)
    face_value = st.number_input("Face Value of the Bond", value=1000.0, on_change=reset_results)
    coupon_rate = st.number_input("Annual Interest Rate (Coupon Rate) as a percentage", value=5.0, on_change=reset_results) / 100
    years = st.number_input("Years until Maturity", value=5, on_change=reset_results)
    markup = st.number_input("Markup on Purchase (in dollars)", value=12.0, on_change=reset_results)
    withholding_tax = st.number_input("Withholding Tax (in percentage, defaults to 15%)", value=15.0, on_change=reset_results)
    
    if st.button("Calculate"):
        st.session_state['show_results'] = True

# Step 2: Results Display
if st.session_state['show_results']:
    ytm = calculate_ytm(face_value, coupon_rate, price, years)
    ytm_percentage = ytm * 100  # Convert to percentage

    total_return_absolute, total_return_annualized_absolute, total_return_percentage, total_return_annualized_percentage = calculate_total_return(face_value, price, coupon_rate, years, markup, withholding_tax)

    with st.expander("Results", expanded=True):
        # Tabular summary of data entered
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

        # Metric cards for YTM and returns
        st.subheader("Results Summary")

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("YTM", f"{ytm_percentage:.2f}%")
        with col2:
            st.metric("Total Return (Absolute)", f"${total_return_absolute:.2f}")
        with col3:
            st.metric("Total Return (Annualized)", f"${total_return_annualized_absolute:.2f}")
        with col4:
            st.metric("Percentage Return", f"{total_return_percentage:.2f}%")
        with col5:
            st.metric("Percentage Return (Annualized)", f"{total_return_annualized_percentage * 100:.2f}%")
