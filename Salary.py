import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
from employee import employee_settings
import calendar

# # Function to show employee details
# def show_employee_details():
#     # Database connection
#     conn = mysql.connector.connect(
#         host='srv1021.hstgr.io',port="3306",user='u627331871_bimodel',passwd='Bimodel@1234',db='u627331871_BI'
#     )
#     cursor = conn.cursor()
#     st.title("Employee Details")
#     cursor.execute("SELECT * FROM Employee")
#     data = cursor.fetchall()
#     df = pd.DataFrame(data, columns=['ECode', 'Gender', 'PAN_No', 'Name', 'AreaOfWork', 'Designation', 'JoinDate', 'Functions', 'Contact_No', 'SetMonthlyPay', 'SetMonthlyHours', 'Godown', 'Pay_Rs'])
#     st.write(df)

#     # Employee selection
#     employee_code = st.selectbox("Select Employee Code", df['ECode'].unique())
#     st.write(df[df['ECode'] == employee_code])

# Function to enter manual attendance
def manual_attendance_entry():
    # Database connection
    conn = mysql.connector.connect(
        host='srv1021.hstgr.io',port="3306",user='u627331871_bimodel',passwd='Bimodel@1234',db='u627331871_BI'
    )
    cursor = conn.cursor()
    st.title("Manual Attendance Entry")
    try:
        cursor.execute("SELECT ECode, Name FROM Employee")
        employees = cursor.fetchall()
        employee_dict = {f"{row[1]} ({row[0]})": row[0] for row in employees}
        
        employee = st.selectbox("Select Employee", list(employee_dict.keys()))
        selected_ecode = employee_dict[employee]
        
        date = st.date_input("Date")
        check_in_time = st.time_input("Check-In Time")
        check_out_time = st.time_input("Check-Out Time")

        # Convert times to datetime objects
        check_in_datetime = datetime.combine(date, check_in_time)
        check_out_datetime = datetime.combine(date, check_out_time)

        if st.button("Submit"):
            hours_worked = (check_out_datetime - check_in_datetime).seconds / 3600.0
            
            # Insert attendance record
            query = """
                INSERT INTO DailyAttendance (ECode, Date, CheckInTime, CheckOutTime, DailyHoursWorked) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (selected_ecode, date, check_in_time, check_out_time, hours_worked))
            conn.commit()

            # Update monthly work hours
            year = date.year
            print(year)
            month = date.month
            print(month)
            month_name = calendar.month_name[month]
            print(month_name)
            query = """
                UPDATE MonthlyWorkHours 
                SET TotalHoursWorked = TotalHoursWorked + %s 
                WHERE ECode = %s AND Pay_Month = %s AND Pay_Year = %s
            """
            cursor.execute(query, (hours_worked, selected_ecode, month_name, year))
            conn.commit()
            
            st.success("Attendance entry added successfully!")
    except mysql.connector.Error as err:
        st.error(f"Database operation error: {err}")
    finally:
        cursor.close()
        conn.close()

def fetch_attendance_data(ecode, pay_year, pay_month_number):
    # Database connection
    conn = mysql.connector.connect(
        host='srv1021.hstgr.io', port="3306", user='u627331871_bimodel', passwd='Bimodel@1234', db='u627331871_BI'
    )
    cursor = conn.cursor()

    # Fetch attendance data for the selected employee and month
    cursor.execute(f"""
        SELECT Date, DailyHoursWorked 
        FROM DailyAttendance 
        WHERE ECode='{ecode}' 
        AND YEAR(Date)='{pay_year}' 
        AND MONTH(Date)='{pay_month_number}'
    """)
    attendance_data = cursor.fetchall()

    # Closing database connection
    cursor.close()
    conn.close()

    return pd.DataFrame(attendance_data, columns=['Date', 'DailyHoursWorked'])


def show_salary_details():
    # Database connection
    conn = mysql.connector.connect(
        host='srv1021.hstgr.io', port="3306", user='u627331871_bimodel', passwd='Bimodel@1234', db='u627331871_BI'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employee")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['ECode', 'Gender', 'PAN_No', 'Name', 'AreaOfWork', 'Designation', 'JoinDate', 'Functions', 'Contact_No', 'SetMonthlyPay', 'SetMonthlyHours', 'Godown', 'Pay_Rs','Superviser'])

    employee_dict = {f"{row[3]} ({row[0]})": row[0] for row in data}
    employee = st.selectbox("Select Employee", list(employee_dict.keys()))
    selected_ecode = employee_dict[employee]

    col1, col2 = st.columns([4, 2])
    with col1:
        st.subheader("Employee Details")
        emp_info = df[df['ECode'] == selected_ecode].iloc[0]
        with st.container():
            st.subheader(f"Employee: {emp_info['Name']}")
            col3, col4 = st.columns(2)
            with col3:
                st.write(f"**Contact Number:** +{emp_info['Contact_No']}")
                st.write(f"**Area of Work:** {emp_info['AreaOfWork']}")
                st.write(f"**Designation:** {emp_info['Designation']}")
                st.write(f"**Function:** {emp_info['Functions']}")
                st.write(f"**Superviser/Contactor:** {emp_info['Superviser']}")
            with col4:
                st.write(f"**Gender:** {emp_info['Gender']}")
                st.write(f"**Godown:** {emp_info['Godown']}")
                st.write(f"**Monthly Pay:** {emp_info['SetMonthlyPay']}")
                st.write(f"**Monthly Hours:** {emp_info['SetMonthlyHours']}")
                

    with col2:
        st.subheader("Salary Details")
        pay_month = st.selectbox("Select Month", ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
        pay_year = st.selectbox("Select Year", ['2024', '2023', '2022'])

        # Fetch salary details
        query = """
            SELECT BaseSalary, OvertimePay, Deductions, NetSalary 
            FROM SalaryDetails 
            WHERE ECode = %s AND Pay_Month = %s AND Pay_Year = %s
        """
        cursor.execute(query, (selected_ecode, pay_month, pay_year))
        data = cursor.fetchone()
        
        if data:
            st.write(f"**Base Salary:** {data[0]}")
            st.write(f"**Overtime Pay:** {data[1]}")
            st.write(f"**Deductions:** {data[2]}")
            st.write(f"**Net Salary:** {data[3]}")
        else:
            st.warning("No salary details found for this employee in the selected month and year.")

    # Fetch daily attendance data for visualization
    st.subheader("Attendance Details")
    month_mapping = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    pay_month_number = month_mapping.get(pay_month)
    cursor.execute("""
        SELECT Date, DailyHoursWorked 
        FROM DailyAttendance 
        WHERE ECode = %s AND YEAR(Date) = %s AND MONTH(Date)=%s
    """, (selected_ecode, pay_year,pay_month_number))
    attendance_data = cursor.fetchall()

    if attendance_data:
        # Prepare the data for the contribution graph
        # Fetch attendance data for the selected employee
        df_contribution = fetch_attendance_data(selected_ecode, pay_year, pay_month_number)

        # Plotting the data using Plotly
        fig = px.line(df_contribution, x='Date', y='DailyHoursWorked', markers=True, title='Daily Working Hours for the Month')

        # Customize hover labels
        fig.update_traces(mode='lines+markers', hovertemplate='%{x}: %{y:.2f} hours')

        # Display Plotly chart
        st.plotly_chart(fig)

        # Closing database connection
        cursor.close()
        conn.close()
    else:
        st.info("No attendance data found for this year.")

def attendance():
    # Sidebar for navigation
    st.sidebar.title("Employee Management System")
    option = st.sidebar.selectbox("Choose an option", ["Manual Attendance Entry", "View Employee Details","Modify Employee"])

    # Navigation logic
    if option == "Manual Attendance Entry":
        manual_attendance_entry()
    elif option == "View Employee Details":
        show_salary_details()
    elif option == "Modify Employee":
        employee_settings()

# Close the database connection
# conn.close()
