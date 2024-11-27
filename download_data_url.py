import requests

# URL ke stažení dat
# url = "https://geoportal.cuzk.cz/ZAKAZKY/Data50/epsg-5514/data50.zip"
url = 'https://geoportal.cuzk.cz/ZAKAZKY/Data250/epsg-5514/data250.zip'

# Odeslání GET požadavku
response = requests.get(url, stream=True)
response.raise_for_status()  # Ověření úspěšnosti požadavku

# Uložení staženého souboru
with open("Data250_S-JTSK.zip", "wb") as file:
    for chunk in response.iter_content(chunk_size=8192):
        file.write(chunk)

print("Stažení dokončeno.")
