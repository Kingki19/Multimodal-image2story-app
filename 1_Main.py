import streamlit as st
import google.generativeai as genai

##### PAGE CONFIGURATION #####
def page_config():
        ''' Function to manage page configuration'''
        st.set_page_config(
                page_title="MI2S",
                page_icon="📝",
                layout="wide",
                initial_sidebar_state="auto"
        )

##### GEMINI CONFIGURATION #####
class GeminiAPIManager:
        def check_gemini_api_key(self, gemini_api_key):
                ''' 
                Function to check whether the API key was really exist in Google. 
                This function especially made for `gemini_api_input()` below
                '''
                if len(gemini_api_key) != 0:
                        try:
                                genai.configure(api_key=gemini_api_key)
                                model = genai.GenerativeModel('gemini-pro')
                                response = model.generate_content("Hello")
                        except Exception as e:
                                st.warning(e)                        
        def gemini_api_input(self):
                ''' Function to input and manage Gemini-AI api key'''
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
                	self.check_gemini_api_key(input_gemini_api)
                except Exception:
                	api_key_valid = False
                if api_key_valid and 'gemini_api_key' not in st.session_state:
                	st.session_state['gemini_api_key'] = input_gemini_api

##### MODEL CONFIGURATION #####
### NOT FINISHED
def model_gemini(input):
        ''' Function to use model Gemini-AI to generate content'''
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello")

##### TABS CONFIGURATION #####
class TabInput:
        def count_iteration(self):
                '''Just help how many user generate for each iteration'''
                if 'iteration' not in st.session_state:
                        st.session_state.iteration = 0
                        st.session_state.disabled = False
                if st.session_state.iteration > 0:
                        st.session_state.disabled = True
                st.markdown(f'You have generate story: {st.session_state.iteration}')
        
        def input_image_col(self):
                '''Create input column for image and show the image'''
                # Initiate session state
                if 'uploaded_image' not in st.session_state:
                        st.session_state.uploaded_image = None
                        st.session_state.image_uploaded = False
                        st.session_state.disabled_generate_button = True
                        
                # Columns for image
                st.markdown('> After you input image, please press \'x\' in input. I cannot add feature to delete image in input after story is generated based on current image.')
                col_image_upload, col_image_show = st.columns(2)
                
                with col_image_upload:
                        uploaded_image = st.file_uploader(
                                "Choose image file", 
                                type=["jpg", "jpeg", "png"], 
                                help='Only accept one image'
                        )
                        if uploaded_image is not None:
                                # Simpan gambar ke dalam session state
                                st.session_state.uploaded_image = uploaded_image
                                st.session_state.image_uploaded = True
                                st.session_state.disabled_generate_button = False
                                
                with col_image_show:
                        # If image is uploaded
                        if st.session_state.uploaded_image is not None:
                                st.image(
                                        st.session_state.uploaded_image, 
                                        caption="Uploaded Image", 
                                        use_column_width='auto'
                                )
                # I SAVE THIS BECAUSE SHOW WHAT IS NEED TO 
                # if st.button("Execute"):
                #         # Lakukan eksekusi sesuai dengan tombol tertentu
                        
                #         # Reset session state untuk menghapus gambar
                #         st.session_state.uploaded_image = None
                #         st.session_state.image_uploaded = False
        
        def input_writing_style(self):
                '''Add writing style to story'''
                # Initiate
                if 'writing_style' not in st.session_state:
                        st.session_state.writing_style = None
                # Add
                if st.session_state.disabled == False:
                        writing_style_input = st.text_input(
                                "Writing Style",
                                placeholder = 'e.g: Fantasy, Romance, Sci-fi, etc',
                                disabled = st.session_state.disabled
                        )
                else:
                        writing_style_input = st.text_input(
                                "Writing Style",
                                placeholder = f"{st.session_state.writing_style}",
                                disabled = st.session_state.disabled
                        )
                if writing_style_input is not None: # add it to global variable
                        st.session_state.writing_style = writing_style_input
        
        def input_story_theme(self):
                '''add theme to story'''
                # initiate
                if 'story_theme' not in st.session_state:
                        st.session_state.story_theme = None
                # add
                if st.session_state.disabled == False:
                        story_theme_input = st.text_input(
                                "Story Theme",
                                placeholder = "e.g Good vs Evil, beauty, loyalty, friendship",
                                disabled = st.session_state.disabled
                        )
                else:
                        story_theme_input = st.text_input(
                                "Story Theme",
                                placeholder = f"{st.session_state.story_theme}",
                                disabled = st.session_state.disabled
                        )
                if story_theme_input is not None: # add it to global variable
                        st.session_state.story_theme = story_theme_input

        def input_image_type(self):
                '''user input image type manually or make it blank'''
                # initiate 
                if 'image_type' not in st.session_state:
                        st.session_state.image_type = None
                # add
                image_type_input = st.text_input(
                        "Image Type",
                        value = "",
                        placeholder = "e.g character, backstory, moments, war, etc"
                        )
                st.session_state.image_type = image_type_input

        def input_total_paragraph(self):
                '''user input total paragraph'''
                # initiate
                if 'total_paragraphs' not in st.session_state:
                        st.session_state.total_paragraphs = None
                # add
                total_par_input = st.slider(
                        'Total Paragraphs Generated',
                        min_value = 1,
                        max_value = 3,
                        value = 1,
                        help = 'Based on your expectation'
                )
                st.session_state.total_paragraphs = total_par_input

        def generate_story_button(self):
                '''Button to run model to generate story'''
                if st.button("Generate a story", disabled=st.session_state.disabled_generate_button):
                        # Execute some code here, right now for debug
                        st.write('Write a story')
                        st.write(f'Writing Style: {st.session_state.writing_style}')
                        st.session_state.iteration += 1
                        # Reset session to delete images
                        st.session_state.uploaded_image = None
                        st.session_state.image_uploaded = False
                        # Rerun app
                        st.rerun()
        
        def create_tab_input(self):
                '''Tab for input images and another element to generate story
                '''
                col_subheader_input, col_iteration = st.columns(2)
                with col_subheader_input: st.subheader('Input Image and Elements')
                with col_iteration: self.count_iteration()
                        
                # Input
                self.input_image_col()
                
                # Column for writing style and theme
                col_writing_style, col_theme = st.columns(2)
                with col_writing_style: self.input_writing_style()
                with col_theme: self.input_story_theme()
                        
                # Column for image type and total paragraph
                col_image_type, col_tot_par = st.columns(2)
                with col_image_type: self.input_image_type()
                with col_tot_par: self.input_total_paragraph()
                        
                # Add button to execute action in the input tab
                # if st.session_state.image_uploaded: 
                self.generate_story_button()

class TabStory:
        def create_tab_story(self):
                ''' Function to create tab for story output
                '''
                st.subheader('Story Output')
                st.markdown("""
                *under development*
                """)

class TabChat: 
        def create_tab_chat(self):
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
        with st.container(border=True): GeminiAPIManager().gemini_api_input()
        tab1, tab2, tab3 = st.tabs(["📥 Input", "📖 Story", "💬 Chat"])
        with tab1: TabInput().create_tab_input()
        with tab2: TabStory().create_tab_story()
        with tab3: TabChat().create_tab_chat()

# Execute main
main()
