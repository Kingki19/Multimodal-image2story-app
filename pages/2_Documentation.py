import streamlit as st
import streamlit_mermaid as stmd

def main():
        st.title('MI2S Documentation')
        st.divider()
        st.header('Feature:')
        st.divider()
        st.header('Graph Input-Output Process')
        code = """
        graph TB
                api_key[/User input api key/]
                api_key_bool{API-key exist or not?}
                input_variable[/User input image, writing style, etc/]
                
                api_key_bool -- API key doesn't exist, input again --> api_key
                api_key_bool -- API key exist, continue --> input_variable

                generate_story(Generate a story)
                story_result[/Story result/]
                input_variable --> generate_story --> story_result

                
        """
        stmd.st_mermaid(code)
        st.divider() 

main()
