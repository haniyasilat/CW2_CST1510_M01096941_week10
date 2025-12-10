import streamlit as st
from app.services.user_service import register_user, login_user
st.set_page_config(
    page_title="Login/Register",
    page_icon="🔑",
    layout="centered"
)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# Check if already logged in
if st.session_state.logged_in:
    st.success(f"Logged in as {st.session_state['username']}")
    if st.button("Go to Dashboard"):
        st.switch_page("pages/1_📊_Dashboard.py")
    st.stop()

# Title
st.title("Welcome!")

# Tabs
tab_login, tab_register = st.tabs(["Login", "Register"])

with tab_login:
    st.subheader("Login")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Login", type="primary"):
        if login_username and login_password:
            success, message = login_user(login_username, login_password)
            if success:
                st.session_state["logged_in"] = True
                st.session_state["username"] = login_username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error(message)
        else:
            st.warning("Please enter username and password")

with tab_register:
    st.subheader("Register")
    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
    
    if st.button("Register", type="primary"):
        if not new_username or not new_password:
            st.warning("Username and password cannot be empty.")
        elif new_password != confirm_password:
            st.warning("Passwords do not match.")
        else:
            success, message = register_user(new_username, new_password)
            if success:
                st.success("Registration successful! You can now log in.")
                st.info("Go to the Login tab to access your account.")
            else:
                st.error(message)