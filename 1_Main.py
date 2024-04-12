import streamlit as st

# App title
st.title('MI2S: Multimodal Image-2-Stories using Gemini-AI')
st.divider()

# Description
st.markdown("""
MI2S (Multimodal Image2Stories) is an innovative application designed to transform images into captivating narratives.  
This cutting-edge tool utilizes multimodal technology, combining visual and textual elements to generate short stories or even full-length novels based on input images.   
By leveraging Gemini-AI, MI2S analyzes the content, context, and emotions conveyed in the image to craft immersive and engaging storytelling experiences.  
Whether you're seeking to create compelling short stories or embark on novel-writing adventures, MI2S opens up endless possibilities for creative expression through the fusion of visual and literary arts. 
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
