import streamlit as st
import pandas as pd
import mysql.connector
import datetime

def machine_form():
    theme_plotly = None
    with open('style.css')as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    conn=mysql.connector.connect(host='srv1021.hstgr.io',port="3306",user='u627331871_bimodel',passwd='Bimodel@1234',db='u627331871_BI')
    c=conn.cursor()
    query="select * from machine_list"
    c.execute(query)
    data=c.fetchall()

    Machine_df=pd.DataFrame(data,columns=["S.No.","Name","Nomenclature","Cost","From_Address","Date_of_purchase"])
    
    Machines=["Tubular / Wire skip machine","Basket for wire twisting","Aluminium wire drawing and welding","Steel wire drawing and welding","Spooling (Aluminium)","Spooling (Steel)","Aluminium scrap box","Rod breakdown Machine (1)","Rod breakdown Machine (2)","Furnace","Others"]
    # form
    with st.form(key="Machinery_form"):
        Name=st.selectbox(label="Name of the Machine*",options=Machines)
        if Name == 'Others':
            new_name = st.text_input('Enter New Machine Name')
            if new_name:
                Name = new_name
                #append
                Machines.append(new_name)
        Nomenclature=st.text_input(label="Nomenclature of the Machine*")
        Cost=st.text_input(label="Cost of the Machine*")
        From=st.text_input(label="Purchase Address*")
        Date=st.date_input(label="Purchase Date*")
        st.markdown("**required*")

        submit_button=st.form_submit_button(label="Submit")

        if submit_button:
            if not Name or not Nomenclature or not Cost or not Date or not From :
                st.warning("Ensure all mandatory fields are filled.")
                st.stop()
            else:
                formatted_cost = "%.2f" % float(Cost)
                data=(Name,Nomenclature,formatted_cost,From,Date)
                
                query2="insert into machine_list(Name,Nomenclature,Cost,From_Address,Date_of_purchase) values(%s,%s,%s,%s,%s)"
                c.execute(query2,data)
                conn.commit()
                print(data)
    conn=mysql.connector.connect(host='srv1021.hstgr.io',port="3306",user='u627331871_bimodel',passwd='Bimodel@1234',db='u627331871_BI')
    c=conn.cursor()
    query5="select * from machine_list"
    c.execute(query5)
    data=c.fetchall()
    df=pd.DataFrame(data,columns=["S.No.","Name","Nomenclature","Cost","From_Address","Date_of_purchase"])
    st.dataframe(df)
