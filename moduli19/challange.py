import pandas as pd
import streamlit as st
import plotly.express as pt

book = pd.read_csv("bestsellers_with_categories_2022_03_27.csv")

st.title("Best Selling Books")
st.write("This is a program about...")

st.sidebar.header("Add a new book")

with st.sidebar.form("my_form"):
    new_name = st.text_input("Book Name")
    new_author = st.text_input("Author Name")
    new_user_rating = ("user rating", 0.5, 5.0, 0.0, 0.1)
    new_reviews = st.number_input("reviews", min_value=0.0, max_value=5.0, step=0.1)
    new_genre = st.text_input("Genre", book["Genre"].nunique())
    new_price = st.number_input("Price", min_value=1, step=1)
    new_year = st.number_input("Year", min_value=2009, max_value=2025)
    submitted = st.form_submit_button("Add book")

if submitted:
    new_data = {
        "Name": new_name,
        "Author": new_author,
        "User Rating": new_user_rating,
        "Reviews": new_reviews,
        "Genre": new_genre,
        "Price": new_price,
        "Year": new_year
    }
    book = pd.concat([book, pd.DataFrame(new_data, index=[0]), book], ignore_index=True)
    book.to_csv("bestsellers_with_categories_2022_03_27.csv", index=False)
    st.success("Book added successfully!")