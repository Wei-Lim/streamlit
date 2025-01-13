# ============================================================================ #
# 0 Importiere Pakete

import streamlit as st
import pandas as pd
import os
from pivottablejs import pivot_ui
from sqlalchemy import create_engine
import uuid  # Zur Generierung einer eindeutigen Sitzungs-ID
from datetime import date
from sqlalchemy import text  # Importiere `text` für SQL-Abfragen

# ============================================================================ #
# Setze Streamlit-Layout auf den Breitbildmodus
# st.set_page_config(layout="wide")

# ============================================================================ #
# 1 MySQL-Verbindung einrichten

benutzer     = 'easymorph'
passwort     = 'Morpheus24'
host         = '192.168.131.8' 
datenbank    = 'stats'

mysql_verbindungs_string = f"mysql+pymysql://{benutzer}:{passwort}@{host}/{datenbank}"
mysql_engine = create_engine(mysql_verbindungs_string)

# ============================================================================ #
# 2 Daten aus MySQL laden

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
        Jahr  = d['Jahr'].astype(int),   # Konvertiere 'Jahr' in einen Integer-Wert
        Monat = d['Monat'].astype(int)   # Konvertiere 'Monat' in einen Integer-Wert
    ))
)

# ============================================================================ #
# 3 Streamlit-Benutzeroberfläche einrichten

st.title("Pivottabelle: Umsatz / Menge (Ladezeit ca. 1-2 Min.)")
st.markdown("**!!!! Die Kundendaten (Branchenname) sind noch nicht final bearbeitet !!!!**")
st.text('Belege, die als "Intern / Marketing" und "Kunststoffteile Lighting" kategorisiert sind, wurden entfernt. '
        'Es werden nur die Belegdaten (4 - Rechnung) der letzten 5 Jahre geladen.')

# Pivot-Tabelle mit pivot_ui generieren
html_datei_pfad = os.path.join(os.getcwd(), 'vorgabe_pivot.html')
pivot_ui(
    umsatz_df, 
    outfile_path   = html_datei_pfad, 
    rows           = ["Gruppe"], 
    cols           = ["Jahr"], 
    vals           = ["Umsatz"], 
    aggregatorName = "Summe", 
    rendererName   = "Tabelle"
)

# Pivot-Tabelle in Streamlit anzeigen
st.components.v1.html(
    open(html_datei_pfad, 'r').read(), 
    scrolling = True, 
    height    = 600,  # Höhe erhöhen, um mehr Inhalt anzuzeigen
)

# ============================================================================ #
# 4 Zugriff pro Tag protokollieren

def zugriff_protokollieren():
    """Protokolliert den täglichen Zugriff für jede eindeutige Sitzung."""
    # Initialisiere `session_id`, falls noch nicht gesetzt
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())  # Generiere eine eindeutige Sitzungs-ID

    # Sitzungsinformationen in die Datenbank einfügen
    try:
        with mysql_engine.begin() as conn:  # Automatisches Commit sicherstellen
            conn.execute(
                text("""
                    INSERT IGNORE INTO pvt_access_logs (session_id, access_date)
                    VALUES (:session_id, :access_date)
                """),
                {"session_id": st.session_state.session_id, "access_date": date.today()}
            )
        st.success("Zugriff erfolgreich protokolliert.")
    except Exception as e:
        st.error(f"Zugriffsprotokollierung fehlgeschlagen: {e}")

# ============================================================================ #
# 5 Zugriffsstatistiken anzeigen (Optional)

def zugriffsstatistiken_abrufen():
    """Ruft tägliche Zugriffsstatistiken ab."""
    with mysql_engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT access_date, COUNT(*) AS daily_users
                FROM pvt_access_logs
                GROUP BY access_date
                ORDER BY access_date DESC
                LIMIT 7
            """)
        )
        return pd.DataFrame(result.fetchall(), columns=["Datum", "Benutzer"])

st.subheader("Tägliche Zugriffsstatistiken")

# Funktion zum Protokollieren von Zugriffen aufrufen
zugriff_protokollieren()
zugriffsstatistiken = zugriffsstatistiken_abrufen()
st.dataframe(zugriffsstatistiken)
