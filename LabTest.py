import streamlit as st
import mysql.connector
import pandas as pd

# MySQL connection details
def get_connection():
    return mysql.connector.connect(
        host="localhost",  # Ensure this is the correct host
        user="root",  # Replace with your MySQL username
        password="Pars@0412",  # Replace with your MySQL password
        database="Kuber_Inventory"  # Replace with your MySQL database name
    )

# Function to fetch data from MySQL
def fetch_data(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(data, columns=columns)

# Streamlit app
st.title("MySQL to Excel Exporter")

query = st.text_area("Enter your SQL query", "SELECT * FROM loading")

if st.button("Fetch Data"):
    data = fetch_data(query)
    st.write(data)

    if not data.empty:
        # Convert DataFrame to Excel
        excel_file = "Loading.xlsx"
        data.to_excel(excel_file, index=False, engine='xlsxwriter')

        # Provide download link
        with open(excel_file, "rb") as file:
            btn = st.download_button(
                label="Download Excel",
                data=file,
                file_name=excel_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
