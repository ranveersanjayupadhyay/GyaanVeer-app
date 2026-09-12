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

st.markdown("👉 GET YOUR FREE API KEY HERE",unsafe_allow_html=True)
api_key = st.text_input("ENTER YOUR GEMINI API KEY:", type="password")
notes = st.text_area("PASTE YOUR STUDY NOTES HERE:", height=150)

if st.button("GENERATE MY STUDY GUIDE"):
   if not api_key or not notes:
      st.warning("PLEASE PROVIDE BOTH AN API KEY AND YOUR NOTES!")
   else:
      client = genai.Client(api_key=api_key)
prompt = f"Summarize the key concepts in bullet points, then create a 5-question multiple-choice quiz based on these notes. Notes: {notes}"
max_retries = 3
wait_time = 2 
    
with st.spinner("GYAANVEER IS ANALYZING..."):
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )
                # Result box also styled as liquid glass
                st.markdown(f"{response.text}", unsafe_allow_html=True) 
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    st.toast(f"Server busy. Retrying... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    wait_time *= 2 
                else:
                    st.error(f"Error: {e}")