import time
import base64
import streamlit as st
from google import genai

# 1. Page Setup
st.set_page_config(page_title="GyaanVeer", page_icon="📚")

# 2. Function to set the background image and styling
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover;
        background-position: top center;
    }}
    /* Reduce Streamlit's default massive top padding */
    .block-container {{
        padding-top: 2rem !important; 
    }}
    /* Glassmorphism for Input Boxes - made a bit darker for contrast */
    .stTextInput input, .stTextArea textarea {{
        background-color: rgba(0, 0, 0, 0.6) !important;
        color: white !important;
        border: 2px solid #e2a6ff !important;
        border-radius: 15px !important;
    }}
    /* Make the labels match the meme aesthetic */
    label {{
        color: #e0f2b3 !important;
        font-family: 'Courier New', Courier, monospace !important;
        font-weight: bold !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

# Apply the background
try:
    add_bg_from_local('bg.jpg')
except Exception as e:
    st.warning("Please upload your image and name it 'bg.jpg'")

# 3. THE INVISIBLE SPACER (The Fix)
# This creates an invisible box that pushes the inputs down. 
# You can change '350px' to '400px' or '300px' to nudge it exactly where you want it!
st.markdown("<div style='height: 450px;'></div>", unsafe_allow_html=True)

# 4. Main App Inputs
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
                    # Put a dark box behind the results so it's readable over your background
                    st.markdown(f"<div style='background-color: rgba(0,0,0,0.8); padding: 20px; border-radius: 10px; color: white; border: 1px solid #e0f2b3;'>{response.text}</div>", unsafe_allow_html=True)
                    break 
                    
                except Exception as e:
                    if attempt < max_retries - 1:
                        st.toast(f"Server busy. Retrying... (Attempt {attempt + 1}/{max_retries})")
                        time.sleep(wait_time)
                        wait_time *= 2 
                    else:
                        st.error(f"Error: {e}")