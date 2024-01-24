# import and set up streamlit app
import streamlit
streamlit.title('My Parents New Healthy Diner')

# add some basic headings and items
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


# import table with data on fruits
import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')  # use the Fruit column as the index so that it appears in the selection widget below (instead of just IDs)

# add widget for fruit selection
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# display table
streamlit.dataframe(my_fruit_list)
