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

# Session state setup to manage section visibility
if 'show_results' not in st.session_state:
    st.session_state['show_results'] = False

# Reset function
def reset_results():
    st.session_state['show_results'] = False
    st.session_state['price'] = 1000.0
    st.session_state['face_value'] = 1000.0
    st.session_state['coupon_rate'] = 5.0
    st.session_state['years'] = 5
    st.session_state['markup'] = 12.0
    st.session_state['withholding_tax'] = 15.0

# Function to show results after calculation
def show_results():
    st.session_state['show_results'] = True

# Step 1: Data Entry Section (only shown if results are not displayed)
if not st.session_state['show_results']:
    with st.form("data_entry"):
        st.session_state['price'] = st.number_input("Current Price of the Bond", value=st.session_state.get('price', 1000.0))
        st.session_state['face_value'] = st.number_input("Face Value of the Bond", value=st.session_state.get('face_value', 1000.0))
        st.session_state['coupon_rate'] = st.number_input("Annual Interest Rate (Coupon Rate) as a percentage", value=st.session_state.get('coupon_rate', 5.0)) / 100
        st.session_state['years'] = st.number_input("Years until Maturity", value=st.session_state.get('years', 5))
        st.session_state['markup'] = st.number_input("Markup on Purchase (in dollars)", value=st.session_state.get('markup', 12.0))
        st.session_state['withholding_tax'] = st.number_input("Withholding Tax (in percentage, defaults to 15%)", value=st.session_state.get('withholding_tax', 15.0))

        # Create the Calculate button
        calculate_button = st.form_submit_button("Calculate")
        
        # On button click, calculate the results and show the results section
        if calculate_button:
            show_results()

# Step 2: Results Section (only shown after Calculate button is clicked)
if st.session_state['show_results']:
    # Retrieve values from session state
    price = st.session_state['price']
    face_value = st.session_state['face_value']
    coupon_rate = st.session_state['coupon_rate']
    years = st.session_state['years']
    markup = st.session_state['markup']
    withholding_tax = st.session_state['withholding_tax']
    
    # Perform calculations
    ytm = calculate_ytm(face_value, coupon_rate, price, years)
    ytm_percentage = ytm * 100  # Convert to percentage

    total_return_absolute, total_return_annualized_absolute, total_return_percentage, total_return_annualized_percentage = calculate_total_return(face_value, price, coupon_rate, years, markup, withholding_tax)

    st.write("### Results Summary")

    # Tabular summary of data entered
    st.write("#### Summary of Data Entered")
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

    # Button to reset and go back to data entry
    if st.button("Reset and Enter New Data"):
        reset_results()
