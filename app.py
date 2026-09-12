import time
import base64
import streamlit as st
from google import genai

# 1. Page Setup
st.set_page_config(page_title="GyaanVeer", page_icon="📚")

# 2. Function to set the background image and Liquid Glass styling
def add_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        # Decode the bytes to a string so it can be used in the CSS
        encoded_string = base64.b64encode(file.read()).decode()
        
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
        }}
        /* Add your Liquid Glass CSS styling here */
        .liquid-glass {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
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

# 3. The Invisible Spacer to push elements below the logo
st.markdown("<div style='height: 450px;'></div>", unsafe_allow_html=True)
st.markdown(" 👉[GET YOUR FREE API KEY HERE](https://aistudio.google.com/app/apikey)", unsafe_allow_html=True)
api_key = st.text_input("ENTER YOUR GEMINI API KEY:", type="password")
notes = st.text_area("PASTE YOUR STUDY NOTES HERE:", height=150)

if st.button("GENERATE MY STUDY GUIDE"):
   if not api_key or not notes:
      st.warning("PLEASE PROVIDE BOTH AN API KEY AND YOUR NOTES!")
   else:
      client = genai.Client(api_key=api_key)
      prompt = f"""Act as a friendly and encouraging Indian school teacher. I am providing you with my study notes below. 
      First, break down the key concepts into 5 to 7 easy-to-understand bullet points. 
      Then, create a simple 5-question multiple-choice quiz to test basic understanding. 
      Where possible, frame the quiz questions using everyday Indian examples (e.g., using terms like local markets, chai, cricket, or local geography) to make the concepts easy to grasp.
      Provide the correct answers at the bottom of the page hidden under an 'Answer Key' heading.

      Notes: {notes}
      """
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
                st.markdown(
                    f"<div class='liquid-glass'>{response.text}</div>",
                    unsafe_allow_html=True
                )
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    st.toast(f"Server busy. Retrying... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    wait_time *= 2 
                else:
                    st.error(f"Error: {e}")