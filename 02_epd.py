import streamlit as st
import pandas as pd
import os

# Title of the dashboard
st.title("EPD Familiendaten")

# File uploader for Excel files in the sidebar
uploaded_pim_file = st.sidebar.file_uploader("Upload a PIM Excel file", type=["xlsx", "xls"])

# If a file is uploaded
if uploaded_pim_file is not None:
    
    # Extract the file name without extension
    file_name = os.path.splitext(uploaded_pim_file.name)[0]

    # Read the uploaded Excel file into a DataFrame
    df = pd.read_excel(uploaded_pim_file)

    # Process the DataFrame to calculate minimum and maximum values
    min_max_df = (
        df
        # Drop columns containing "(Unit)" in their names
        .drop(columns=df.filter(like="(Unit)").columns)
        # Pivot the DataFrame longer to reshape the lifetime values
        .melt(
            id_vars   =['Systemleistung', 'Effektiver Lichtstrom', 'Lichtausbeute', 'Schutzart (IP)', 
                        'IK-Stoßfestigkeit', 'max. Höchsttemperatur', 'max. Tiefsttemperatur'],
            var_name  ="LxBy",
            value_name="Lebensdauer"
        )
        # Drop the temporary 'LxBy' column after melting
        .drop(columns='LxBy')
        # Pivot the DataFrame longer to reshape the temperature values
        .melt(
            id_vars   =['Systemleistung', 'Effektiver Lichtstrom', 'Lichtausbeute', 'Schutzart (IP)', 
                        'IK-Stoßfestigkeit', 'Lebensdauer'],
            var_name  ='Temp_Bezeichnung',
            value_name='Temperatur'
        )
        # Drop the temporary 'Temp_Bezeichnung' column after melting
        .drop(columns='Temp_Bezeichnung')
        # Remove duplicate rows from the DataFrame
        .drop_duplicates()
        # Aggregate to find the minimum and maximum values for numeric columns
        .agg(['min', 'max'])
    )

    # Display the resulting DataFrame in the Streamlit app
    st.dataframe(min_max_df)
