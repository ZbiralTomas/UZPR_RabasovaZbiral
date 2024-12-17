from functions import *
import json

# Definování proměnných
url_50 = "https://geoportal.cuzk.cz/ZAKAZKY/Data50/epsg-5514/data50.zip"
url_250 = 'https://geoportal.cuzk.cz/ZAKAZKY/Data250/epsg-5514/data250.zip'
data_50_fname = 'Data50_S-JTSK.zip'
data_250_fname = 'Data250_JTSK.zip'
data_50_basename = os.path.splitext(data_50_fname)[0]
data_250_basename = os.path.splitext(data_250_fname)[0]

# Stažení dat z ČUZK
if not os.path.exists(data_50_fname):
    DownloadDataFromURL(url_50, data_50_fname)

if not os.path.exists(data_250_fname):
    DownloadDataFromURL(url_250, data_250_fname)

# Extrakce dat (pouze pokud ještě nejsou extrahovaná)
ExtractData(data_50_fname)
ExtractData(data_250_fname)

# Načtení dat chráněných území - odstranění duplikátů a vyřešení stejných jmen NP a chko
chu_gdf = gpd.read_file(os.path.join(data_50_basename, "ChraneneUzemi.shp"))
chu_gdf_agg = chu_gdf.dissolve(by=["NAZEV", "KATEGCHU"], aggfunc="first")

# Rozdělení na CHKO a NP
chko = chu_gdf_agg[chu_gdf_agg.index.get_level_values("KATEGCHU") == "CHKO"]
nar_p = chu_gdf_agg[chu_gdf_agg.index.get_level_values("KATEGCHU") == "NP"]

# Načtení hranic krajů
kraje_gdf = gpd.read_file(os.path.join(data_250_basename, "PolbndRegDA.shp"))

# Načtení adresářů z json file
with open("dictionaries.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Extrakce jednotlivých dat
hrady_zamky = data["hrady_zamky"]
veze_rozhledny = data["veze_rozhledny"]
prirodni_turisticke_cile = data["prirodni_turisticke_cile"]

# Vypočte statistiku
nazvy, rozloha_v_krajich, procentualni_prispevky = statistics(kraje_gdf, chu_gdf_agg)
shared_colors = plt.cm.tab20.colors[:len(nazvy)]

# Otevře okno s interaktivním grafickým zobrazením
create_interactive_plots(chko, nar_p, kraje_gdf, nazvy, procentualni_prispevky, rozloha_v_krajich, hrady_zamky,
                         veze_rozhledny, prirodni_turisticke_cile, shared_colors)

