import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

with st.sidebar:
    st.title(" Dashboard")
# Connect to the same database as Week 8
def get_incidents_data():
    db_path = Path(r"C:\Users\hnsil\OneDrive - Middlesex University\CW2_M01096941_CST1510\week9\app\data\intelligence_platform.db")
    conn = sqlite3.connect(str(db_path))
    df = pd.read_sql_query("SELECT * FROM cyber_incidents", conn) #takes all the rows from the table and converts to dataframe
    conn.close()
    return df

# Your dashboard code
st.set_page_config(page_title="Dashboard", layout="wide")
st.title("Dashboard")

incidents_df = get_incidents_data()
st.metric("Total Incidents", len(incidents_df))
    
    # Check if we have data and the right columns
if not incidents_df.empty:
    st.bar_chart(incidents_df["incident_type"].value_counts())
    st.dataframe(incidents_df)
else:
    st.warning("Table exists but is empty. Add data through your Week 8 app.")
        
