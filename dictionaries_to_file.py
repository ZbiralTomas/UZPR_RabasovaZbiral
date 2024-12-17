import json
import os

# Define your dictionaries
data = {
    "hrady_zamky": {
        'Hlavní město Praha': 2269.57,
        'Jihočeský kraj': 992.62,
        'Jihomoravský kraj': 1155.75,
        'Karlovarský kraj': 367.00,
        'Kraj Vysočina': 353.64,
        'Královéhradecký kraj': 614.56,
        'Liberecký kraj': 585.93,
        'Moravskoslezský kraj': 450.95,
        'Olomoucký kraj': 413.47,
        'Pardubický kraj': 409.20,
        'Plzeňský kraj': 450.50,
        'Středočeský kraj': 1271.47,
        'Ústecký kraj': 353.71,
        'Zlínský kraj': 449.83
    },
    "veze_rozhledny": {
        'Hlavní město Praha': 833.89,
        'Jihočeský kraj': 185.26,
        'Jihomoravský kraj': 60.64,
        'Karlovarský kraj': 25.97,
        'Kraj Vysočina': 86.48,
        'Královéhradecký kraj': 186.11,
        'Liberecký kraj': 46.28,
        'Moravskoslezský kraj': 224.76,
        'Olomoucký kraj': 76.44,
        'Pardubický kraj': 28.02,
        'Plzeňský kraj': 77.78,
        'Středočeský kraj': 136.81,
        'Ústecký kraj': 24.80,
        'Zlínský kraj': 75.34
    },
    "prirodni_turisticke_cile": {
        'Hlavní město Praha': 0.00,
        'Jihočeský kraj': 30.19,
        'Jihomoravský kraj': 439.05,
        'Karlovarský kraj': 86.78,
        'Kraj Vysočina': 6.09,
        'Královéhradecký kraj': 1172.41,
        'Liberecký kraj': 119.85,
        'Moravskoslezský kraj': 334.36,
        'Olomoucký kraj': 233.80,
        'Pardubický kraj': 7.96,
        'Plzeňský kraj': 0.00,
        'Středočeský kraj': 148.25,
        'Ústecký kraj': 455.83,
        'Zlínský kraj': 15.91
    },
    "rok_zalozeni_NP": {
        "Krkonošský": 1963,
        "Podyjí": 1991,
        "Šumava": 1991,
        "České Švýcarsko": 2000
    },
    "rok_zalozeni_CHKO": {
        "Český ráj": 1955,
        "Moravský kras": 1956,
        "Šumava": 1963,
        "Jizerské hory": 1968,
        "Jeseníky": 1969,
        "Orlické hory": 1969,
        "Žďárské vrchy": 1970,
        "Český kras": 1972,
        "Labské pískovce": 1972,
        "Beskydy": 1973,
        "Slavkovský les": 1974,
        "České středohoří": 1976,
        "Kokořínsko - Máchův kraj": 1976,
        "Lužické hory": 1976,
        "Pálava": 1976,
        "Křivoklátsko": 1978,
        "Třeboňsko": 1979,
        "Bílé Karpaty": 1980,
        "Blaník": 1981,
        "Blanský les": 1989,
        "Litovelské Pomoraví": 1990,
        "Broumovsko": 1991,
        "Poodří": 1991,
        "Železné hory": 1991,
        "Český les": 2005,
        "Brdy": 2016
    }
}

os.makedirs('data/json_files', exist_ok=True)
# Save to a JSON file
with open("data/json_files/dictionaries.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
