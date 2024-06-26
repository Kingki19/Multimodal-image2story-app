import streamlit as st
import google.generativeai as genai
import PIL.Image
# Download Story (libraries)
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from docx import Document
from odf.opendocument import OpenDocumentText
from odf.text import P


##### PAGE CONFIGURATION #####
def page_config() -> None:
        ''' Function to manage page configuration'''
        st.set_page_config(
                page_title="MI2S",
                page_icon="📝",
                layout="wide",
                initial_sidebar_state="auto"
        )
###### SESSION STATE MANAGEMENT #####
# def global_variabel() -> None:
        

##### GEMINI CONFIGURATION #####
class GeminiAPIManager:
        def check_gemini_api_key(self, gemini_api_key: str) -> None:
                ''' 
                Function to check whether the API key was really exist in Google. 
                This function especially made for `gemini_api_input()` below
                '''
                if len(gemini_api_key) != 0:
                        try:
                                genai.configure(api_key=gemini_api_key)
                                model = genai.GenerativeModel('gemini-pro')
                                response = model.generate_content("Hello")
                                st.success("Gemini API key is valid!")
                        except Exception as e:
                                st.warning(e)                        
        def gemini_api_input(self) -> str: #It return API-key as string, i can't store it in st.session_state
                ''' Function to input and manage Gemini-AI api key'''
                # Input API key for Gemini API
                input_gemini_api = st.text_input(
                        label='Gemini-AI API key',
                        placeholder='Input your own Gemini-AI API key',
                        type='password',
                        help='required to use this application'
                )
                if input_gemini_api == '':
                        st.info('Please input gemini API key before using this app')
                        st.markdown('''
                        Or if you don't have one, get your own Gemini-AI API key here:  
                        [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
                        ''')
                        return None
                        
                api_key_valid = True
                try: # Check first 
                        self.check_gemini_api_key(input_gemini_api)
                except Exception:
                        api_key_valid = False
                if api_key_valid == True:
                        return input_gemini_api
                else: 
                        st.error("Invalid Gemini API key. Please check and try again.")
                        return None

##### MODEL CONFIGURATION
class Model:
        ''' This whole object class was build followed by this documentation: 
        (if something error whenever it call the model, i or YOU can help to fix it using following link below)
        - Get Started with Gemini using Python:     https://ai.google.dev/gemini-api/docs/get-started/python
        - Configure the generative model:           https://ai.google.dev/api/python/google/generativeai/GenerativeModel
        - All types of Gemini models are available: https://ai.google.dev/api/python/google/generativeai/list_models
        
        THANKS FOR GOOGLE that give me chance of money freedom for research using Gemini-AI API while making this app.
        Error: I can't store gemini api key in st.session_state --> Fix: i store it in local variavble instead
        '''
        def __init__(self, gemini_api_key):
                self.gemini_api_key = gemini_api_key
        
        def configuration(self):
                '''Configure the model and use it in multiple case'''
                genai.configure(api_key=self.gemini_api_key)
                gemini_version = 'models/gemini-1.5-pro-latest' # Here if you want to change gemini model, i set it into this because it support multimodal input. check https://ai.google.dev/api/python/google/generativeai/list_models
                model = genai.GenerativeModel(gemini_version)
                return model
                
        def summary_prompt(self) -> str: # This is not finish yet (don't call it)
                '''If user already generated lot of story, Model can't handle so many input. So i made another model to summary the result'''
                if 'story_results' not in st.session_state:
                        st.session_state.story_results = []
                if len(st.session_state.story_results) < 3: #This mean if user already generate 3 story (press generate button 3 times)
                        return None
                else:
                        story_combined = '\n\n'.join(st.session_state.story_results)
                        prompt = f"""
                        Help me to summarize this whole story:   
                        {story_combined}
                        """
        def summarize_the_story(self) -> str: # This is not finish yet (don't call it)
                '''Model summarize the story'''
                prompt = self.summary_prompt()
                if prompt is not None:
                        return None
                
        def generate_story_prompt(self) -> str:
                '''Manage prompt that will used to input it to Gemini'''
                if 'story_results' not in st.session_state:
                        st.session_state.story_results = []
                if 'model_generate_story_prompt' not in st.session_state:
                        st.session_state.model_generate_story_prompt = None
                # Combined all stories from a list into a string
                story_combined = '\n\n'.join(st.session_state.story_results)
                if len(st.session_state.story_results) > 0:
                        last_generated_story = st.session_state.story_results[-1]
                else: 
                        last_generated_story = ""
                input_prompt = f"""
                        Hey, help me to generate a continuous story based on some image input.
                        For now, the following story is produced:  
                        
                        {story_combined}
                        
                        You just have to continue the story from the story above without needing to rewrite the story. If there's no story in it then you have to create a new one.
                        Make it readable for human.
                        Here are the rules you must adhere to when producing stories based on images:
                        - Writing Style: {st.session_state.writing_style}
                        - Story Theme: {st.session_state.story_theme}
                        - Image Type: {st.session_state.image_type}
                        - You need generate story exactly {str(st.session_state.total_paragraphs)} paragraphs
                        - Here's additional message for you when generate the story:
                        {st.session_state.add_message}
                """
                # Return
                st.session_state.model_generate_story_prompt = input_prompt
                
        def generate_story_from_image(self) -> list[str]:
                '''Generate story using input image, last stories (if exist), input other text'''
                # Execute prompt function
                self.generate_story_prompt()
                model = self.configuration()
                text_prompt = str(st.session_state.model_generate_story_prompt)
                # text_prompt = "Buatkan cerita dari gambar ini!"
                image = st.session_state.uploaded_image
                if st.session_state.uploaded_image == None:
                        st.error("Image is not uploaded")
                        return
                response = model.generate_content([text_prompt, image], stream=False)
                
                st.write(response.text)
                
                st.session_state.story_results.append(response.text)
                

        

##### TABS CONFIGURATION #####
class TabInput:
        def __init__(self, gemini_api_key):
                self.gemini_api_key = gemini_api_key
                
        def count_iteration(self) -> None:
                '''Just help how many user generate for each iteration'''
                if 'iteration' not in st.session_state:
                        st.session_state.iteration = 0
                        st.session_state.disabled = False
                if st.session_state.iteration > 0:
                        st.session_state.disabled = True
                st.markdown(f'You have generate story: {st.session_state.iteration}')
        
        def input_image_col(self) -> None:
                '''Create input column for image and show the image'''
                # Initiate session state
                if 'uploaded_image' not in st.session_state:
                        st.session_state.uploaded_image = None
                        st.session_state.image_uploaded = False
                if 'disabled_generate_button' not in st.session_state:
                        st.session_state.disabled_generate_button = True
                        
                # Columns for image
                st.markdown('''
                        > After you generate story, please press `x` in image input option.  
                        > I cannot add feature to delete image in input after story is generated based on current image due to limitation on Streamlit Framework.
                        ''')
                col_image_upload, col_image_show = st.columns(2)
                
                with col_image_upload:
                        uploaded_image = st.file_uploader(
                                "Choose image file", 
                                type=["jpg", "jpeg", "png", "webp"], 
                                help='Only accept one image'
                        )
                        
                        if uploaded_image is not None:
                                # Access image uploaded using Image from PIL (Pillow)
                                image_PIL = PIL.Image.open(uploaded_image)
                                
                                # Save image to session state
                                st.session_state.uploaded_image = image_PIL
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
        
        def input_writing_style(self) -> None:
                '''Add writing style to story'''
                # Initiate
                if 'writing_style' not in st.session_state:
                        st.session_state.writing_style = None
                # Add
                if st.session_state.disabled == False:
                        writing_style_input = st.text_input(
                                "Writing Style",
                                placeholder = 'e.g Poetic, Novel, Caption, Short Story, etc',
                                help = "You can only input this once for each ongoing story",
                                disabled = st.session_state.disabled
                        )
                else:
                        writing_style_input = st.text_input(
                                "Writing Style",
                                placeholder = f"{st.session_state.writing_style}",
                                help = "You can only input this once for each ongoing story",
                                disabled = st.session_state.disabled
                        )
                if (writing_style_input is not None) and (st.session_state.iteration == 0): # add it to global variable
                        st.session_state.writing_style = writing_style_input
        
        def input_story_theme(self) -> None:
                '''add theme to story'''
                # initiate
                if 'story_theme' not in st.session_state:
                        st.session_state.story_theme = None
                # add
                if st.session_state.disabled == False:
                        story_theme_input = st.text_input(
                                "Story Theme",
                                placeholder = "e.g Good vs Evil, beauty, loyalty, friendship",
                                help = "You can only input this once for each ongoing story",
                                disabled = st.session_state.disabled
                        )
                else:
                        story_theme_input = st.text_input(
                                "Story Theme",
                                placeholder = f"{st.session_state.story_theme}",
                                help = "You can only input this once for each ongoing story",
                                disabled = st.session_state.disabled
                        )
                if (story_theme_input is not None) and (st.session_state.iteration == 0): # add it to global variable
                        st.session_state.story_theme = story_theme_input

        def input_image_type(self) -> None:
                '''user input image type manually or make it blank'''
                # initiate 
                if 'image_type' not in st.session_state:
                        st.session_state.image_type = None
                # add
                image_type_input = st.text_input(
                        "Image Type",
                        value = "",
                        help = 'You must fill in this section',
                        placeholder = "e.g character, backstory, moments, place, etc"
                        )
                st.session_state.image_type = image_type_input
                
                if st.session_state.image_type == '':
                        st.session_state.disabled_generate_button = True
                        
        def input_total_paragraph(self) -> None:
                '''user input total paragraph'''
                # initiate
                if 'total_paragraphs' not in st.session_state:
                        st.session_state.total_paragraphs = None
                # add
                total_par_input = st.number_input(
                        'Total Paragraphs Generated',
                        min_value = 1,
                        max_value = 10,
                        value = 1,
                        help = 'Based on your expectation, i give limit for each image to generate max 10 paragraph. The more paragraphs there are the more random things Gemini will add to the story. From me, i recommend for using in range 1 to 5'
                )
                st.session_state.total_paragraphs = total_par_input

        def input_add_message(self) -> None:
                '''User input additional message'''
                if 'add_message' not in st.session_state:
                        st.session_state.add_message = None
                add_message_input = st.text_area(
                        'Additional Message',
                        help = 'Additional prompts that are not in the options',
                        placeholder = '(1) a name or atmosphere or certain emotion to an image; (2) more detail to story that will be generated such as dialog, interaction, etc'
                )
                st.session_state.add_message = add_message_input
                
        def generate_story_button(self) -> None:
                '''Button to run model to generate story'''
                if 'generate_button_clicked' not in st.session_state:
                        st.session_state.generate_button_clicked = False
                if st.button("Generate a story", disabled = st.session_state.disabled_generate_button):
                        # Manage error if user forget to input gemini api key
                        if (self.gemini_api_key == "") or (self.gemini_api_key == None):
                                st.error("You forgot to enter the Gemini-API-Key")
                                return
                        # Execute some code here, right now for debug
                        Model(self.gemini_api_key).generate_story_from_image()
                        st.session_state.iteration += 1
                        # Reset session to delete images
                        st.session_state.uploaded_image = None
                        st.session_state.image_uploaded = False
                        st.session_state.disabled = True
                        st.session_state.generate_button_clicked = True
                        # Rerun app
                        st.rerun()
        
        def create_tab_input(self) -> None:
                '''Tab for input images and another element to generate story'''
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
                self.input_add_message() # Add additional message
                
                # Add button to execute action in the input tab
                col_generate_button, col_button_clicked = st.columns(2)
                with col_generate_button: 
                        self.generate_story_button()
                with col_button_clicked:
                        # Tell user to go to another tab after the story was generated
                        if st.session_state.generate_button_clicked == True:
                                st.success('You have generate story, please go to `story` tab')
                                st.session_state.generate_button_clicked = False
                      
class TabStory:
        def download_story_to_pdf(self, story_text: str) -> None:
                buffer = BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=letter)
                styles = getSampleStyleSheet()
                story_paragraphs = story_text.split("\n")
                story = [Paragraph(p, styles["BodyText"]) for p in story_paragraphs if p.strip()]
                doc.build(story)
                pdf_data = buffer.getvalue()
                buffer.close()
                st.download_button("Download in PDF", pdf_data, file_name="output_story.pdf", mime="application/pdf")
                
        def download_story_to_doc(self, story_text: str) -> None:
                doc = Document()
                doc.add_paragraph(story_text)
                doc_buffer = BytesIO()
                doc.save(doc_buffer)
                doc_data = doc_buffer.getvalue()
                doc_buffer.close()
                st.download_button("Download in DOC", doc_data, file_name="output_story.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                

        def download_story_to_odt(self, story_text: str) -> None:
                doc = OpenDocumentText()
                para = P(text=story_text)
                doc.text.addElement(para)
                with BytesIO() as output:
                        doc.save(output)  # Simpan ke BytesIO
                        data = output.getvalue()  # Dapatkan data biner
                st.download_button("Download in ODT", data, file_name="output_story.odt", mime="application/vnd.oasis.opendocument.text")
                        
        def popover_download_story(self, disabled) -> None:
                if 'story_results' in st.session_state:   
                        story_combined = '\n\n'.join(st.session_state.story_results)
                else:
                        story_combined = ""
                with st.popover("Download Story", use_container_width=True, disabled = disabled):
                        self.download_story_to_pdf(story_combined)
                        self.download_story_to_doc(story_combined)
                        self.download_story_to_odt(story_combined)
                        
        def create_tab_story(self) -> None:
                ''' Function to create tab for story output'''
                if ('story_results' not in st.session_state) or (st.session_state.story_results == []):
                        story_results_generated = True
                        disable_popover_download = True
                else:
                        story_results_generated = False
                        disable_popover_download = False
                        
                col_header_story, col_download = st.columns([0.6, 0.4])
                with col_header_story: st.subheader('Story Output')
                with col_download: self.popover_download_story(disabled = disable_popover_download)
                        
                if story_results_generated is True:
                        st.info('There is no story generated yet')
                else:
                        story_combined = '\n\n'.join(st.session_state.story_results)
                        st.markdown(story_combined)

class TabChat: 
        def create_tab_chat(self) -> None:
                ''' Function to create tab for chat with story
                '''
                st.subheader('Chat with story')
                st.markdown("""
                *under development*
                """)

class TabHistory:
        def create_tab_history(self, gemini_api_key):
                st.subheader('Prompt history for story generation')
                Model(gemini_api_key).generate_story_prompt()
                st.write(st.session_state.model_generate_story_prompt)

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

        col_tutorial, col_tutor_popover = st.columns([8, 2])
        with col_tutorial: st.write("If you are new to this application, please pay attention to the short tutorial on the side/below")
        with col_tutor_popover:
                with st.popover("Quick Tutorial:"):
                        st.markdown("""
                                You need to follow this 
                                1. Get your own api key here: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
                                2. Input your own api key
                                3. Input image first (to manage error, if you get `ValueError` please delete and input image again)
                                4. Input another element such as writing style, story theme, etc
                                5. (OPTIONAL) Input additional message like languange would use or character/moment name or etc
                                6. Press 'generate story' button
                                7. If you want to generate more story: delete image by pressing `x` button and follow again this step from step (3)
                        """)
        
        with st.container(border=True): 
                gemini_api_key = GeminiAPIManager().gemini_api_input()

        tab1, tab2, tab3, tab4 = st.tabs(["📥 Input", "📖 Story", "💬 Chat", "📜 History"])
        with tab1: 
                TabInput(gemini_api_key).create_tab_input()
        with tab2: TabStory().create_tab_story()
        with tab3: TabChat().create_tab_chat()
        with tab4: TabHistory().create_tab_history(gemini_api_key)

# Execute main
main()
