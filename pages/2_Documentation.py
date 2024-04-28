import streamlit as st

def main():
        st.title('MI2S Documentation')
        st.divider()
        st.header('Feature:')
        st.divider()
        st.header('Graph Input-Output Process')
        st.markdown("""
        ```mermaid
        flowchart LR
                A-- This is the text! ---B

        ```
        """)
        st.divider() 

main()
