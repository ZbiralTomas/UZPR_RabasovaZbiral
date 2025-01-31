# Interactive Geoplots Project

This project visualizes National Parks (NP) and Protected Landscape Areas (CHKO) in Czechia using **interactive geographic plots** and dynamic charts.

## Features

### Geographic Plot with Pop-Up Window
- **Hovering** displays information about National Parks (NP) or Protected Landscape Areas (CHKO).
- The information includes:
  - Name of the area
  - Area size in km²
  - Year of foundation

### Dynamic Chart Example
- Pie chart for regional contributions
- Bar chart for percentage of protected areas within the area of Czech regions
- Stacked bar chart for tourist visits to natural tourist destinations of Czech regions


## Data Sources

1. **Czech National Parks and Protected Areas**:
   - Retrieved from [Czech Geoportal](https://geoportal.gov.cz).
   - Data files: `data50.zip` and `data250.zip`.

2. **Dictionaries for Foundation Years**:
   - Hand-curated foundation years for NP and CHKO stored in Python dictionaries retrieved from [CzechTourism report](https://tourdata.cz/data/navstevnost-turistickych-cilu-2023/).

---

## Usage

### Running the Application

1. **Clone the Repository**:
   - git clone https://github.com/ZbiralTomas/UZPR_RabasovaZbiral.git cd UZPR_RabasovaZbiral
2. **Install Dependencies**:
   - pip install -r requirements.txt
3. **Run the Program**:
   - python main.py
  

### Features

1. **Geographic Plot**:
- Shows **NP** (red) and **CHKO** (green) boundaries.
- Hover over an area to view:
  - Area name
  - Size
  - Year of foundation

2. **Dynamic Charts**:
- **Pie Chart**: Shows regional contributions.
- **Bar Chart**: Displays percentage of protected areas per region.
- **Stacked Bar Chart**: Highlights tourist site visits by category.

---

## Project Structure

The project consists of the following main components:

### 1. **`main.py`**
The main entry point for running the program. It:
- Loads and prepares spatial datasets for NP and CHKO.
- Processes and aggregates the data.
- Passes the data into the visualization functions.

### 2. **`functions.py`**
Contains all core functions for data visualization and interactivity.

Key functions include:
- **`create_interactive_plots`**: Sets up the figure, axes, and interactive widgets.
- **`on_hover`**: Handles mouse hover events over geographic regions.
- **`toggle_plots`**: Manages visibility of pie, bar, and stacked bar charts based on checkboxes.

### 3. **`dictionaries_to_file.py`**
Handles additional data (e.g., founding years for NP and CHKO) and saves it to dictionaries.


