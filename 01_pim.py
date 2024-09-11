import pandas as pd
import streamlit as st

# Title of the dashboard
st.title("PIM Abgleich")

# File uploader for Excel files in the sidebar
uploaded_pim_file = st.sidebar.file_uploader("Upload a PIM Excel file", type=["xlsx", "xls"])
uploaded_jk_file  = st.sidebar.file_uploader("Upload a jKarat Excel file", type=["xlsx", "xls"])

# Main content
if uploaded_pim_file is not None:
    # Read the uploaded PIM Excel file into a DataFrame
    pim_df = pd.read_excel(uploaded_pim_file)

if uploaded_jk_file is not None:
    # Read the uploaded jKarat Excel file into a DataFrame
    jk_df = pd.read_excel(uploaded_jk_file)
    
# If both PIM and jKarat files are uploaded
if uploaded_pim_file and uploaded_jk_file:
    # Identify common columns between the two DataFrames, excluding "Artikel-Nr."
    cols = pim_df.columns.intersection(jk_df.columns)
    cols = cols.drop("Artikel-Nr.")

    # Display the common columns as a radio button selection in the sidebar
    selected_column = st.sidebar.radio("Select a column for comparison:", options=cols)

    # If a column is selected, perform the comparison
    if selected_column:
        # Filter the selected column and "Artikel-Nr." from each DataFrame
        pim_col_df = pim_df.filter(items=["Artikel-Nr.", selected_column])
        jk_col_df  = jk_df.filter(items=["Artikel-Nr.", selected_column])

        # Merge the two DataFrames on "Artikel-Nr." with suffixes to differentiate them
        join_df    = pd.merge(pim_col_df, jk_col_df, "left", on="Artikel-Nr.", suffixes=("_pim", "_jk"))

        # Create the column names for comparison
        str_x = "".join([selected_column, "_pim"])
        str_y = "".join([selected_column, "_jk"])

        # Add a "check" column that shows if the selected columns match between the two DataFrames
        join_df["check"] = join_df[str_x] == join_df[str_y]

        # Filter the DataFrame to show only the rows where the columns don't match
        result_df = join_df[join_df["check"] == False]

        # Display the resulting DataFrame
        st.dataframe(result_df)

# Display dataframes for the uploaded files if either file is uploaded
if uploaded_pim_file or uploaded_jk_file:
    st.header("Uploaded Excel Files")

# Display the PIM DataFrame
if uploaded_pim_file is not None:
    st.write("PIM:")
    st.dataframe(pim_df)

# Display the jKarat DataFrame
if uploaded_jk_file is not None:
    st.write("jKarat:")
    st.dataframe(jk_df)
