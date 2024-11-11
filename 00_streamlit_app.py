import streamlit as st
import pandas as pd
from streamlit_ldap_authenticator import Authenticate

# Set up the Streamlit page with a title and an icon
st.set_page_config(
    layout = "wide",
    page_title = "Daten-Apps", 
    initial_sidebar_state = "auto",
    page_icon = ":material/menu:"
)

# # CSS to hide the Streamlit menu and footer
# hide_streamlit_style = """
#     <style>
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     [data-testid="stToolbar"] {visibility: hidden;}  /* Hides the entire toolbar including "Deploy" */
#     [data-testid="stHeader"] {visibility: hidden;}   /* Hides the Streamlit header */
#     </style>
#     """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Declare the authentication object using credentials and session settings from Streamlit secrets
auth = Authenticate(
    st.secrets['ldap'],
    st.secrets['session_state_names'],
    st.secrets['auth_cookie']
)

# Login Process
user = auth.login()

# Display login instructions only if the user is not logged in
if user is None:
    st.markdown("### Anweisungen zur Anmeldung")
    st.markdown("Bitte geben Sie Ihre vollständige E-Mail-Adresse (z. B. `j.pracht@pracht.com`) ein, um sich anzumelden.")
    st.markdown("Hinweis: Das Passwort ist dasselbe wie bei der Windows-Anmeldung (LDAP).")

# # For displaying the dataset from LDAP-Server
# st.markdown("### TEST")
# st.markdown(user)

# Load the list of authorized users from a CSV file
user_df = pd.read_csv('0_data/user_authorised.txt')

# Check if the login was successful
if user is not None:
    # Display a logout form with a welcome message
    auth.createLogoutForm({'message': f"Welcome {user['displayName']}"})

    # Verify if the logged-in user is in the list of authorized users
    user_row = user_df[user_df['Email'] == user['userPrincipalName'].lower()]
    
    if not user_row.empty:
        # Extract the authorized apps for the logged-in user
        authorized_apps = user_row['AuthorizedApps'].values[0].split(',')

        # Define available pages in a dictionary
        all_apps = {
            "pim": st.Page("01_pim.py", title="PIM Abgleich", icon=":material/inventory:"),
            "epd": st.Page("02_epd.py", title="EPD Daten", icon=":material/eco:"),
            "pvt": st.Page("03_pvt.py", title="Umsatz Pivottabelle", icon=":material/table_view:"),
            "test": st.Page("99_test_app.py", title="Test App", icon=":material/bug_report:")
        }

        # Filter available pages based on user authorization
        pages_to_display = [all_apps[app.strip()] for app in authorized_apps if app.strip() in all_apps]

        # Set up navigation between the pages
        pg = st.navigation(pages_to_display)

        # Run the selected page
        pg.run()
    else:
        # Display a warning message if the user is not authorized
        st.warning("Your Account has not been authorised to use these applications. Please contact the IT department to obtain authorisation.")
