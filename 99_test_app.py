import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Title of the dashboard
st.title("Streamlit Dashboard with File Upload")

# Sidebar
st.sidebar.title("Sidebar")
st.sidebar.header("User Input")

# Sidebar input widgets
user_input = st.sidebar.text_input("Enter a value:")
number_input = st.sidebar.slider("Select a number:", 0, 100, 50)
checkbox_input = st.sidebar.checkbox("Show plot")

# File uploader for Excel files
uploaded_file = st.sidebar.file_uploader("Upload an PIM Excel file", type=["xlsx", "xls"])

# Main content
st.write("You entered:", user_input)
st.write("Slider value:", number_input)

if uploaded_file is not None:
    # Read the Excel file
    df = pd.read_excel(uploaded_file)
    st.write("Uploaded Excel file:", df.head())

    if checkbox_input:
        st.subheader("Plot of Uploaded Data")
        if df.shape[1] >= 2:  # Ensure there are at least two columns for plotting
            fig, ax = plt.subplots()
            ax.plot(df.iloc[:, 0], df.iloc[:, 1], 'o')  # Plot the first two columns
            st.pyplot(fig)
        else:
            st.write("Not enough columns to plot.")
else:
    # Example DataFrame if no file is uploaded
    df = pd.DataFrame({
        'A': np.random.rand(100),
        'B': np.random.rand(100) * number_input
    })
    st.write("Generated DataFrame:", df.head())

    if checkbox_input:
        st.subheader("Plot of Random Data")
        fig, ax = plt.subplots()
        ax.plot(df['A'], df['B'], 'o')
        st.pyplot(fig)

# Footer
st.write("This is a Streamlit dashboard with file upload functionality.")


data = {
    'A': np.random.rand(10),
    'B': np.random.rand(10),
    'C': np.random.rand(10),
    'D': np.random.rand(10)
}
df = pd.DataFrame(data)

# Title of the app
st.title("Streamlit DataFrame Column Filter")

# Show the full DataFrame
st.write("Original DataFrame:")
st.dataframe(df)

# Multiselect widget for selecting columns
selected_columns = st.multiselect(
    "Select columns to display", options=df.columns, default=df.columns.tolist()
)

# Display the filtered DataFrame
if selected_columns:
    filtered_df = df[selected_columns]
    st.write("Filtered DataFrame:")
    st.dataframe(filtered_df)
else:
    st.write("No columns selected.")


