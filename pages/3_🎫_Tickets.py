# pages/3_Tickets.py
import streamlit as st
from app.data.tickets import get_all_tickets

st.set_page_config(page_title="IT Tickets", page_icon="🎫", layout="wide")


if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Login required.")
    st.stop()

st.title("🎫 IT Tickets Overview")

df = get_all_tickets()

col1, col2, col3 = st.columns(3)
col1.metric("Total Tickets", len(df))
col2.metric("Open Tickets", (df["status"] == "Open").sum() if "status" in df.columns else 0)
col3.metric("High Priority", (df["priority"] == "High").sum() if "priority" in df.columns else 0)

st.divider()

colA, colB = st.columns(2)
with colA:
    st.subheader("Priority Breakdown")
    if "priority" in df.columns and not df.empty:
        st.bar_chart(df["priority"].value_counts())
    else:
        st.info("No priority data available.")

with colB:
    st.subheader("Status Breakdown")
    if "status" in df.columns and not df.empty:
        st.bar_chart(df["status"].value_counts())
    else:
        st.info("No status data available.")

st.divider()
st.subheader("📄 Full Ticket Table")
st.dataframe(df, use_container_width=True)
