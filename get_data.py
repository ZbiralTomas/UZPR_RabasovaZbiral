import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the webpage with the required data
url = 'https://tourdata.cz/data/navstevnost-turistickych-cilu-2023/'  # Replace with the correct data URL

# Send a GET request to the webpage
response = requests.get(url)
response.raise_for_status()  # Verify the request was successful

# Parse the content of the webpage with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all tables on the webpage
tables = soup.find_all('table')

# Assuming the first table contains the desired data
if tables:
    table = tables[0]
    # Extract the table data into a pandas DataFrame
    df = pd.read_html(str(table))[0]
    print(df.head())
else:
    print("No tables were found on the webpage.")
