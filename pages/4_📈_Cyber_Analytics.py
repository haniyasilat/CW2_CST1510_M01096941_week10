import plotly.express as px
import streamlit as st
import pandas as pd
import sqlite3
with st.sidebar:
    st.title("Visualizations")
st.set_page_config(page_title="Visualizations", layout="wide")
st.title("Cyber Incidents Analytics")

def get_incidents_data():
    db_path = r"C:\Users\hnsil\OneDrive - Middlesex University\CW2_M01096941_CST1510\week08\DATA\intelligence_platform.db"
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
    conn.close()
    return df

incidents_df = get_incidents_data()

# Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Incidents", len(incidents_df))
with col2:
    st.metric("Open Incidents", len(incidents_df[incidents_df["status"] == "Open"]))

with col3:
    st.metric("Types", incidents_df["incident_type"].nunique())
incidents_df['date_parsed'] = pd.to_datetime(incidents_df['date_reported'], format='%m/%d/%Y')
st.subheader("Incident Types")
type_counts = incidents_df['incident_type'].value_counts()
fig1 = px.bar(type_counts, title="Incidents by Type")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.scatter(
    incidents_df, 
    x='date_parsed', 
    y='incident_type',  # Show incident type on y-axis
    title="Incidents Over Time",
    color='incident_type',  # Color by incident type
    size_max=10
)
st.plotly_chart(fig2, use_container_width=True)