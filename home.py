import streamlit as st
import pandas as pd

def show_home():
    st.title("Personalized Wine Recommendation System")
    st.image("png/logo.jpg")  # Ensure the path to your actual logo is correct

    # Directly show the input box for the name
    name = st.text_input("What's your name?", key='name_input')
    
    if st.button("Save"):
        # Define the column names as specified
        columns = ["Druivensoort", "Zuur", "Body / vol", "Suiker / zoet", "Citrusfruit", "Appel", "Tropisch fruit", 
                   "Steenfruit", "Meloen", "Peer", "Noten", "Rood fruit", "Bloemen", "Honing", "Kruiden"]

        # Initialize CSV with the name and zero for other columns
        initial_values = [name] + [0.0] * 14  # Name and zeros for other wine-related columns
        data = pd.DataFrame([initial_values], columns=columns)
        
        # Save to a CSV file
        data.to_csv('csv/user_data.csv', index=False)
        
        st.success(f"Hello {name}, your preferences have been saved. Proceed to the questionnaire through the sidebar.")
