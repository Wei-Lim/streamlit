import streamlit as st
import pandas as pd
from streamlit_ldap_authenticator import Authenticate

# Set up the Streamlit page with a title and an icon
st.set_page_config(page_title="Daten-Apps", page_icon=":material/menu:")

# CSS to hide the Streamlit menu and footer
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}  /* Hides the entire toolbar including "Deploy" */
    [data-testid="stHeader"] {visibility: hidden;}   /* Hides the Streamlit header */
    </style>
    """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Declare the authentication object using credentials and session settings from Streamlit secrets
auth = Authenticate(
    st.secrets['ldap'],
    st.secrets['session_state_names'],
    st.secrets['auth_cookie']
)

# Login Process
# Prompt the user to log in using their full email address (e.g., w.truong@pracht.com)
user = auth.login()

# Load the list of authorized users from a CSV file
user_df = pd.read_csv('0_data/user_authorised.txt', header=None, names=['Email'])

# Check if the login was successful
if user is not None:

    # Display a logout form with a welcome message
    auth.createLogoutForm({'message': f"Welcome {user['displayName']}"})

    # Verify if the logged-in user is in the list of authorized users
    user_is_authorised = user['userPrincipalName'] in user_df['Email'].values
    
    # If the user is authorized, display the available pages
    if user_is_authorised:
        
        # Pages can be defined here
        pim  = st.Page("01_pim.py", title="PIM Abgleich", icon=":material/inventory:")
        epd  = st.Page("02_epd.py", title="EPD Daten", icon=":material/eco:")
        test = st.Page("99_test_app.py", title="Test App", icon=":material/bug_report:")

        # Set up navigation between the pages
        pg = st.navigation([pim, epd, test])
        
        # Run the selected page
        pg.run()
    else:
        # Display a warning message if the user is not authorized
        st.warning("Your Account has not been authorised to use these applications. Please contact the IT department to obtain authorisation.")
