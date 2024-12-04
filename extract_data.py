import geopandas as gpd
import zipfile
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np

plot = True

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

# Zjištění, které záznamy jsou CHKO a které jsou NP
chko = chu_gdf_agg[chu_gdf_agg.index.get_level_values("KATEGCHU") == "CHKO"]
nar_p = chu_gdf_agg[chu_gdf_agg.index.get_level_values("KATEGCHU") == "NP"]

# Načtení dat krajů
kraje_gdf = gpd.read_file(os.path.join("Data250_S-JTSK", "PolbndRegDA.shp"))

if plot:
    # Povolení LaTeXového režimu
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    # Vizualizace
    fig, ax = plt.subplots(figsize=(10, 10))

    # Vykreslení CHKO (např. zeleně)
    chko.plot(ax=ax, edgecolor="black", color="green", label="CHKO")

    # Vykreslení NP (např. červeně)
    nar_p.plot(ax=ax, edgecolor="black", color="red", label="NP")

    # Vykreslení hranic krajů (průhledná výplň, jen černé linie)
    kraje_gdf.plot(ax=ax, edgecolor="black", facecolor="none", linewidth=1)

    # Vytvoření vlastní legendy
    legend_patches = [
        Patch(facecolor="green", edgecolor="black", label="CHKO"),
        Patch(facecolor="red", edgecolor='black', label="NP"),
        Patch(facecolor="none", edgecolor="black", label="Hranice krajů")
    ]
    ax.legend(handles=legend_patches, loc="upper right")
    # Adjusting ticks by multiplying them by -1
    xticks = ax.get_xticks()
    yticks = ax.get_yticks()
    ax.set_xticklabels([f"${-1 * int(tick):d}$" for tick in xticks])
    ax.set_yticklabels([f"${-1 * int(tick):d}$" for tick in yticks])

    # Popisky s LaTeXem
    plt.xlabel(r"$Y_{\mathrm{S-JTSK}} \left[\mathrm{m}\right]$")
    plt.ylabel(r"$X_{\mathrm{S-JTSK}} \left[\mathrm{m}\right]$")

    # Zobrazení grafu
    plt.savefig("figures/CHKO_NP_plot.pdf", format="pdf", bbox_inches="tight")
    plt.show()


# data z https://tourdata.cz/data/navstevnost-turistickych-cilu-2023/ v tis.


hrady_zamky = {
    'Hlavní město Praha': 2269.57,
    'Jihočeský kraj': 992.62,
    'Jihomoravský kraj': 1155.75,
    'Karlovarský kraj': 367.00,
    'kraj Vysočina': 353.64,
    'Královéhradecký kraj': 614.56,
    'Liberecký kraj': 585.93,
    'Moravskoslezský kraj': 450.95,
    'Olomoucký kraj': 413.47,
    'Pardubický kraj': 409.20,
    'Plzeňský kraj': 450.50,
    'Středočeský kraj': 1271.47,
    'Ústecký kraj': 353.71,
    'Zlínský kraj': 449.83
}

veze_rozhledny = {
    'Hlavní město Praha': 833.89,
    'Jihočeský kraj': 185.26,
    'Jihomoravský kraj': 60.64,
    'Karlovarský kraj': 25.97,
    'kraj Vysočina': 86.48,
    'Královéhradecký kraj': 186.11,
    'Liberecký kraj': 46.28,
    'Moravskoslezský kraj': 224.76,
    'Olomoucký kraj': 76.44,
    'Pardubický kraj': 28.02,
    'Plzeňský kraj': 77.78,
    'Středočeský kraj': 136.81,
    'Ústecký kraj': 24.80,
    'Zlínský kraj': 75.34
}

prirodni_turisticke_cile = {
    'Hlavní město Praha': 0.00,
    'Jihočeský kraj': 30.19,
    'Jihomoravský kraj': 439.05,
    'Karlovarský kraj': 86.78,
    'kraj Vysočina': 6.09,
    'Královéhradecký kraj': 1172.41,
    'Liberecký kraj': 119.85,
    'Moravskoslezský kraj': 334.36,
    'Olomoucký kraj': 233.80,
    'Pardubický kraj': 7.96,
    'Plzeňský kraj': 0.00,
    'Středočeský kraj': 148.25,
    'Ústecký kraj': 455.83,
    'Zlínský kraj': 15.91
}

# Výpočet celkové plochy ČR (součet ploch všech krajů)
celkova_plocha_cr = kraje_gdf["SHAPE_Area"].sum()

# Výpočet celkové plochy chráněných území (CHKO + NP)
celkova_plocha_chranena = chu_gdf_agg["SHAPE_Area"].sum()
# Výpočet procenta chráněných území z celkové plochy ČR
procento_chranena_cr = (celkova_plocha_chranena / celkova_plocha_cr) * 100
print(f"Procento chráněných území z celkové plochy ČR: {procento_chranena_cr:.2f} %")


print("\nPodíl chráněných území v jednotlivých krajích:")
kraje_prispevek = []
vysledky = [] # list, kde jsou tuply o délce 2 (název, hodnota)
for _, kraj in kraje_gdf.iterrows():
    kraj_geom = kraj.geometry
    kraj_area = kraj["SHAPE_Area"]

    # Průnik krajské geometrie s chráněnými územími
    prunik = chu_gdf_agg.intersection(kraj_geom).area.sum()
    kraje_prispevek.append((kraj["NAMN"], (prunik/celkova_plocha_chranena)*100))

    # Výpočet procenta plochy chráněných území v daném kraji
    procento_chranena_kraj = (prunik / kraj_area) * 100
    vysledky.append((kraj["NAMN"], procento_chranena_kraj))
    print(f"{kraj['NAMN']}: {procento_chranena_kraj:.2f} %")


# Rozdělení seznamu kraje_prispevek na dvě části: názvy a procenta
nazvy, prispevky_procenta = zip(*kraje_prispevek)

shared_colors = plt.cm.tab20.colors[:len(nazvy)]

# Vytvoření koláčového grafu
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(
    prispevky_procenta,
    labels=nazvy,
    autopct="%.1f%%",  # Zobrazení procent v grafu
    startangle=90,     # Natočení grafu
    colors=shared_colors  # Barevná paleta
)

# Nastavení názvu grafu
plt.title("Podíl krajů na celkové rozloze chráněných území v ČR")

# Zobrazení grafu
plt.savefig("figures/prispevek_kraju_CR.pdf", format="pdf", bbox_inches="tight")
plt.show()

nazvy, rozloha_v_krajich = zip(*vysledky)
# Vytvoření sloupcového grafu
fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(nazvy))  # Pozice x pro jednotlivé sloupce
bars = ax.bar(x, rozloha_v_krajich, color=shared_colors, edgecolor="black")

# Popisky os a titul grafu
ax.set_xlabel("Kraje", fontsize=12)
ax.set_ylabel("Procento chráněné plochy [%]", fontsize=12)
ax.set_title("Podíl chráněné plochy v jednotlivých krajích", fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(nazvy, rotation=45, ha="right", fontsize=10)

# Zobrazení hodnot nad sloupci
for bar, perc in zip(bars, rozloha_v_krajich):
    ax.text(
        bar.get_x() + bar.get_width() / 2,  # Střed sloupce
        bar.get_height() + 0.5,  # Trochu nad vrchol sloupce
        f"{perc:.1f}%",  # Zobrazená hodnota
        ha="center", fontsize=10
    )

# Zobrazení grafu
plt.tight_layout()
plt.savefig("figures/podil_CHKU_v_krajich.pdf", format="pdf", bbox_inches="tight")
plt.show()


# Vytvoření seznamů dat
kraje = list(hrady_zamky.keys())
hrady_values = list(hrady_zamky.values())
veze_values = list(veze_rozhledny.values())
prirodni_values = list(prirodni_turisticke_cile.values())

# Pozice na ose X
x = np.arange(len(kraje))

# Vytvoření grafu
fig, ax = plt.subplots(figsize=(12, 6))

# Vykreslení jednotlivých částí sloupců
bar1 = ax.bar(x, hrady_values, color="lightblue", label="Hrady a zámky")
bar2 = ax.bar(x, veze_values, bottom=hrady_values, color="salmon", label="Věže a rozhledny")
bar3 = ax.bar(
    x,
    prirodni_values,
    bottom=np.array(hrady_values) + np.array(veze_values),
    color="lightgreen",
    label="Přírodní turistické cíle"
)

# Přidání popisků a legendy
ax.set_xlabel("Kraje", fontsize=12)
ax.set_ylabel("Hodnota (v tisících návštěvníků)", fontsize=12)
ax.set_title("Návštěvnost turistických cílů v krajích", fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(kraje, rotation=45, ha="right", fontsize=10)
ax.legend()

# Zobrazení grafu
plt.tight_layout()
plt.savefig("figures/navstevnost_prirodnich_cilu.pdf", format="pdf", bbox_inches="tight")
plt.show()