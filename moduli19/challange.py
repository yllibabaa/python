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
    new_user_rating = st.slider("User Rating", 0.5, 5.0, 0.0, 0.1)
    new_reviews = st.number_input("Reviews", min_value=0)
    new_genre = st.text_input("Genre")
    new_price = st.number_input("Price", min_value=1, step=1)
    new_year = st.number_input("Year", min_value=2009, max_value=2025)
    submitted = st.form_submit_button(label="Add book")

    if submitted:
        new_data = {
            "Name": [new_name],
            "Author": [new_author],
            "User Rating": [new_user_rating],
            "Reviews": [new_reviews],
            "Genre": [new_genre],
            "Price": [new_price],
            "Year": [new_year]
        }
        book = pd.concat([pd.DataFrame(new_data, index=[0]), book], ignore_index=True)
        book.to_csv("bestsellers_with_categories_2022_03_27.csv", index=False)
        st.sidebar.success("Book added successfully!")

st.sidebar.header("Filter Options")
selected_author = st.sidebar.selectbox("Select Author", ["ALL"] + list(book['Author'].unique()))
selected_year = st.sidebar.selectbox("Select Year", ["ALL"] + list(book['Year'].unique()))
selected_genre = st.sidebar.selectbox("Select Genre", ["ALL"] + list(book['Genre'].unique()))
min_rating = st.sidebar.slider("Minimum User Rating", 0.5, 5.0, 0.0, 0.1)
max_price = st.sidebar.slider("Maximim Price", 0, book['Price'].max(), book['Price'].max())

filtered_book = book.copy()

if selected_author != "ALL":
    filtered_book = filtered_book[filtered_book['Author'] == selected_author]
if selected_year != "ALL":
    filtered_book = filtered_book[filtered_book['Year'] == int(selected_year)]
if selected_genre != "ALL":
    filtered_book = filtered_book[filtered_book['Genre'] == selected_genre]

filtered_book = filtered_book[
    (filtered_book['User Rating'] >= min_rating) & (filtered_book['Price'] <= max_price)
    ]

st.subheader("summary statistics")

total_books = filtered_book.shape[0]
unique_titles = filtered_book['Name'].nunique()
average_rating = filtered_book['User Rating'].mean()
average_price = filtered_book['Price'].mean()
total_reviews = filtered_book['Reviews'].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Books", total_books)
col2.metric("Unique Titles", unique_titles)
col3.metric("Average Rating", f"{average_rating:.2f}")
col4.metric("Average Price", f"${average_price:.2f}")

st.subheader("Filtered preview")
st.write(filtered_book.head())

st.subheader("Dataset preview")
st.write(filtered_books_df.head())

col1 , col2 = st.colums(2)
with col1:
    st.subheader("top 10 books titles")
    top_titles = filtered_books_df['Name'].value_counts().head(10)
    st.bar_chart(top_titles)

with col2:
    st.subheader("top 10 books authors")
    top_authors = filtered_books_df['Author'].value_counts().head(10)
    st.bar_chart(top_authors)
