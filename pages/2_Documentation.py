import streamlit as st
import streamlit_mermaid as stmd

def main():
        st.title('MI2S Documentation')
        st.divider()
        st.header('Feature:')
        st.divider()
        st.header('Graph Input-Output Process')
        code = """
        graph TD;
                A-->B;
                A-->C;
                B-->D;
                C-->D;
        """
        stmd.st_mermaid(code)
        st.divider() 

main()
