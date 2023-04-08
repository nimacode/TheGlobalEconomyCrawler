import psycopg2
import requests
from bs4 import BeautifulSoup

# Step 1: Scrape the list of countries from the website
url = 'https://www.theglobaleconomy.com/economies/'
response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')
continent_list_with_countries = soup.find_all('div', {'class': 'listOfUnits'})



continent_countries_map = {}
for item in continent_list_with_countries:
    continent_name = item.find('div', {'class': 'listOfUnitsTitle'}).text.strip()
    country_list = item.find('div', {'class': ''})
    countries = [x.text.strip() for x in country_list.find_all('a', {'class': 'unitElement'})]
    continent_countries_map[continent_name] = countries


# Step 2: Store the list of countries in a PostgreSQL database
conn = psycopg2.connect(
    dbname="db_name",
    user="user",
    password="",
    host="localhost"
)

cursor = conn.cursor()


# Insert each country into the table
for continent, countries in continent_countries_map.items():
    for country in countries:
        cursor.execute("INSERT INTO countries (name, continent_name) VALUES (%s, %s)", (country, continent))

# Commit the changes and close the connection
conn.commit()
conn.close()