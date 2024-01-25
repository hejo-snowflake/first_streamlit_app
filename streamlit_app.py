# import and set up streamlit app
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

# add some basic headings and items
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


# import table with data on fruits
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')  # use the Fruit column as the index so that it appears in the selection widget below (instead of just IDs)

# add widget for fruit selection
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display table
streamlit.dataframe(fruits_to_show)


# create function for fruityvice website call
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)          # get fruit information from website
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())                            # take the json data and normalize it, i.e. turns it into a proper table
    return fruityvice_normalized


# New Section to display fruityvice API response, changed such that only part of the code is executed every time a new fruit is entered, no more default
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')  # added input text field
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
  else:
      streamlit.dataframe( get_fruityvice_data(fruit_choice) )  # output the normalized fruit data as a table

except URLError as e:
  streamlit.error()






streamlit.header("The fruit load list contains:")
# Snowflake-related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM fruit_load_list")
        return my_cur.fetchall() # all lines

# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)


# Allow the end user to add fruit to the list (not really though, it's just displayed but not added to the DB
add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'Jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

# Add SQL INSERT statement, this inserts the value 'from streamlit' every time one interacts wtih the app 
# --> Control of Flow problem since it is ALWAYS added, not just when we want (i.e. when entering a new fruit in the second insert field and hitting enter)
my_cur.execute("INSERT INTO fruit_load_list VALUES ('from streamlit')")
