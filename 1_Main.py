import streamlit as st
import google.generativeai as genai

##### PAGE CONFIGURATION
def page_config():
        ''' Function to manage page configuration
        '''
        st.set_page_config(
                page_title="MI2S",
                page_icon="📝",
                layout="wide",
                initial_sidebar_state="auto"
        )

##### GEMINI CONFIGURATION
def check_gemini_api_key(gemini_api_key):
        ''' Function to check whether the API key was really exist in Google
        This function especially made for `gemini_api_input()` below
        '''
        if len(gemini_api_key) != 0:
                try:
                        genai.configure(api_key=gemini_api_key)
                        model = genai.GenerativeModel('gemini-pro')
                        response = model.generate_content("Hello")
                except Exception as e:
                        st.warning(e)                        
def gemini_api_input():
        ''' Function to input and manage Gemini-AI api key
        '''
        # Input API key for Gemini API
        input_gemini_api = st.text_input(
                label='Gemini-AI API key',
                placeholder='Input your own Gemini-AI API key',
                type='password',
                help='required to use this application'
        )
        st.markdown('''
        Or if you don't have one, get your own Gemini-AI API key here:  
        [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
        ''')
        api_key_valid = True
        try:
        	check_gemini_api_key(input_gemini_api)
        except Exception:
        	api_key_valid = False
        if api_key_valid and 'gemini_api_key' not in st.session_state:
        	st.session_state['gemini_api_key'] = input_gemini_api

##### TABS CONFIGURATION
def tab_input():
        ''' Function to create tab for input images and another element to generate story
        '''
        st.subheader('Input Image and Elements')
        st.markdown('> For right now, only limited to one image per upload')
        
        # Columns for image
        col_image_upload, col_image_show = st.columns(2)
        with col_image_upload:
                uploaded_image = st.file_uploader("Choose image file", 
                                                  type=["jpg", "jpeg", "png"], 
                                                  help='Only accept one image')
        with col_image_show:
                if uploaded_image is not None:
                        st.write("filename:", uploaded_image.name)
                        st.image(uploaded_image, 
                                 caption="Uploaded Image", 
                                 use_column_width='auto')
                
        st.write('test')
        
def tab_story():
        ''' Function to create tab for story output
        '''
        st.subheader('Story Output')
        st.markdown("""
        *under development*
        """)
        
def tab_chat():
        ''' Function to create tab for chat with story
        '''
        st.subheader('Chat with story')
        st.markdown("""
        *under development*
        """)

##### MAIN EXECUTION
def main():
        ''' MAIN EXECUTION APPS IN HERE
        '''
        page_config()
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
        with st.container(border=True):
                gemini_api_input()
        tab1, tab2, tab3 = st.tabs(["📥 Input", "📖 Story", "💬 Chat"])
        with tab1: tab_input()
        with tab2: tab_story()
        with tab3: tab_chat()

# Execute main
main()
