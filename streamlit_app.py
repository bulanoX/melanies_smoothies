# Import python packages
import streamlit as st

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  "Choose the fruits you want in your custom Smoothie"
)

from snowflake.snowpark.functions import col

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('search_on'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()
name_on_order=st.text_input('Name on Smoothie')
st.write("The name on your Smoothie will be:",name_on_order)

import requests 
ingredients_list = st.multiselect('Choose up to 5 ingredients', my_dataframe, max_selections=5)
ingredients_string=''
if ingredients_list and len(ingredients_list)<6:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    

    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen+' '
        st.subheader(fruit_chosen+' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)    
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
        st.write(ingredients_string)     
      
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    time_to_instert=st.button('Submit Order')
    #st.write(my_insert_stmt)
    if time_to_instert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")




