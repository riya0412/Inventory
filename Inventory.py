import streamlit as st
import pandas as pd
import mysql.connector
import datetime
import math

def conversion_module():
    theme_plotly = None
    with open('style.css')as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    # Function to calculate weight of ACSR conductor
    def calculate_acsr_weight(aluminum_weight, steel_weight):
        acsr_weight = (aluminum_weight) + (steel_weight)
        return acsr_weight

    # Function to calculate cost price of ACSR conductor
    def calculate_cost_price(machine_utility,time,labours, labor_rate, acsr_weight):
        conn=mysql.connector.connect(host='srv1021.hstgr.io', port="3306", user='u627331871_bimodel', passwd='Bimodel@1234', db='u627331871_BI')
        c=conn.cursor()
        query="select * from orders"
        c.execute(query)
        data=c.fetchall()
        order_df=pd.DataFrame(data,columns=["Order_Id","Product_Name","Type_of_order","Dealer_Name","Quantity","Unit","Rate","Amount","Labour_Associated","POC_Name","POC_Number","Date_of_order","Expected_Delivery_Date","Status"])
        aluminum_cost  = order_df[(order_df['Type_of_order'] == 'From') & (order_df['Product_Name']=='Aluminium Rod') ]['Amount'].sum()
        steel_cost  = order_df[(order_df['Type_of_order'] == 'From') & (order_df['Product_Name']=='Steel Rod') ]['Amount'].sum()
        acsr_cost = (float(aluminum_cost) * float(aluminum_weight)) + (float(steel_cost) * float(steel_weight))
        machine_utility_cost= machine_utility * time * 8.00
        labor_cost=labours * labour_rate * time
        total_cost = acsr_cost + machine_utility_cost + labor_cost
        print(machine_utility_cost)
        return total_cost

    # Streamlit UI components
    st.title("Conductor Production Cost Calculator")
    # st.title("Conductor Production Cost Calculator")
    Product=["ACSR","AAC","AAAC","Aerial Bunched Cable"]
    Product_Name=st.selectbox(label="Product Name",options=Product)
    if Product_Name=="ACSR":
        Products=["Mole","Squirrel","Weasel","Rabbit","Raccoon"]
        Product_Type=st.selectbox(label="Product Type",options=Products)
    elif Product_Name=="AAC":
        Products=["Wolf","Panther","Zebra","Moose","Gopher","Fox","Ferret"]
        Product_Type=st.selectbox(label="Product Type",options=Products)
    elif Product_Name=="AAAC":
        Products=["Mink","Beaver","Otter","Cat"]
        Product_Type=st.selectbox(label="Product Type",options=Products)
    elif Product_Name=="Aerial Bunched Cable":
        Products=["Tiger","Lion","Goat","Deer"]
        Product_Type=st.selectbox(label="Product Type",options=Products)
    
    aluminum_weight = st.number_input("Enter Weight of Aluminum (in kg):", min_value=0)
    steel_weight = st.number_input("Enter Weight of Steel Wire (in kg):", min_value=0)
    Labours=st.number_input("Number of Labours")
    # aluminum_cost = st.number_input("Enter Cost of Aluminum (per kg):", min_value=0.0, step=0.01)
    # steel_cost = st.number_input("Enter Cost of Steel (per kg):", min_value=0.0, step=0.01)
    time_perKG=0.5
    machine_utility_perhour = 100
    conn=mysql.connector.connect(host='srv1021.hstgr.io', port="3306", user='u627331871_bimodel', passwd='Bimodel@1234', db='u627331871_BI')
    c=conn.cursor()
    query="select * from labour"
    c.execute(query)
    data=c.fetchall()
    labour_rate=100

    if st.button("Calculate"):
        acsr_weight = calculate_acsr_weight(aluminum_weight, steel_weight)
        total_cost = calculate_cost_price( machine_utility_perhour,time_perKG,Labours, labour_rate, acsr_weight)
        conn=mysql.connector.connect(host='kuber.mysql.database.azure.com',port="3306",user='kuber',passwd='Pars@0412',db='kuberinventory')
        c=conn.cursor()
        query="select * from Inventry_Module"
        c.execute(query)
        data=c.fetchall()   
        df=pd.DataFrame(data,columns=["S_No","Product_Name","Quantity","Unit","Last_updated","By_whom"]) 
        st.write("Weight of Conductor:", acsr_weight, "kg")
        st.write("Total Production Cost:", total_cost)
        new_quantity_al=float(df[df["Product_Name"]=="Aluminium Rod"]["Quantity"].values)-float(aluminum_weight)
        new_quantity_steel=float(df[df["Product_Name"]=="Steel Rod"]["Quantity"].values)-float(steel_weight)        
        conn=mysql.connector.connect(host='localhost',port="3306",user='root',passwd='Pars@0412',db='Kuber')
        c=conn.cursor()
        query="update Inventry_Module set Quantity = %s, Unit= %s where Product_Name=%s"
        c.execute(query,(acsr_weight,"Kg",Product_Name))
        conn.commit()
        query="update Inventry_Module set Quantity = %s, Unit= %s where Product_Name=%s"
        c.execute(query,(new_quantity_al,"Kg","Aluminium Rod"))
        conn.commit()
        query="update Inventry_Module set Quantity = %s, Unit= %s where Product_Name=%s"
        c.execute(query,(new_quantity_steel,"Kg","Steel Rod"))
        conn.commit()
        query="select* from Inventry_Module"
        c.execute(query)
        data=c.fetchall()
        df=pd.DataFrame(data,columns=["S_No","Product_Name","Quantity","Unit","Last_updated","By_whom"]) 
        st.dataframe(df)
        # df.loc[df['Product_Name'] == 'ACSR', 'Quantity'] += acsr_weight

