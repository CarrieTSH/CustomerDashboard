import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import altair as alt
import pydeck as pk

#read the files and pre-process the data
customers_info=pd.read_csv(r'C:\Users\Admin\Desktop\课件\Data science with Python\Northwind+Traders\Northwind Traders\customers.csv',encoding='ISO-8859-1')
orders_info=pd.read_csv(r'C:\Users\Admin\Desktop\课件\Data science with Python\Northwind+Traders\Northwind Traders\orders.csv',encoding='ISO-8859-1')

country_counts = customers_info['country'].value_counts().reset_index()
country_counts.columns = ['country', 'count']

orders_info['orderDate'] = pd.to_datetime(orders_info['orderDate']) #to extract year easier
orders_info['Year'] = orders_info['orderDate'].dt.year
orders_count = orders_info.groupby(['Year','customerID']).size().reset_index(name='Count')
orders_count['Year'] = orders_count['Year'].astype(str)

st.set_page_config(
    page_title="Customers info dashboard",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#sidebar customization
with st.sidebar:
    st.title('👤 Customers')
    st.sidebar.markdown('''Created with ❤️ by **Lin WANG & Shuhui TANG**''')

#make a stacked column chart to show top10 customers who had ordered the most in 2013-2015
#step 1: select top 10 customers
total_orders_by_customer = orders_info.groupby('customerID').size().reset_index(name='TotalOrders')
top10_customers = total_orders_by_customer.nlargest(10, 'TotalOrders')['customerID']
top10_customers_orders = orders_count[orders_count['customerID'].isin(top10_customers)]
#step2: create the stacked column chart by plotly
Top10_customers_fig = px.bar (top10_customers_orders, x='customerID', 
    y='Count',color='Year',title="Top 10 Customers in 2013-2015",
    category_orders={"Year": sorted(top10_customers_orders['Year'].unique())},labels={"Count": "Order Volume"},
    barmode='stack',color_discrete_sequence=["#1f77b4", "#aec7e8", "#c6dbef"]
)


#Create a new dictionary which has the countryID for each country name(for the mapping purpose)
country_code_map={
    'Germany': 'DEU',
    'France': 'FRA',
    'Brazil': 'BRA',
    'Spain': 'ESP',
    'USA': 'USA',
    'UK': 'UK',
    'Mexico': 'MEX',
    'Venezuela': 'VEN',
    'Canada': 'CAN',
    'Argentina': 'ARG',
    'Italy': 'ITA',
    'Finland': 'FIN',
    'Denmark': 'DNK',
    'Belgium': 'BEL',
    'Austria': 'AUT',
    'Portugal': 'PRT',
    'Switzerland': 'CHE',
    'Sweden': 'SWE',
    'Ireland': 'IRL',
    'Norway': 'NOR',
    'Poland': 'POL'
}

#make a choropleth map to show the distriubtion of our customers
country_counts['country'] = country_counts['country'].map(country_code_map) 

#mapping the country name in country_counts df with the country ID in country_code_map df
customer_distribution = px.choropleth(country_counts, locations='country', color='count', color_continuous_scale='blues',
                               range_color=(0, max(country_counts.count())),
                               scope="world",
                               labels={'count':'number_of_customers'}
                              )
# use plotly.express package to draw a choropleth map to show the distribution of our customers worldwid. 
# The number of customers will influence the color filled on the map
customer_distribution.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )


st.subheader('Customer Orders')
st.plotly_chart(Top10_customers_fig, use_container_width=True)
st.subheader('Customer Distribution🌍')
st.plotly_chart(customer_distribution, use_container_width=True)

#adjust the layout of the map
