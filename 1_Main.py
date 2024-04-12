import streamlit as st

# App title
st.title('MI2S')
st.divider()

# Description
st.markdown("""
This is description on Markdown
""")  

# Input API key for Gemini API
input_gemini_api = st.text_input(
  label = 'Gemini-AI API',
  placeholder = 'Input your own Gemini-AI API',
  type = 'password'
)
if 'gemini_api_key' not in st.session_state:
    st.session_state['gemini_api_key'] = input_gemini_api
# debug
st.write(input_gemini_api)
