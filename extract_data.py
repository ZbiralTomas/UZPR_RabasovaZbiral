import geopandas as gpd
import zipfile
import os
import matplotlib.pyplot as plt

# Rozbalení dat Data50_S-JTSK
data50 = 'Data50_S-JTSK'
if not os.path.exists(data50) or not os.listdir(data50):
    with zipfile.ZipFile('Data50_S-JTSK.zip', 'r') as zip_ref:
        zip_ref.extractall(data50)

# Rozbalení dat Data250_S-JTSK
data250 = 'Data250_S-JTSK'
if not os.path.exists(data250) or not os.listdir(data250):
    with zipfile.ZipFile('Data250_S-JTSK.zip', 'r') as zip_ref:
        zip_ref.extractall(data250)

# Načtení dat chráněných území
chu_gdf = gpd.read_file(os.path.join("Data50_S-JTSK", "ChraneneUzemi.shp"))
chu_gdf_agg = chu_gdf.dissolve(by=["NAZEV", "KATEGCHU"], aggfunc="first")

# Načtení dat krajů
kraje_gdf = gpd.read_file(os.path.join("Data250_S-JTSK", "PolbndRegDA.shp"))

# Vizualizace
fig, ax = plt.subplots(figsize=(10, 10))

# Vykreslení hranic chráněných území
chu_gdf_agg.plot(ax=ax, edgecolor="black", color="lightgreen", label="Chráněná území")

# Vykreslení hranic krajů (průhledná výplň, jen černé linie)
kraje_gdf.plot(ax=ax, edgecolor="blue", facecolor="none", linewidth=1, label="Hranice krajů")

# Přidání legendy
plt.legend(loc="upper right")

# Popisky a zobrazení
plt.title("Chráněná území a hranice krajů v ČR")
plt.xlabel("Délka (Longitude)")
plt.ylabel("Šířka (Latitude)")
plt.show()



# data z https://tourdata.cz/data/navstevnost-turistickych-cilu-2023/ v tis.
navstevnost_kraju = {
    'Hlavní město Praha': 11886,
    'Jihočeský kraj': 3010,
    'Jihomoravský kraj': 4808,
    'Karlovarský kraj': 1048,
    'kraj Vysočina': 2042,
    'Královéhradecký kraj': 3980,
    'Liberecký kraj': 2551,
    'Moravskoslezský kraj': 3883,
    'Olomoucký kraj': 2392,
    'Pardubický kraj': 1631,
    'Plzeňský kraj': 2634,
    'Středočeský kraj': 6634,
    'Ústecký kraj': 2002,
    'Zlínský kraj': 3228
}

