# import and set up streamlit app
import streamlit
import pandas
import requests
import snowflake.connector
import urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

# add some basic headings and items
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


# import table with data on fruits
#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')  # use the Fruit column as the index so that it appears in the selection widget below (instead of just IDs)

# add widget for fruit selection
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display table
streamlit.dataframe(fruits_to_show)



# New Section to display fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')  # added input text field with 'Kiwi' as default
streamlit.write('The user entered ', fruit_choice)

#import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# take the json data and normalize it, i.e. turns it into a proper table
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output the normalized data as a table
streamlit.dataframe(fruityvice_normalized)


# FOR TROUBLESHOOTING: dont't run code after this statement
streamlit.stop()


#import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
# my_data_row  = my_cur.fetchone() # one line  --> this HAS TO BE COMMENTED OUT (or removed), otherwise the first row is saved here and thus not included in the my_data_rows
my_data_rows = my_cur.fetchall() # all lines
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)


# Allow the end user to add fruit to the list (not really though, it's just displayed but not added to the DB
add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'Jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

# Add SQL INSERT statement, this inserts the value 'from streamlit' every time one interacts wtih the app 
# --> Control of Flow problem since it is ALWAYS added, not just when we want (i.e. when entering a new fruit in the second insert field and hitting enter)
my_cur.execute("INSERT INTO fruit_load_list VALUES ('from streamlit')")
