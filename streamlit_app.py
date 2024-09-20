# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize your smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom **Smoothie!**
\n
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)


label = 'Choose a fruit'
name_on_order = ''
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:',name_on_order)

cnx = st.connection('snowflake')
session = cnx.session()
#session = get_active_session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)  #
ingredients_list = st.multiselect('Choose uptu 5 ingredients: ', my_dataframe, max_selections = 5)

#options = ('Strawberry','Banana', 'Peaches')
#option = st.selectbox( label, options)
    #, index=0, format_func=special_internal_function, key=None, help=None, on_change=None, args=None, kwargs=None,*, placeholder="Choose an option", disabled=False, label_visibility="visible")


    

if ingredients_list:
    #st.write('You selected:', ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+(' ')
    st.write('You selected:', ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    st.write(my_insert_stmt)
    if ingredients_string:
        time_to_insert = st.button('submit order')
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            mymessage = name_on_order+' your '+ingredients_string+' Smoothie is ordered!'
            st.success(mymessage, icon="✅")
        
