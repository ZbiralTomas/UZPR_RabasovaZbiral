import os
import requests
import zipfile
import matplotlib # Ensures interactive backend for plotting
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import CheckButtons
import geopandas as gpd
from shapely.geometry import Point
import json
matplotlib.use("TkAgg")


# Stažení dat z URL adresy
def DownloadDataFromURL(url, filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    # Celková velikost souboru
    total_size = int(response.headers.get('Content-Length', 0))
    chunk_size = 8192  # Velikost jednoho bloku dat
    downloaded_size = 0  # Sledování stažených dat

    print(f"Stahuji data z adresy {url}.")

    # Zahájení stahování
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=chunk_size):
            file.write(chunk)
            downloaded_size += len(chunk)

            # Průběh stahování
            progress = int(20 * downloaded_size / total_size)
            progress_bar = f"[{'|' * progress}{'.' * (20 - progress)}]"

            # Převod hodnot z B na MB
            downloaded_mb = downloaded_size / 1_048_576
            total_mb = total_size / 1_048_576
            print(f"\r{progress_bar}   {downloaded_mb:.2f}/{total_mb:.2f} MB", end="")

    print(f"\nSoubor {filename} úspěšně stažen.")


# Extrahuje data, pokud již nejsou extrahována
def ExtractData(zip_file):
    dirname = os.path.splitext(zip_file)[0]
    if not os.path.exists(dirname) or not os.listdir(dirname):
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(dirname)


# Vypočte statistická data, pro vytváření grafů
def statistics(kraje, chu):
    # Výpočet celkové plochy ČR (součet ploch všech krajů)
    celkova_plocha_cr = kraje["SHAPE_Area"].sum()

    # Výpočet celkové plochy chráněných území (CHKO + NP)
    celkova_plocha_chranena = chu["SHAPE_Area"].sum()
    # Výpočet procenta chráněných území z celkové plochy ČR
    procento_chranena_cr = (celkova_plocha_chranena / celkova_plocha_cr) * 100
    print(f"Procento chráněných území z celkové plochy ČR: {procento_chranena_cr:.2f} %")

    print("\nPodíl chráněných území v jednotlivých krajích:")
    vysledky = []  # tuple (nazev, rozloha, procentuální příspěvek)

    for _, kraj in kraje.iterrows():
        kraj_geom = kraj.geometry
        kraj_area = kraj["SHAPE_Area"]

        # Průnik krajů s chráněnými územími
        prunik = chu.intersection(kraj_geom).area.sum()

        # Výpočet příspěvku kraje na celkovou plochu chráněných území
        prispevek_procento = (prunik / celkova_plocha_chranena) * 100

        # Výpočet procenta plochy chráněných území v daném kraji
        procento_chranena_kraj = (prunik / kraj_area) * 100

        # Přidání do výsledného seznamu jako tuple o délce 3
        vysledky.append((kraj["NAMN"], procento_chranena_kraj, prispevek_procento))

        print(f"{kraj['NAMN']}: {procento_chranena_kraj:.2f} %")

    # Rozdělení seznamu na tři části: názvy, rozlohy a příspěvky
    nazvy, rozloha_v_krajich, prispevky_procenta = zip(*vysledky)

    return nazvy, rozloha_v_krajich, prispevky_procenta


def create_interactive_plots(chko, nar_p, kraje_gdf, nazvy, prispevky_procenta,
                             rozloha_v_krajich, hrady_dict, veze_dict,
                             prirodni_dict, shared_colors):
    # Načtení directories se statistickými daty, která nešli stáhnout
    with open("data/json_files/dictionaries.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    NP_years = data["rok_zalozeni_NP"]
    CHKO_years = data["rok_zalozeni_CHKO"]
    x = np.arange(len(nazvy))  # X pozice pro sloupcové grafy

    # Hodnoty z adresářů
    hrady_values = [hrady_dict.get(kraj, 0) for kraj in nazvy]
    veze_values = [veze_dict.get(kraj, 0) for kraj in nazvy]
    prirodni_values = [prirodni_dict.get(kraj, 0) for kraj in nazvy]

    # matplotlib grid pro více nepravidelně rozmístěných grafů a widgetů
    fig = plt.figure(figsize=(18, 12))
    gs = GridSpec(7, 7, figure=fig, height_ratios=[0.3, 2, 3, 0.15, 1, 1, 1], width_ratios=[3, 1, 1, 0.1, 1, 1.5, 0.4])

    geo_ax = fig.add_subplot(gs[1:3, 0:3])  # Geografický graf
    popup_ax = fig.add_subplot(gs[4:7, 0:3])  # Pop-up okno
    plot1_ax = fig.add_subplot(gs[1:4, 4:6])  # Koláčový graf
    plot2_ax = fig.add_subplot(gs[1:4, 4:6])  # Sloupcový
    plot3_ax = fig.add_subplot(gs[1:4, 4:6])  # Sloupcový skládaný

    # Geografický graf
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    # graf CHKO and NP
    chko.plot(ax=geo_ax, edgecolor="black", color="green", label="CHKO")
    nar_p.plot(ax=geo_ax, edgecolor="black", color="red", label="NP")
    kraje_gdf.plot(ax=geo_ax, edgecolor="black", facecolor="none", linewidth=1)

    # legenda
    legend_patches = [
        Patch(facecolor="green", edgecolor="black", label="CHKO"),
        Patch(facecolor="red", edgecolor="black", label="NP"),
        Patch(facecolor="none", edgecolor="black", label="Hranice krajů")
    ]
    geo_ax.legend(handles=legend_patches, loc="upper right")
    geo_ax.set_xlabel(r"$Y_{\mathrm{S-JTSK}} \left[\mathrm{m}\right]$")
    geo_ax.set_ylabel(r"$X_{\mathrm{S-JTSK}} \left[\mathrm{m}\right]$")
    geo_ax.set_title("NP a CHKO v České Republice")

    # x a y do kladných souřadnic -  z nějakého důvodu jsou v geometrii záporné?
    xticks = geo_ax.get_xticks()
    yticks = geo_ax.get_yticks()

    geo_ax.set_xticklabels([f"{-1 * int(tick):d}" for tick in xticks])
    geo_ax.set_yticklabels([f"{-1 * int(tick):d}" for tick in yticks])

    # Koláčový graf
    threshold = 0.5  # threshold pro odstranění hodnot z grafu (zobrazení pod grafem)
    filtered_procenta = []
    filtered_labels = []
    excluded_labels = []
    excluded_values = []

    # zjišťuje hodnoty k odstranění, resp. jejich indexy
    for i, val in enumerate(prispevky_procenta):
        if val >= threshold:
            filtered_procenta.append(val)
            filtered_labels.append(nazvy[i])
        else:
            excluded_labels.append(nazvy[i])
            excluded_values.append(f"{val:.1f}")

    # nakonec nejspíš zbytečná funkce? Zapomněl jsem, že píšu popisy v TeXu a nešlo mi napsat %
    def autopct_format(pct):
        return f"{pct:.1f}%" if pct > 0 else ""

    plot1_ax.clear()
    plot1_ax.pie(
        filtered_procenta,
        labels=filtered_labels,
        autopct=autopct_format,
        startangle=90,
        colors=shared_colors[:len(filtered_labels)]
    )
    plot1_ax.set_title("Podíl krajů na celkové rozloze chráněných území v ČR")

    if excluded_labels:
        exclusion_text = "\n".join(
            f"{label} = {value}\%" for label, value in zip(excluded_labels, excluded_values)
        )
        plot1_ax.text(
            0.5, -0.1, exclusion_text, ha='center', va='center', fontsize=10, transform=plot1_ax.transAxes
        )

    # Sloupcový graf
    bars = plot2_ax.bar(x, rozloha_v_krajich, width=0.7, color=shared_colors, edgecolor="black")
    plot2_ax.set_xlabel("Kraje", fontsize=12)
    plot2_ax.set_ylabel("Podíl chráněné plochy [%]", fontsize=12)
    plot2_ax.set_title("Podíl chráněné plochy v jednotlivých krajích")
    plot2_ax.set_xticks(x)
    plot2_ax.set_xticklabels(nazvy, rotation=45, ha="right", fontsize=10)

    # Složený sloupcový graf
    plot3_ax.bar(x, hrady_values, color="lightblue", label="Hrady a zámky")
    plot3_ax.bar(x, veze_values, bottom=hrady_values, color="salmon", label="Věže a rozhledny")
    plot3_ax.bar(
        x,
        prirodni_values,
        bottom=np.array(hrady_values) + np.array(veze_values),
        color="lightgreen",
        label="Přírodní turistické cíle"
    )
    plot3_ax.set_ylim(0, 3300)
    plot3_ax.set_xlabel("Kraje", fontsize=12)
    plot3_ax.set_ylabel("Návštěvnost [tis. návštěvníků]", fontsize=12)
    plot3_ax.set_title("Návštěvnost turistických cílů v krajích")
    plot3_ax.set_xticks(x)
    plot3_ax.set_xticklabels(nazvy, rotation=45, ha="right", fontsize=10)
    plot3_ax.legend()

    # Pop-up základní fráze
    popup_ax.text(
        0.5, 0.5,
        "Najeďte myší na chráněnou oblast",
        ha='center', va='center', fontsize=12, color='gray'
    )
    popup_ax.axis('off')
    popup_ax.set_title("")

    # Funkce na detekování toho, že je potřeba vypsat data v pop-upu
    def on_hover(event):
        """Handles hover events on the geographic plot."""
        if event.inaxes == geo_ax:
            mouse_point = Point(event.xdata, event.ydata)
            found = False

            # Kontroluje překryv myši a geometrie na základě souřadnic myši - pro NP
            for idx, row in nar_p.iterrows():
                if row.geometry.contains(mouse_point):
                    area_name = idx[0]
                    founded_year = NP_years.get(area_name, "N/A")
                    popup_ax.clear()
                    popup_ax.axis('off')
                    popup_ax.text(
                        0.5, 0.5,
                        f"National Park: {area_name}\n"
                        f"Plocha: {row.geometry.area / 1_000_000.0:.2f} km²\n"
                        f"Vyhlášeno: {founded_year}",
                        ha='center', va='center', fontsize=12
                    )
                    found = True
                    break

            # Kontroluje překryv myši a geometrie na základě souřadnic myši - pro CHKO
            if not found:
                for idx, row in chko.iterrows():
                    if row.geometry.contains(mouse_point):
                        area_name = idx[0]
                        founded_year = CHKO_years.get(area_name, "N/A")
                        popup_ax.clear()
                        popup_ax.axis('off')
                        popup_ax.text(
                            0.5, 0.5,
                            f"CHKO: {area_name}\n"
                            f"Plocha: {row.geometry.area / 1_000_000.0:.2f} km²\n"
                            f"Vyhlášeno: {founded_year}",
                            ha='center', va='center', fontsize=12
                        )
                        found = True
                        break

            # Pokud myš není ani nad jedním chráněným uzemím, ukazuje základní frázi
            if not found:
                popup_ax.clear()
                popup_ax.axis('off')
                popup_ax.text(
                    0.5, 0.5,
                    "Najeďte myší na chráněnou oblast",
                    ha='center', va='center', fontsize=12, color='black'
                )

            fig.canvas.draw_idle()

        # Checkboxy pro výber grafů k zobrazení - tady se mi bohužel nepodařilo vyřešit aby se automaticky "odškrtli"

    checkbox_ax = plt.axes([0.65, 0.06, 0.25, 0.15])
    check_labels = ["Příspěvek krajů k celkové\n rozloze chráněných území v ČR", "Show Bar Chart",
                    "Návštěvnost přírodních cílů v krajích"]
    checkbox = CheckButtons(checkbox_ax, labels=check_labels, actives=[True, False, False])

    # Definice "zmáčknutí tlačítka"
    def toggle_plots(label):
        plot1_ax.set_visible(False)
        plot2_ax.set_visible(False)
        plot3_ax.set_visible(False)

        # Zobrazí zaškrtnutý graf
        if label == "Příspěvek krajů k celkové\n rozloze chráněných území v ČR":
            plot1_ax.set_visible(True)
        elif label == "Show Bar Chart":
            plot2_ax.set_visible(True)
        elif label == "Návštěvnost přírodních cílů v krajích":
            plot3_ax.set_visible(True)

        plt.draw()

    checkbox.on_clicked(toggle_plots)
    fig.canvas.mpl_connect('motion_notify_event', on_hover)

    # Ensure only the first plot is visible initially
    plot2_ax.set_visible(False)
    plot3_ax.set_visible(False)
    plt.tight_layout()
    plt.show()


