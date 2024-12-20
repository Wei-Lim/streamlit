# ============================================================================ #
# 0 Import packages

import streamlit as st
import pandas as pd
import os
from pivottablejs import pivot_ui
from sqlalchemy import create_engine
# pip install SQLAlchemy pymysql

# ============================================================================ #
# Set Streamlit layout to wide mode
# st.set_page_config(layout="wide")

# ============================================================================ #
# 1 Load Data
# umsatz_df = pd.read_csv("0_data/umsatz.csv")

# MySQL connection
user        = 'William'
password    = 'Will1510!'
host        = '192.168.131.8' 
database    = 'stats'

mysql_con_string = f"mysql+pymysql://{user}:{password}@{host}/{database}"
mysql_engine = create_engine(mysql_con_string)

umsatz_df = pd.read_sql(
    """
        SELECT 
            Jahr, Monat, Umsatz, Menge, Artikelnummer, Artikelstamm_1, 
            Modell, Gruppe, Linie, Branchenname, `Inland / Ausland`
        FROM belegdaten 
        WHERE Jahr >= YEAR(CURDATE()) - 5;
    """, 
    mysql_engine
)

umsatz_df = (
    umsatz_df
    .pipe(lambda d: d.assign(
        Jahr  = d['Jahr'].astype(int),   # Convert 'Jahr' to integer
        Monat = d['Monat'].astype(int)   # Convert 'Monat' to integer
    ))
)

# ============================================================================ #
# 2. Streamlit UI setup

st.title("Pivottabelle Umsatz / Menge (Ladezeit ca. 1-2 min)")
st.markdown("**!!!! Die Kundendaten (Branchenname) sind noch nicht final bearbeitet !!!!**")
st.text('Belege kategorisiert als "Intern / Marketing" und "Kunststoffteile Lighting" sind entfernt worden. Nur die Belegdaten (4 - Rechnung) der letzten 5 Jahren werden geladen')

# Generate pivot table using pivot_ui
html_file_path = os.path.join(os.getcwd(), 'preset_pivot.html')
pivot_ui(
    umsatz_df, 
    outfile_path   = html_file_path, 
    rows           = ["Gruppe"], 
    cols           = ["Jahr"], 
    vals           = ["Umsatz"], 
    aggregatorName = "Sum", 
    rendererName   = "Table"
)

# Display the pivot table in Streamlit
st.components.v1.html(
    open(html_file_path, 'r').read(), 
    scrolling = True, 
    height    = 600,  # Increase height to fit more of the screen
    # width=1500    # Increase width to fit more of the screen
)
