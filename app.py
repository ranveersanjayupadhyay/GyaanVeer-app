import time
import base64
import streamlit as st
from google import genai

# 1. Page Setup
st.set_page_config(page_title="GyaanVeer", page_icon="📚")

# 2. Function to set the background image and Liquid Glass styling
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    
    """,
    unsafe_allow_html=True
    )

# Apply the background
try:
    add_bg_from_local('bg.jpg')
except Exception as e:
    st.warning("Please upload your image and name it 'bg.jpg'")

# 3. The Invisible Spacer to push elements below the logo
st.markdown("", unsafe_allow_html=True)