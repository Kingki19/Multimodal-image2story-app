import streamlit as st
import streamlit_mermaid as stmd

def main():
        st.title('MI2S Documentation')
        st.divider()
        st.markdown("""
                Drive demo app: [https://drive.google.com/drive/folders/1q5JD0FOkX-lAcIhVcojK1z4LrTPjGXNT?usp=drive_link](https://drive.google.com/drive/folders/1q5JD0FOkX-lAcIhVcojK1z4LrTPjGXNT?usp=drive_link)     
        """)
        st.divider()
        st.header('Feature')
        st.markdown("""
        - It can generate any text/story/poem/etc from image
        - It can generate story continously
        - Chat with story: you can ask what really happen to story and ask Gemini suggestion what's next story that could be make
        """)
        st.divider()
        st.header('Weakness/Problems')
        st.markdown("""
        - Chat feature still not develop yet (I don't have enough time)
        - User can't continue story if the user end it (suggestion: User can send document that contain last story input. But i don't have enough time to develop it)

        *Main feature is complete and i will publish the project to Google AI Hackaton. After that, i still continue the project until all is done.*
        """)
        st.divider()
        st.header('Graph Input-Output Process')
        graph_url = 'https://github.com/Kingki19/Multimodal-image2story-app/blob/main/images/I_O%20graph.drawio.png?raw=true'
        st.image(graph_url, caption='Graph I/O')
        st.divider() 

main()
