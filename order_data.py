import streamlit as st
import pandas as pd
import mysql.connector
import datetime

def order_data():
    theme_plotly = None
    with open('style.css')as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    conn=mysql.connector.connect(host='kuber.mysql.database.azure.com',port="3306",user='kuber',passwd='Pars@0412',db='kuberinventory')
    c=conn.cursor()
    query="select * from orders"
    c.execute(query)
    data=c.fetchall()
    

    order_df=pd.DataFrame(data,columns=["Order_Id","Product_Name","Product_Type","Type_of_order","Dealer_Name","Quantity","Unit","Rate","Amount","Labour_Associated","POC_Name","POC_Number","Date_of_order","Expected_Delivery_Date","Status"])
    # ProductName=st.sidebar.multiselect(
    #         "SELECT PRODUCT Name",
    #         options=order_df["Product_Name"].unique(),
    #         default=order_df["Product_Name"].unique(),
    #         )
    # ProductType=st.sidebar.multiselect(
    #         "SELECT PRODUCT Type",
    #         options=order_df["Product_Type"].unique(),
    #         default=order_df["Product_Type"].unique(),
    #         )
    # OrderStatus=st.sidebar.multiselect(
    #         "SELECT Status",
    #         options=order_df["Status"].unique(),
    #         default=order_df["Status"].unique(),
    #         )
    # df_selection=order_df.query(
    #     "Product_Name==@ProductName & Product_Type==@ProductType & Status==@OrderStatus"
    #     )
    option1=["From","To"]
    option2=["Kg","Km"]
    Labour=["Labour1","Labour2","Labour3","Labour4","Labour5","Labour6","Others"]

    # form
    Product=["AAC","ACSR","Wire","Insulator","Structural Components","AAAC","Aerial Bunched Cable","Aluminium Scrap"]
    Name=st.selectbox(label="Product Name*",options=Product)
    if Name=="ACSR":
        Products=["Mole","Squirrel","Weasel","Rabbit","Raccoon"]
        Type=st.selectbox(label="Product Type",options=Products)
    elif Name=="AAC":
        Products=["Wolf","Panther","Zebra","Moose","Gopher","Fox","Ferret"]
        Type=st.selectbox(label="Product Type",options=Products)
    elif Name=="AAAC":
        Products=["Mink","Beaver","Otter","Cat"]
        Type=st.selectbox(label="Product Type",options=Products)
    elif Name=="Aerial Bunched Cable":
        Products=["Tiger","Lion","Goat","Deer"]
        Type=st.selectbox(label="Product Type",options=Products)
    elif Name=="Wire":
        Products=["Stay Wires","Earthing wire","Aluminium wire","Steel wire"]
        Type=st.selectbox(label="Product Type",options=Products)
    elif Name=="Insulator":
        Products=["Polymer Insulator","Porcelain insulator","Glass Insulator"]
        Type=st.selectbox(label="Product Type",options=Products)
    elif Name=="Structural Components":
        Products=["Jumper Cable","Earthing rod","Stay elbow","Stay Rod"]
        Type=st.selectbox(label="Product Type",options=Products)
    elif Name=="Aluminium Scrap":
        Products=["Aluminium Scrap"]
        Type=st.selectbox(label="Product Type",options=Products)
    Address=st.selectbox(label="Type of order (TO/FROM)*",options=option1)
    Party=["MARUTI ENTERPRISES","SHREE SHYAM ENTERPRISES",
"NAMAN INTERNATIONALv/ RYAN",
"D&M CABLES",
"KRISHNA ENTERPRISES",
"PMHSR TRANSFORMERS & CONDUCTORS PVT. LTD.",
"POWER SAHAJ",
"NARMADA METAL",
"ELECON CONDUCTORS LTD.",
"JAIPURIA BROTHERS ELECTRICALS PVT. LTD.",
"LAXMI WIRE INDUSTRIES",
"SHANTAVEER ELECTRICAL ENGG. CO.",
"SRI PADMAWATI METALS",
"GUPTA IMPEX",
"REKHA INDUSTRIES",
"JM CABLE AND CONDUCTORS",
"RASS HEAVY ELECTRICALS PVT LTD",
"ANGOORI METALS"
"LAXMI WIRE INDUSTRIES",
"RKS STEEL INDUSTRIES PVT LTD",
"TAPODHANI METALS AND ALLOYS",
"SHREE PUSHKAR WIRES",
"KAMYA ENTERPRISES PVT. LTD.",
"MAHAVIR TRANSMISSION LIMITED",
"JAIPURIA BROTHERS ELECTRICALS PVT. LTD.",
"SAN ELECTRICALS",
"DEEPAK TRADING COMPANY",
"SRI PADMAWATI METALS",
"SAKAMBHARI ENTERPRISES",
"SHREE NATH METAL WORKS",
"JAI AMBAY ELECTRICALS",
"NARMADA INFRATECH AND VIDHYUT PRODUCTS PVT. LTD.",
"TECHNO FIBRE INDUSTRIES",
"MAAN ALUMINIUM LTD.",
"ARHAM INDUSTRIES",
"SUMRIDHI ALUMINIUM PVT. LTD.",
"A.S WIRE INDUSTRIES",
"SR ENTERPRISES",
"PUSHPANJALI ENTERPRISES PVT LTD",
"RAJ ENTERPRISES",
"PRAGATI ENTERPRISES",
"MAHESHWARI ELECTRICALS",
"GLOBAL METAL TECH"
"R.L. JAIN & SONS",
"STAR BANGLES",
"G.S TRADING COMPANY",
"JAIPURIA BROTHERS",
"BHALLA ENGINEERS",
"RAKMAN INDUSTRIES LTD",
"PARMESHWAR WIRE PRODUCTS",
"RISHAB POWER CONTROLS"
,"INDIAN QUALIY PRODUCRTS CO","MANSA TRADING CO"]
    Person=st.selectbox(label="Name of the client/vender*",options=Party)
    Quantity=st.text_input(label="Quantity(Kg/Km)*")
    Unit=st.selectbox(label="Kg/Km*",options=option2)
    Rate=st.text_input(label="Rate*")
    Labour_Associated=st.multiselect("Labours Associated",options=Labour)
    if Labour_Associated == 'Others':
        new_Labour = st.text_input('Enter New Labour')
        if new_Labour:
            Labour_Associated = new_Labour
            Labour.append(new_Labour)
    POC_Name=st.text_input(label="Name of POC")
    POC_Number=st.text_input(label="Number of POC")
    Date=st.date_input(label="Order Date*")
    Delivery_Date=st.date_input(label="Expected Delivery Date*")
    st.markdown("**required*")

        # submit_button=st.form_submit_button(label="Submit")

    if st.button("Submit"):
        if not Address or not Name or not Type or not Person or not Quantity or not Date or not Unit or not Rate or not Labour_Associated or not Delivery_Date:
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()
        else:
            # new_data= pd.DataFrame(
            #     [
            #         {
            #             "Type_of_order": Address,
            #             "Person": Person,
            #             "Quantity":Quantity,
            #             "Unit":Unit,
            #             "Rate":Rate,
            #             "Labour_Associated":", ".join(Labour_Associated),
            #             "POC_Name":POC_Name,
            #             "POC_Number":POC_Number,
            #             "Date_of_order":Date.strftime("%d/%m/%Y"),
            #         }
            #     ]
            # )
            formatted_quantity = "%.2f" % float(Quantity)
            formatted_rate = "%.2f" % float(Rate)
            amount=float(Quantity)*float(Rate)
            formatted_amount="%.2f" % float(amount)
            data=(Name,Type,Address,Person,formatted_quantity,Unit,formatted_rate,formatted_amount,", ".join(Labour_Associated),POC_Name,POC_Number,Date.strftime("%Y-%m-%d"),Delivery_Date.strftime("%Y-%m-%d"))
            if Address=="To":
                present_quantity=order_df[order_df["Product_Name"]==Name]["Quantity"].sum()
                if (float(present_quantity)<float(formatted_quantity)):
                    st.warning("Entered Quantity is more then the presen quantity")
                    # st.stop()
                else:
                    query2="insert into orders(Product_Name,Product_Type,Type_of_order,Dealer_Name,Quantity,Unit,Rate,Amount,Labour_Associated,POC_Name,POC_Number,Order_Date,Expected_delivery_date) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    c.execute(query2,data)
                    conn.commit()
                    last_order_id = c.lastrowid
                    Expected_Delivery_Date=Delivery_Date.strftime("%Y-%m-%d")
                    query3="insert into orders_tracking(Order_id,Product_Name,Expected_Delivery_Date) values(%s,%s,%s)"
                    c.execute(query3,(last_order_id,Name,Expected_Delivery_Date))
                    conn.commit()
                    print(data)
            else:
                query2="insert into orders(Product_Name,Product_Type,Type_of_order,Dealer_Name,Quantity,Unit,Rate,Amount,Labour_Associated,POC_Name,POC_Number,Order_Date,Expected_delivery_date) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                c.execute(query2,data)
                conn.commit()
                last_order_id = c.lastrowid
                Expected_Delivery_Date=Delivery_Date.strftime("%Y-%m-%d")
                query3="insert into orders_tracking(Order_id,Product_Name,Expected_Delivery_Date) values(%s,%s,%s)"
                c.execute(query3,(last_order_id,Name,Expected_Delivery_Date))
                conn.commit()
                print(data)
    conn=mysql.connector.connect(host='kuber.mysql.database.azure.com',port="3306",user='kuber',passwd='Pars@0412',db='kuberinventory')
    c=conn.cursor()
    query5="select * from orders"
    c.execute(query5)
    data=c.fetchall()
    order_df=pd.DataFrame(data,columns=["Order_Id","Product_Name","Product_Type","Type_of_order","Dealer_Name","Quantity","Unit","Rate","Amount","Labour_Associated","POC_Name","POC_Number","Date_of_order","Expected_Delivery_Date","Status"])
    ProductName=st.sidebar.multiselect(
            "SELECT PRODUCT Name",
            options=order_df["Product_Name"].unique(),
            default=order_df["Product_Name"].unique(),
            )
    ProductType=st.sidebar.multiselect(
            "SELECT PRODUCT Type",
            options=order_df["Product_Type"].unique(),
            default=order_df["Product_Type"].unique(),
            )
    OrderStatus=st.sidebar.multiselect(
            "SELECT Status",
            options=order_df["Status"].unique(),
            default=order_df["Status"].unique(),
            )
    df_selection=order_df.query(
        "Product_Name==@ProductName & Product_Type==@ProductType & Status==@OrderStatus"
        )
    showData=st.multiselect('Filter: ',df_selection.columns,default=["Order_Id","Product_Name","Product_Type","Type_of_order","Dealer_Name","Quantity","Unit","Rate","Amount","Labour_Associated","POC_Name","POC_Number","Date_of_order","Expected_Delivery_Date","Status"])
    st.dataframe(df_selection[showData],use_container_width=True)
    # df=pd.DataFrame(data,columns=["Order_id","Product_Name","Type_of_order","Dealer_Name","Quantity","Unit","Rate","Amount","Labour_Associated","POC_Name","POC_Number","Date_of_order","Expected_Delivery_Date","Status"])
    # st.dataframe(df)
    total_order=df_selection["Order_Id"].count()
    cost_price = df_selection[df_selection['Type_of_order'] == 'From']['Amount'].sum()
    selling_price = df_selection[df_selection['Type_of_order'] == 'To']['Amount'].sum()
    Purchased_Quantity=df_selection[df_selection['Type_of_order'] == 'From']['Quantity'].sum()
    Sold_Quantity=df_selection[df_selection['Type_of_order'] == 'To']['Quantity'].sum()
    Purchased_Rate=df_selection[df_selection['Type_of_order'] == 'From']['Rate'].sum()
    Sold_Rate=df_selection[df_selection['Type_of_order'] == 'To']['Rate'].sum()
    profit_per_unit = Sold_Rate - Purchased_Rate
    Overall_profit=(Sold_Quantity*Sold_Rate)-(Sold_Quantity*Purchased_Rate)
    
    total0,total1,total2,total3,total4=st.columns(5,gap='small')
    with total0:
        st.info("Total Orders",icon="💰")
        st.metric(label="Total Order",value=f"{total_order:,.0f}")
    with total1:
        st.info('Total Purchased Quantity',icon="💰")
        st.metric(label="Total Purchased Quantity",value=f"{Purchased_Quantity:,.0f}")
    with total2:
        st.info('Total Sold Quantity',icon="💰")
        st.metric(label="Total Sold Quantity",value=f"{Sold_Quantity:,.0f}")
    with total3:
        st.info('Profit per Unit',icon="💰")
        st.metric(label="Profit per Unit",value=f"{profit_per_unit:,.0f}")
    with total4:
        st.info('Overall Profit',icon="💰")
        st.metric(label="Overall Profit",value=f"{Overall_profit:,.0f}")

def order_status(name):
    def update_order_status(order_id,Name, status):
        conn=mysql.connector.connect(host='kuber.mysql.database.azure.com',port="3306",user='kuber',passwd='Pars@0412',db='kuberinventory')
        c=conn.cursor()
        query = "UPDATE orders_tracking SET Status = %s, By_whom = %s , Updation_date =%s WHERE Order_id = %s"
        query2= "UPDATE orders SET Status=%s WHERE order_id= %s"
        updated_at = datetime.date.today()  # Get current date
        c.execute(query, (status,Name,updated_at, order_id))
        conn.commit()
        c.execute(query2,(status, order_id))
        conn.commit()
    st.header("Update Tracking")
    order_id = st.number_input("Enter Order ID:",min_value=1)
    Name=name
    # loaded = st.checkbox("Loaded by sender")
    # out_for_delivery = st.checkbox("Out for delivery")
    # delivered = st.checkbox("Delivered")
    status=st.radio("Status",options=["Loaded by sender","Out for delivery","Delivered"])

    if st.button("Update Order Status"):
        if status=="Loaded by sender":
            update_order_status(order_id,Name, "Loaded")
        elif status=="Out for delivery":
            update_order_status(order_id,Name, "Out for delivery")
        elif status=="Delivered":
            update_order_status(order_id,Name, "Delivered")
            conn=mysql.connector.connect(host='kuber.mysql.database.azure.com',port="3306",user='kuber',passwd='Pars@0412',db='kuberinventory')
            c=conn.cursor()
            query = "select * from orders where order_id=%s"
            c.execute(query,(order_id,))
            Order_Type=c.fetchall()
            orderr=pd.DataFrame(Order_Type,columns=["Order_Id","Product_Name","Product_Type","Type_of_order","Dealer_Name","Quantity","Unit","Rate","Amount","Labour_Associated","POC_Name","POC_Number","Date_of_order","Expected_Delivery_Date","Status"])
            Inventry=pd.read_excel('Inventory.xlsx')
            nested_products=pd.read_excel('Nested_Products.xlsx')
            Product_Name=orderr["Product_Name"]
            Quantity=orderr["Quantity"]
            Product_Type=orderr["Product_Type"]
            if (orderr["Type_of_order"]=="To").any():
                Inventry.loc[Inventry['ProductName'].values == Product_Name.values, 'Quantity(KGS/MTS)'] -= Quantity
                nested_products.loc[nested_products['ProductTypes'].values == Product_Type.values, 'Quantity(KGS/MTS)'] -= Quantity
            elif (orderr["Type_of_order"]=="From").any():
                Inventry.loc[Inventry['ProductName'].values == Product_Name.values, 'Quantity(KGS/MTS)'] += Quantity
                nested_products.loc[nested_products['ProductTypes'].values == Product_Type.values, 'Quantity(KGS/MTS)'] += Quantity
            Inventry.to_excel('Inventory.xlsx', index=False)
            nested_products.to_excel('Nested_Products.xlsx', index=False)


        st.success("Order status updated successfully!")
    conn=mysql.connector.connect(host='kuber.mysql.database.azure.com',port="3306",user='kuber',passwd='Pars@0412',db='kuberinventory')
    c=conn.cursor()
    query4="select * from orders_tracking"
    c.execute(query4)
    data=c.fetchall()
    df=pd.DataFrame(data,columns=["Order_id","Product_Name","Expected_Delivery_Date","Status","Updation_Date","By_whom"])
    OrderStatus=st.sidebar.multiselect(
            "SELECT Status",
            options=df["Status"].unique(),
            default=df["Status"].unique(),
            )
    bywhom=st.sidebar.multiselect(
            "SELECT By Whom",
            options=df["By_whom"].unique(),
            default=df["By_whom"].unique(),
            )
    df_selection=df.query(
        "Status==@OrderStatus & By_whom==@bywhom"
        )
    showData=st.multiselect('Filter: ',df_selection.columns,default=["Order_id","Product_Name","Expected_Delivery_Date","Status","Updation_Date","By_whom"])
    st.dataframe(df_selection[showData],use_container_width=True)





