import streamlit as st
from home import show_home
from form import show_form
from result import show_result

# Open streamlit environment
# streamlit run app.py

def menu():
    st.sidebar.title("Menu")
    # Set "Home" as the default page
    page = st.sidebar.radio("Ga naar: ", ["Home", "Vragenlijst", "Uitslagen"], index=0)

    if page == "Home":
        show_home()
    elif page == "Vragenlijst":
        show_form()
    elif page == "Uitslagen":
        show_result()

# Main entry point
if __name__ == "__main__":
    menu()
