import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import time
import pickle
from order_data import *
from Machinery import *
from Inventory import *
from Calculators import *
from pathlib import Path
import streamlit_authenticator as stauth
from streamlit_extras.metric_cards import style_metric_cards
st.set_option('deprecation.showPyplotGlobalUse', False)
import plotly.graph_objs as go
import mysql.connector
import math
import yaml
import yaml
from yaml.loader import SafeLoader


st.set_page_config(page_title="Kuber Enterprises",page_icon="🌍",layout="wide")
# st.header("ANALYTICAL PROCESSING, KPI, TRENDS & PREDICTIONS")

# User Authentication
with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_minutes'],
    config['pre-authorized']
)

authenticator.login()

if st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')

elif st.session_state["authentication_status"]:
    # authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
    person_name=st.session_state["name"]
    # st.title('Some content')
    #all graphs we use custom css not streamlit 
    theme_plotly = None

    # load Style css
    with open('style.css')as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

    #uncomment these two lines if you fetch data from mysql
    # result = view_all_data()
    # df=pd.DataFrame(result,columns=["Policy","Expiry","Location","State","Region","Investment","Construction","BusinessType","Earthquake","Flood","Rating","id"])

    conn=mysql.connector.connect(host='kuber.mysql.database.azure.com',port="3306",user='kuber',passwd='Pars@0412',db='kuberinventory')
    c=conn.cursor()
    query="select * from client_list"
    c.execute(query)
    data=c.fetchall()

    df=pd.DataFrame(data,columns=["id","PartyNumber","GSTIN","PartyGrade","TimeGuaranteeforCredit","LastCreditCycle","CreditDue","AnyGuaranteeParty","PurchaseSaleBoth","MajorProductsDealtIn","HSNCode","ManufacturedAlso","ManufacturedRates","POCName","POCContactInfo","LastTradedValuesWithProducts","LastMeeting","AddressWork"])
    
    #load excel file | comment this line when  you fetch data from mysql
    # Inventry=pd.read_excel('To work on - Data Analysis.xlsx', sheet_name='Inventory')
    # nested_products=pd.read_excel('To work on - Data Analysis.xlsx', sheet_name='Nested Products')



    #this function performs basic descriptive analytics like Mean,Mode,Sum  etc
    def Home():
        #side bar logo
        # st.sidebar.image("data/Kuber_logo.jpeg",caption="")
        Inventry=pd.read_excel('To work on - Data Analysis.xlsx', sheet_name='Inventory')
        nested_products=pd.read_excel('To work on - Data Analysis.xlsx', sheet_name='Nested Products')
        conn=mysql.connector.connect(host='kuber.mysql.database.azure.com',port="3306",user='kuber',passwd='Pars@0412',db='kuberinventory')
        c=conn.cursor()
        query5="select * from orders_tracking"
        c.execute(query5)
        data1=c.fetchall()
        orders=pd.DataFrame(data1, columns=["Order_id","Product_Name","Expected_Delivery_Date","Status","Updation_Date","By_whom"])

        #switcher
        ProductGrade=st.sidebar.multiselect(
            "SELECT PRODUCT GRADE",
            options=Inventry["ProductGrade"].unique(),
            default=Inventry["ProductGrade"].unique(),
            )
        StockLess=st.sidebar.multiselect(
            "SELECT STOCK STATUS",
            options=Inventry["Stockless"].unique(),
            default=Inventry["Stockless"].unique(),
            )
        Godown=st.sidebar.multiselect(
        "SELECT Godown",
        options=Inventry["Godown"].unique(),
        default=Inventry["Godown"].unique(),
        )
        df_selection=Inventry.query(
        "ProductGrade==@ProductGrade & Stockless==@StockLess & Godown ==@Godown"
        )
        # df_selection1=nested_products.query()
        with st.expander("VIEW EXCEL DATASET"):
            showData=st.multiselect('Filter: ',df_selection.columns,default=["S.No.","Product","ProductName","ProductGrade","Quantity(KGS/MTS)","StockCheckedon?","Stockless","Godown","Fromvendor(optional)"])
            st.dataframe(df_selection[showData],use_container_width=True)
            # merged_df = pd.merge(inventory_df, nested_products_df, left_on='S.No.', right_on='inventory ID', how='inner')
        #compute top analytics
        total_quantity = df_selection['Quantity(KGS/MTS)'].sum()
        total_product= df_selection['Product'].count()
        # CreditDue_median= float(pd.Series(df_selection['CreditDue']).median()) 
        # rating = float(pd.Series(df_selection['Rating']).sum())
        total_nested_product=nested_products['ProductTypes'].count()
        pending_orders=orders[orders["Status"]!="Delivered"]["Status"].count()


        total1,total2,total3,total4=st.columns(4,gap='small')
        with total1:
            st.info('Total Quantity',icon="💰")
            st.metric(label="Total Quantity",value=f"{total_quantity:,.0f}")


        with total2:
            st.info('Total Product',icon="💰")
            st.metric(label="Total Product",value=f"{total_product:,.0f}")
        
        with total3:
            st.info('Total Product Type',icon="💰")
            st.metric(label="Total Product Type",value=f"{total_nested_product:,.0f}")
        
        with total4:
            st.info('Total Pending Orders',icon="💰")
            st.metric(label="Total Pending Orders",value=f"{pending_orders:,.0f}")

        # power_bi_embed_code = """<iframe title="Inventry Dashboard" width="1140" height="541.25" src="https://app.powerbi.com/reportEmbed?reportId=08d20a68-0292-4f91-bb4e-e7442dfa4d7e&autoAuth=true&ctid=e97bc3a3-8b62-4fc6-a6d9-f9f3f07f3c12" frameborder="0" allowFullScreen="true"></iframe>" frameborder="0" allowFullScreen="true"></iframe>
    # """

        # Display the embedded Power BI report using st.write
        # st.write(power_bi_embed_code, unsafe_allow_html=True)

        st.subheader("Line Graph")
        fig = px.line(df, x='PartyNumber', y='CreditDue', title='Value Over Time')
        st.plotly_chart(fig)
        st.subheader("Pie Chart")
        purchase_only = df[df['PurchaseSaleBoth'] == 'Purchase']
        sale_only = df[df['PurchaseSaleBoth'] == 'Sale']
        both = df[df['PurchaseSaleBoth'] == 'Both']

        # Count number of parties in each category
        purchase_count = len(purchase_only)
        sale_count = len(sale_only)
        both_count = len(both)

        # Create a DataFrame for plotting
        df2 = pd.DataFrame({
            'Category': ['Purchase Only', 'Sale Only', 'Both'],
            'Count': [purchase_count, sale_count, both_count]
        })

        # Plot pie chart
        fig = px.pie(df2, values='Count', names='Category', title='Party Distribution by Purchase/Sale/Both')
        st.plotly_chart(fig)

    def Calculator():
        st.title("CALCULATOR")
        # Get user input for diameter in inches
        with st.sidebar:
            # st.sidebar.image("data/Kuber_logo.jpeg",caption="")
            selected=option_menu(
                menu_title="Calculators",
                options=["Size/Cost Calculator Inches","Size/Cost Calculator MM","SWG To Diameter and Area","Diameter to SWG","Number of Layers","Rod Cost"],
                icons=["calculator","calculator","calculator","calculator","calculator","calculator"],
                menu_icon="cast",
                default_index=0
            )
        if selected=="Size/Cost Calculator Inches":
            #st.subheader(f"Page: {selected}")
            SizeCalculatorinches()
            # graphs()
        elif selected=="Size/Cost Calculator MM":
            #st.subheader(f"Page: {selected}")
            SizeCalculatorMM()
            # graphs()
        elif selected=="SWG To Diameter and Area":
            SWG_to_DA()
        elif selected=="Diameter to SWG":
            Dia_to_SWG()
        elif selected=="Number of Layers":
            layers()
        elif selected=="Rod Cost":
            RodCost()

        # st.sidebar.image("data/Kuber_logo.jpeg",caption="")
    def reports():
        st.title("Inventory Report")
        power_bi_embed_code = """<iframe title="Inventry Dashboard" width="915" height="600" src="https://app.powerbi.com/reportEmbed?reportId=08d20a68-0292-4f91-bb4e-e7442dfa4d7e&autoAuth=true&ctid=e97bc3a3-8b62-4fc6-a6d9-f9f3f07f3c12" frameborder="1" allowFullScreen="true"></iframe> """

        # Display the embedded Power BI report using st.write
        st.write(power_bi_embed_code, unsafe_allow_html=True)
        # st.components.v1.iframe(power_bi_embed_code, width=800, height=500)
        def update_data(excel_path, df, changes):
            '''Updates the inventory data in the Excel sheet.'''
            
            if changes['edited_rows']:
                deltas = changes['edited_rows']
                for i, delta in deltas.items():
                    df.loc[i, list(delta.keys())] = list(delta.values())
            
            if changes['added_rows']:
                new_rows = pd.DataFrame(changes['added_rows'])
                df = pd.concat([df, new_rows], ignore_index=True)
            
            if changes['deleted_rows']:
                df = df.drop(changes['deleted_rows'])
            
            # Reset index if needed
            df = df.reset_index(drop=True)
            
            # Save the updated dataframe back to Excel
            df.to_excel(excel_path, index=False)
            
            return df
        Inventory=pd.read_excel('Inventory.xlsx')
        nested_products=pd.read_excel('Nested_Products.xlsx')
        edited_df = st.data_editor(
            Inventory,
            disabled=['S.No.'], # Don't allow editing the 'id' column.
            num_rows='dynamic', # Allow appending/deleting rows.
            # column_config={
            #     # Show dollar sign before price columns.
            #     "price": st.column_config.NumberColumn(format="$%.2f"),
            #     "cost_price": st.column_config.NumberColumn(format="$%.2f"),
            # },
            key='inventory_table')
        has_uncommitted_changes1 = any(len(v) for v in st.session_state.inventory_table.values())
        st.button(
            'Commit changes',
            type='primary',
            disabled=not has_uncommitted_changes1,
            # Update data in database
            on_click=update_data,
            args=("Inventory.xlsx", Inventory, st.session_state.inventory_table))
        # edited_df = st.data_editor(
        #     nested_products,
        #     disabled=['S.No.'], # Don't allow editing the 'id' column.
        #     num_rows='dynamic', # Allow appending/deleting rows.
        #     # column_config={
        #     #     # Show dollar sign before price columns.
        #     #     "price": st.column_config.NumberColumn(format="$%.2f"),
        #     #     "cost_price": st.column_config.NumberColumn(format="$%.2f"),
        #     # },
        #     key='nested_inventory_table')
        # has_uncommitted_changes2 = any(len(v) for v in st.session_state.nested_inventory_table.values())
        # st.button(
        #     'Commit changes',
        #     type='primary',
        #     disabled=not has_uncommitted_changes2,
        #     # Update data in database
        #     on_click=update_data,
        #     args=("Nested_Products.xlsx", nested_products, st.session_state.nested_inventory_table))
        
        st.subheader('Units left', divider='red')

        need_to_reorder = Inventory[Inventory['Quantity(KGS/MTS)'] < Inventory['Threshold']].loc[:, 'ProductName']

        if len(need_to_reorder) > 0:
            items = '\n'.join(f'* {name}' for name in need_to_reorder)

            st.error(f"We're running dangerously low on the items below:\n {items}")
        
        st.altair_chart(
            # Layer 1: Bar chart.
            alt.Chart(Inventory)
                .mark_bar(
                    orient='horizontal',
                )
                .encode(
                    x='Quantity(KGS/MTS)',
                    y='ProductName',
                )
            # Layer 2: Chart showing the reorder point.
            + alt.Chart(Inventory)
                .mark_point(
                    shape='diamond',
                    filled=True,
                    size=50,
                    color='salmon',
                    opacity=1,
                )
                .encode(
                    x='Threshold',
                    y='ProductName',
                )
            ,
            use_container_width=True)

        st.caption('NOTE: The :diamonds: location shows the reorder point.')
        #menu bar
    def sideBar():
        with st.sidebar:
            # st.sidebar.image("data/Kuber_logo.jpeg",caption="")
            selected=option_menu(
                menu_title="Main Menu",
                options=["Home","Inventory","Production Tracking","Orders","Reports","Calculator","Machine_Entry","Log Out"],
                icons=["house","eye","book","book","book","book","book","lock"],
                menu_icon="cast",
                default_index=0
            )
        if selected=="Home":
            #st.subheader(f"Page: {selected}")
            Home()
            # graphs()
        elif selected=="Calculator":
            #st.subheader(f"Page: {selected}")
            Calculator()
            # graphs()
        elif selected=="Orders":
            order_data()
        elif selected=="Production Tracking":
            order_status(person_name)
        elif selected=="Machine_Entry":
            machine_form()
        elif selected=="Inventory":
            conversion_module()
        elif selected=="Reports":
            reports()
        elif selected=="Log Out":
            authenticator.logout()

    sideBar()
# sideBar()

#theme
hide_st_style=""" 

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""
