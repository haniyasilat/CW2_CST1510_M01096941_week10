import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Optional


# Database path (points to week08 DATA folder)
DB_PATH = r"C:\Users\hnsil\OneDrive - Middlesex University\CW2_M01096941_CST1510\week08\DATA\intelligence_platform.db"


def normalize_date_str(s: str) -> Optional[str]:
    """Try to parse a date string into ISO YYYY-MM-DD. Return None if unparseable."""
    if not s or not s.strip():
        return None
    s = s.strip()
    formats = ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"]
    for fmt in formats:
        try:
            dt = datetime.strptime(s, fmt)
            return dt.strftime("%Y-%m-%d")
        except Exception:
            continue
    # Try parsing common variants with time included (ISO)
    try:
        dt = datetime.fromisoformat(s)
        return dt.date().isoformat()
    except Exception:
        return None


def normalize_db_dates(db_path: str) -> int:
    """Normalize `date_reported` values in `cyber_incidents` to ISO format. Returns number of rows updated."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, date_reported FROM cyber_incidents")
    rows = cursor.fetchall()
    updated = 0
    for rid, date_val in rows:
        iso = normalize_date_str(date_val)
        if iso and iso != date_val:
            cursor.execute("UPDATE cyber_incidents SET date_reported = ? WHERE id = ?", (iso, rid))
            updated += 1
    conn.commit()
    conn.close()
    return updated


def find_unparseable_rows(db_path: str) -> List[Tuple[int, str]]:
    """Return list of (id, date_reported) for rows that cannot be parsed."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, date_reported FROM cyber_incidents")
    rows = cursor.fetchall()
    bad = []
    for rid, date_val in rows:
        if normalize_date_str(date_val) is None:
            bad.append((rid, date_val))
    conn.close()
    return bad


st.set_page_config(page_title="Incidents", layout="wide")
st.title("Manage Cyber Incidents")
st.write("Create, Read, Update, and Delete cyber incident records.")
st.header("Incident Management")

tab1, tab2, tab3 = st.tabs(["View", "Add New", "Edit/Delete"])


def get_incidents_data(db_path: str = DB_PATH) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query("SELECT * FROM cyber_incidents", conn)
    finally:
        conn.close()
    return df


with tab1:
    st.subheader("View Incidents")
    incidents_df = get_incidents_data()
    st.dataframe(incidents_df)


with tab2:
    st.subheader("Add New Incident")
    with st.form("add_incident_form"):
        current_date = datetime.now().strftime("%Y-%m-%d")
        incident_type = st.selectbox(
            "Incident Type",
            ["Malware", "Phishing", "Espionage", "Data destruction", "Denial of service", "Other"]
        )
        severity = st.selectbox("Severity", ["Low", "Medium", "High"])
        status = st.selectbox("Status", ["Open", "In Progress", "Closed"])
        description = st.text_area("Description")
        reported_by = st.text_input("Reported By", "System")

        submitted = st.form_submit_button("Add Incident")
        if submitted:
            if not description.strip():
                description = "None"
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO cyber_incidents 
                (date_reported, incident_type, severity, status, description, reported_by)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (current_date, incident_type, severity, status, description, reported_by))
            conn.commit()
            conn.close()
            st.success("Incident added successfully!")


with tab3:
    st.subheader("Edit/Delete Incident")
    with st.form("edit_delete_form"):
        date_reported = st.text_input("Date Reported (YYYY-MM-DD or MM/DD/YYYY)", placeholder="2024-11-05 or 11/05/2024")
        new_status = st.selectbox("New Status", ["Open", "In Progress", "Resolved", "Closed"])

        update_submitted = st.form_submit_button("Update Status")
        delete_submitted = st.form_submit_button("Delete Incident")

        if update_submitted:
            iso_date = normalize_date_str(date_reported)
            if iso_date is None:
                st.error("Could not parse the provided date. Use YYYY-MM-DD or MM/DD/YYYY.")
            else:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE cyber_incidents SET status = ? WHERE date_reported = ?",
                    (new_status, iso_date)
                )
                conn.commit()
                conn.close()
                st.success(f"Incident on {iso_date} status updated to {new_status}.")

        if delete_submitted:
            iso_date = normalize_date_str(date_reported)
            if iso_date is None:
                st.error("Could not parse the provided date. Use YYYY-MM-DD or MM/DD/YYYY.")
            else:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM cyber_incidents WHERE date_reported = ?", (iso_date,))
                conn.commit()
                conn.close()
                st.success(f"Incident on {iso_date} deleted successfully.")


with st.expander("Maintenance"):
    st.write("Check and normalize stored date values to ISO `YYYY-MM-DD` format.")
    if st.button("Normalize stored dates"):
        updated = normalize_db_dates(DB_PATH)
        st.success(f"Updated {updated} row(s) to ISO date format.")
        bad = find_unparseable_rows(DB_PATH)
        if bad:
            st.warning("Rows with unparseable dates (fix manually):")
            st.dataframe(pd.DataFrame(bad, columns=["id", "date_reported"]))
        else:
            st.info("No unparseable date values found.")
