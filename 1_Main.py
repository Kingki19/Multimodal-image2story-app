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
  label = 'Gemini-AI API key',
  placeholder = 'Input your own Gemini-AI API key',
  type = 'password',
  help = 'required to use this application'
)
if 'gemini_api_key' not in st.session_state:
    st.session_state['gemini_api_key'] = input_gemini_api
st.markdown('''
Or if you don't have one, get your own Gemini-AI API key here:  
[https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
''')

# debug
st.write(st.session_state['gemini_api_key'])
