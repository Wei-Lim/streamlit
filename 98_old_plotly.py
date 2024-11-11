import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# # Erstellung von Beispieldaten für das ganze Jahr
# def create_orderline_data(year):
#     # Erstellen Sie einen Datumsbereich für das gesamte Jahr
#     dates = pd.date_range(start=f'{year}-01-01', end=f'{year}-12-31', freq='D')
#     data = {
#         'Bestell-ID': range(1, len(dates) * 10 + 1),  # Angenommen, 10 Bestellungen pro Tag
#         'Produkt': [f'Produkt {i % 5 + 1}' for i in range(len(dates) * 10)],
#         'Artikelnummer': [f'Artikel {i % 10 + 1}' for i in range(len(dates) * 10)],
#         'Kategorie': [f'Kategorie {i % 3 + 1}' for i in range(len(dates) * 10)],
#         'Vertreter': [f'Vertreter {i % 4 + 1}' for i in range(len(dates) * 10)],
#         'Produktgruppe': [f'Gruppe {i % 2 + 1}' for i in range(len(dates) * 10)],
#         'Menge': [np.random.randint(1, 11) for _ in range(len(dates) * 10)],
#         'Preis': [round(np.random.uniform(5, 50), 2) for _ in range(len(dates) * 10)],
#         'Datum': np.tile(dates, 10)
#     }
#     return pd.DataFrame(data)

# # Laden der Daten für das angegebene Jahr und das vorherige Jahr
# def load_data(current_year):
#     current_year_data = create_orderline_data(current_year)
#     previous_year_data = create_orderline_data(current_year - 1)
    
#     # Berechnung des Umsatzes für beide Jahre
#     current_year_data['Umsatz'] = current_year_data['Menge'] * current_year_data['Preis']
#     previous_year_data['Umsatz'] = previous_year_data['Menge'] * previous_year_data['Preis']
    
#     return current_year_data, previous_year_data

kajspo_df = pd.read_csv("0_data/kajspo.csv")


# year = 2023  # Sie können dieses Jahr beliebig ändern
# current_year_data, previous_year_data = load_data(year)

# # Streamlit-App-Layout
# st.title("Umsatzbericht mit dynamischem Pivot")

# # Seitenleiste für Benutzerauswahl
# st.sidebar.header("Filteroptionen")

# # Dynamische Auswahl für Kategorien
# st.sidebar.write("Wählen Sie Kategorien zum Pivotieren:")
# categories = current_year_data['Kategorie'].unique().tolist()
# selected_categories = st.sidebar.multiselect("Wählen Sie Kategorien:", categories)

# # Dynamische Auswahl für Vertreter
# vertreter = current_year_data['Vertreter'].unique().tolist()
# selected_vertreter = st.sidebar.multiselect("Wählen Sie Vertreter:", vertreter)

# # Dynamische Auswahl für Produktgruppen
# product_groups = current_year_data['Produktgruppe'].unique().tolist()
# selected_product_groups = st.sidebar.multiselect("Wählen Sie Produktgruppen:", product_groups)

# if selected_categories or selected_vertreter or selected_product_groups:
#     # Filtern der Daten basierend auf ausgewählten Kategorien, Vertretern und Produktgruppen
#     filtered_current_data = current_year_data[
#         (current_year_data['Kategorie'].isin(selected_categories) |
#          current_year_data['Vertreter'].isin(selected_vertreter) |
#          current_year_data['Produktgruppe'].isin(selected_product_groups))
#     ]
    
#     filtered_previous_data = previous_year_data[
#         (previous_year_data['Kategorie'].isin(selected_categories) |
#          previous_year_data['Vertreter'].isin(selected_vertreter) |
#          previous_year_data['Produktgruppe'].isin(selected_product_groups))
#     ]

#     # Gruppierung nach Jahr und Monat für das aktuelle Jahr
#     monthly_revenue_current = (
#         filtered_current_data.groupby([filtered_current_data['Datum'].dt.to_period('M')])
#         .agg({'Umsatz': 'sum'})
#         .reset_index()
#     )
#     monthly_revenue_current['Datum'] = monthly_revenue_current['Datum'].dt.to_timestamp()  # In Timestamp umwandeln

#     # Berechnung des kumulierten Umsatzes für das aktuelle Jahr
#     monthly_revenue_current['Kumulierte Einnahmen'] = monthly_revenue_current['Umsatz'].cumsum()

#     # Gruppierung nach Jahr und Monat für das vorherige Jahr
#     monthly_revenue_previous = (
#         filtered_previous_data.groupby([filtered_previous_data['Datum'].dt.to_period('M')])
#         .agg({'Umsatz': 'sum'})
#         .reset_index()
#     )
#     monthly_revenue_previous['Datum'] = monthly_revenue_previous['Datum'].dt.to_timestamp()  # In Timestamp umwandeln

#     # Berechnung des kumulierten Umsatzes für das vorherige Jahr
#     monthly_revenue_previous['Kumulierte Einnahmen'] = monthly_revenue_previous['Umsatz'].cumsum()

#     # Jahrsspalte zu beiden Datensätzen hinzufügen
#     monthly_revenue_current['Jahr'] = year
#     monthly_revenue_previous['Jahr'] = year - 1

#     # Kombinieren der Datensätze zum Plotten
#     combined_revenue = pd.concat([monthly_revenue_current, monthly_revenue_previous], ignore_index=True)

#     # Erstellung einer Plotly-Figur für den monatlichen Umsatzvergleich nach Jahr
#     combined_revenue['Monat'] = combined_revenue['Datum'].dt.strftime('%b')  # Monatsnamen extrahieren
#     combined_revenue['Jahr'] = combined_revenue['Jahr'].astype(str)  # Jahr als String für Gruppierung sicherstellen
    
#     # Monatsumsatz-Diagramm
#     revenue_fig = px.bar(combined_revenue, x='Monat', y='Umsatz', color='Jahr',
#                           title="Monatlicher Umsatzvergleich nach Jahr",
#                           labels={'Umsatz': 'Gesamtumsatz'},
#                           color_discrete_sequence=['blue', 'orange'])

#     # Kumulierte Umsatz-Diagramm
#     cumulative_fig = px.line(combined_revenue, x='Monat', y='Kumulierte Einnahmen', color='Jahr',
#                               title="Kumulierte Einnahmen nach Monat",
#                               labels={'Kumulierte Einnahmen': 'Kumulierte Einnahmen'},
#                               color_discrete_sequence=['green', 'red'])

#     # Layout aktualisieren, um nach Monat zu gruppieren
#     revenue_fig.update_xaxes(categoryorder='array', categoryarray=combined_revenue['Monat'].unique())  # Monate korrekt anordnen
#     revenue_fig.update_layout(xaxis_title='Monat', yaxis_title='Gesamtumsatz')
#     cumulative_fig.update_xaxes(categoryorder='array', categoryarray=combined_revenue['Monat'].unique())  # Monate korrekt anordnen
#     cumulative_fig.update_layout(xaxis_title='Monat', yaxis_title='Kumulierte Einnahmen')

#     # Anzeigen der Plotly-Figuren in Streamlit
#     st.plotly_chart(revenue_fig)
#     st.plotly_chart(cumulative_fig)

#     # Abschnitt für Umsatz nach Artikelnummer für einen bestimmten Monat
#     st.header("Umsatz nach Artikelnummer für einen bestimmten Monat")

#     # Dropdown für Monatselektion
#     month_selection = st.selectbox("Monat auswählen:", 
#                                     pd.date_range(start=f'{year}-01-01', end=f'{year}-12-31', freq='ME').month_name())

#     # Umwandeln der Monatselektion in Monatsnummer
#     month_map = {month: index for index, month in enumerate(pd.date_range(start='2023-01-01', end='2023-12-31', freq='ME').month_name(), start=1)}
#     month_number = month_map[month_selection]

#     # Filtern der Daten für den ausgewählten Monat
#     selected_month_data = filtered_current_data[filtered_current_data['Datum'].dt.month == month_number]

#     # Gruppierung nach Artikelnummer und Berechnung des Umsatzes
#     article_revenue = (
#         selected_month_data.groupby('Artikelnummer')
#         .agg({'Umsatz': 'sum'})
#         .reset_index()
#     )

#     # Anzeigen des Umsatzes nach Artikelnummer
#     if not article_revenue.empty:
#         st.subheader(f"Umsatz für {month_selection} {year}")
#         st.dataframe(article_revenue)

#         # Balkendiagramm für Artikelumsatz
#         article_revenue_fig = px.bar(article_revenue, x='Artikelnummer', y='Umsatz',
#                                       title=f"Umsatz nach Artikelnummer für {month_selection} {year}",
#                                       labels={'Umsatz': 'Gesamtumsatz'})
#         st.plotly_chart(article_revenue_fig)

# else:
#     st.write("Bitte wählen Sie mindestens eine Kategorie, einen Vertreter oder eine Produktgruppe aus, um den Verkaufsbericht anzuzeigen.")
