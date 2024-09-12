import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error
import bcrypt
from datetime import datetime
import calendar

# Define database connection parameters
DB_PARAMS = {
    'host': 'srv1021.hstgr.io',
    'port': "3306",
    'user': 'u627331871_bimodel',
    'password': 'Bimodel@1234',
    'database': 'u627331871_BI'
}

def get_employees():
    try:
        connection = mysql.connector.connect(**DB_PARAMS)
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Employee")
            employees = cursor.fetchall()
            return employees
    except Error as e:
        st.error(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def update_employee(ecode, gender, pan_no, name, area_of_work, designation, join_date, functions, contact_no, monthly_pay, monthly_hours, godown, pay_rs):
    try:
        connection = mysql.connector.connect(**DB_PARAMS)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE Employee
                SET Gender = %s, PAN_No = %s, Name = %s, AreaOfWork = %s, Designation = %s, 
                    JoinDate = %s, Functions = %s, Contact_No = %s, SetMonthlyPay = %s, 
                    SetMonthlyHours = %s, Godown = %s, Pay_Rs = %s
                WHERE ECode = %s
            """, (gender, pan_no, name, area_of_work, designation, join_date, functions, contact_no, monthly_pay, monthly_hours, godown, pay_rs, ecode))
            connection.commit()
            st.success("Employee updated successfully!")
    except Error as e:
        st.error(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def delete_employee(ecode):
    try:
        connection = mysql.connector.connect(**DB_PARAMS)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Employee WHERE ECode = %s", (ecode,))
            connection.commit()
            st.success("Employee deleted successfully!")
    except Error as e:
        st.error(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def add_employee(gender, pan_no, name, area_of_work, designation, join_date, functions, contact_no, monthly_pay, monthly_hours, godown, pay_rs):
    try:
        connection = mysql.connector.connect(**DB_PARAMS)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO Employee (Gender, PAN_No, Name, AreaOfWork, Designation, JoinDate, Functions, Contact_No, SetMonthlyPay, SetMonthlyHours, Godown, Pay_Rs)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (gender, pan_no, name, area_of_work, designation, join_date, functions, contact_no, monthly_pay, monthly_hours, godown, pay_rs))
            connection.commit()
            st.success("Employee added successfully!")
            # Clear session state
            st.session_state["new_gender"] = ""
            st.session_state["new_pan_no"] = ""
            st.session_state["new_name"] = ""
            st.session_state["new_area_of_work"] = ""
            st.session_state["new_designation"] = ""
            st.session_state["new_join_date"] = datetime.today().date()
            st.session_state["new_functions"] = ""
            st.session_state["new_contact_no"] = ""
            st.session_state["new_monthly_pay"] = 0.0
            st.session_state["new_monthly_hours"] = 0
            st.session_state["new_godown"] = ""
            st.session_state["new_pay_rs"] = 0.0
    except Error as e:
        st.error(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def employee_settings():
    if "new_gender" not in st.session_state:
        st.session_state["new_gender"] = ""
    if "new_pan_no" not in st.session_state:
        st.session_state["new_pan_no"] = ""
    if "new_name" not in st.session_state:
        st.session_state["new_name"] = ""
    if "new_area_of_work" not in st.session_state:
        st.session_state["new_area_of_work"] = ""
    if "new_designation" not in st.session_state:
        st.session_state["new_designation"] = ""
    if "new_join_date" not in st.session_state:
        st.session_state["new_join_date"] = datetime.today().date()
    if "new_functions" not in st.session_state:
        st.session_state["new_functions"] = ""
    if "new_contact_no" not in st.session_state:
        st.session_state["new_contact_no"] = ""
    if "new_monthly_pay" not in st.session_state:
        st.session_state["new_monthly_pay"] = 0.0
    if "new_monthly_hours" not in st.session_state:
        st.session_state["new_monthly_hours"] = 0
    if "new_godown" not in st.session_state:
        st.session_state["new_godown"] = ""
    if "new_pay_rs" not in st.session_state:
        st.session_state["new_pay_rs"] = 0.0

    st.header("Employee Management")
    st.write("Manage employee records.")

    employees = get_employees()
    if employees:
        for emp in employees:
            with st.expander(f"ECode: {emp['ECode']} - {emp['Name']}"):
                new_gender = st.selectbox("Gender", ["Male", "Female"], index=["Male", "Female"].index(emp['Gender']), key=f"gender_{emp['ECode']}")
                new_pan_no = st.text_input("PAN No", value=emp['PAN_No'], key=f"pan_no_{emp['ECode']}")
                new_name = st.text_input("Name", value=emp['Name'], key=f"name_{emp['ECode']}")
                new_area_of_work = st.text_input("Area of Work", value=emp['AreaOfWork'], key=f"area_of_work_{emp['ECode']}")
                new_designation = st.text_input("Designation", value=emp['Designation'], key=f"designation_{emp['ECode']}")
                new_join_date = st.date_input("Join Date", value=emp['JoinDate'], key=f"join_date_{emp['ECode']}")
                new_functions = st.text_area("Functions", value=emp['Functions'], key=f"functions_{emp['ECode']}")
                new_contact_no = st.text_input("Contact No", value=emp['Contact_No'], key=f"contact_no_{emp['ECode']}")
                
                # Ensure min_value, max_value, and step are defined
                min_value = 0.0
                max_value = None
                step = 0.01
                
                new_monthly_pay = st.number_input("Monthly Pay", value=float(emp['SetMonthlyPay']), format="%.2f", min_value=min_value, max_value=max_value, step=step, key=f"monthly_pay_{emp['ECode']}")
                new_monthly_hours = st.number_input("Monthly Hours", value=int(emp['SetMonthlyHours']), min_value=0, key=f"monthly_hours_{emp['ECode']}")
                new_godown = st.text_input("Godown", value=emp['Godown'], key=f"godown_{emp['ECode']}")
                new_pay_rs = st.number_input("Pay Rs", value=float(emp['Pay_Rs']), format="%.2f", min_value=min_value, max_value=max_value, step=step, key=f"pay_rs_{emp['ECode']}")

                if st.button(f"Update Employee {emp['ECode']}", key=f"update_employee_{emp['ECode']}"):
                    update_employee(emp['ECode'], new_gender, new_pan_no, new_name, new_area_of_work, new_designation, new_join_date, new_functions, new_contact_no, new_monthly_pay, new_monthly_hours, new_godown, new_pay_rs)
                if st.button(f"Delete Employee {emp['ECode']}", key=f"delete_employee_{emp['ECode']}"):
                    delete_employee(emp['ECode'])

    st.subheader("Add New Employee")
    new_gender = st.selectbox("Gender", ["Male", "Female"], key="new_gender")
    new_pan_no = st.text_input("PAN No", key="new_pan_no")
    new_name = st.text_input("Name", key="new_name")
    new_area_of_work = st.text_input("Area of Work", key="new_area_of_work")
    new_designation = st.text_input("Designation", key="new_designation")
    new_join_date = st.date_input("Join Date", key="new_join_date")
    new_functions = st.text_area("Functions", key="new_functions")
    new_contact_no = st.text_input("Contact No", key="new_contact_no")
    
    # Ensure min_value, max_value, and step are defined
    min_value = 0.0
    max_value = None
    step = 0.01
    
    new_monthly_pay = st.number_input("Monthly Pay", value=0.0, format="%.2f", min_value=min_value, max_value=max_value, step=step, key="new_monthly_pay")
    new_monthly_hours = st.number_input("Monthly Hours", value=0, min_value=0, key="new_monthly_hours")
    new_godown = st.text_input("Godown", key="new_godown")
    new_pay_rs = st.number_input("Pay Rs", value=0.0, format="%.2f", min_value=min_value, max_value=max_value, step=step, key="new_pay_rs")

    if st.button("Add Employee", key="add_employee"):
        add_employee(new_gender, new_pan_no, new_name, new_area_of_work, new_designation, new_join_date, new_functions, new_contact_no, new_monthly_pay, new_monthly_hours, new_godown, new_pay_rs)
