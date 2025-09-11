import streamlit as st

# Title
st.title("🧮 Simple Calculator")

# Input fields
num1 = st.number_input("Enter first number", format="%.2f")
num2 = st.number_input("Enter second number", format="%.2f")

# Operation selection
operation = st.selectbox("Choose operation", ["Addition", "Subtraction", "Multiplication", "Division"])

# Calculate result
if st.button("Calculate"):
    if operation == "Addition":
        result = num1 + num2
        st.success(f"Result: {result:.2f}")
    elif operation == "Subtraction":
        result = num1 - num2
        st.success(f"Result: {result:.2f}")
    elif operation == "Multiplication":
        result = num1 * num2
        st.success(f"Result: {result:.2f}")
    elif operation == "Division":
        if num2 == 0:
            st.error("❌ Cannot divide by zero.")
        else:
            result = num1 / num2
            st.success(f"Result: {result:.2f}")
