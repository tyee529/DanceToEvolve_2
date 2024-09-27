import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px

@st.cache_data
def load_google_sheet(sheet_url, sheet_name, json_keyfile_name):
    # Define the scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_name, scope)

    # Authorize the clientsheet 
    client = gspread.authorize(creds)

    # Get the instance of the Spreadsheet
    sheet = client.open_by_url(sheet_url)

    # Get the first sheet of the Spreadsheet
    worksheet = sheet.worksheet(sheet_name)
    data = worksheet.get_all_records()

    # Convert to DataFrame
    df = pd.DataFrame(data)
    return df

# Load data
st.title('Dancer Attendance Analysis')
sheet_url = st.text_input('Enter Google Sheet URL:', 'https://docs.google.com/spreadsheets/d/1nigC8X7S0L7wBsFOhIz8DpXiyNXXnqHxVEIHdzVWl9k/edit?usp=sharing')
sheet_name = st.text_input('Enter Sheet Name (e.g., Sheet1):', 'Data')
json_keyfile_name = st.text_input('Enter JSON Keyfile Name (e.g., credentials.json):', 'winter-clone-436904-v5-aee209d45b4f.json')

if sheet_url and sheet_name and json_keyfile_name:
    df = load_google_sheet(sheet_url, sheet_name, json_keyfile_name)
    st.write("Data Loaded Successfully")

    # Allow user to select attributes for dynamic graphing
    x_axis_options = ['Year', 'Season', 'Session', 'Class', 'Teacher', 'Location', 'City']
    x_axis = st.multiselect('Select X-Axis Variables (Year -> Season -> Session Order Recommended)', x_axis_options, default=['Year', 'Season', 'Session'])

    if x_axis:
        # Grouping data based on selected x-axis variables
        grouped_df = df.groupby(x_axis).agg({'DancerID': 'count'}).reset_index()
        grouped_df.rename(columns={'DancerID': 'Number of Dancers'}, inplace=True)

        # Plotting the dynamic graph
        fig = px.bar(grouped_df, x=x_axis, y='Number of Dancers', title='Number of Dancers by Selected Attributes')
        st.plotly_chart(fig)

    # Display data table for reference
    if st.checkbox('Show Raw Data'):
        st.dataframe(df)
else:
    st.write("Error, cmon man, what r u doing Tyler")
