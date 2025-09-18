import streamlit as st
import import pandas as pd


data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "State": ["California", "Texas", "Florida"]
}


df = pd.DataFrame(data)


st.write("Here is a table with names, ages, and states:")
st.dataframe(df)
