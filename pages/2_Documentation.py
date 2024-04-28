import streamlit as st
import streamlit_mermaid as stmd

def main():
        st.title('MI2S Documentation')
        st.divider()
        st.header('Feature:')
        st.divider()
        st.header('Graph Input-Output Process')
        graph_url = 'https://github.com/Kingki19/Multimodal-image2story-app/blob/main/images/I_O%20graph.drawio.png?raw=true'
        st.image(graph_url, caption='Graph I/O')
        st.divider() 

main()
