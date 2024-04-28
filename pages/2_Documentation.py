import streamlit as st

def main():
        st.title('MI2S Documentation')
        st.divider()
        st.header('Feature:')
        st.divider()
        st.header('Graph Input-Output Process')
        st.markdown("""
        ```mermaid
                graph TD;
                A-->B;
                A-->C;
                B-->D;
                C-->D;
        ```
        """)
        st.divider() 

main()
