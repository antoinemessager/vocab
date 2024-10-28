from functions import *

st_theme = st_javascript("""window.getComputedStyle(window.parent.document.getElementsByClassName("stApp")[0]).getPropertyValue("color-scheme")""")

if True:
  
  col1, col2 = st.columns(2) 
  with col1:
    st.write('''<style>
    [data-testid="column"] {
        width: calc(33.3333% - 1rem) !important;
        flex: 1 1 calc(33.3333% - 1rem) !important;
        min-width: calc(33% - 1rem) !important;
    }
    </style>''', unsafe_allow_html=True)
    st.button(label='unknown')
    st.button(label='too easy')
  with col2:
    st.write('''<style>
    [data-testid="column"] {
        width: calc(33.3333% - 1rem) !important;
        flex: 1 1 calc(33.3333% - 1rem) !important;
        min-width: calc(33% - 1rem) !important;
    }
    </style>''', unsafe_allow_html=True)
    st.button(label='known')
    st.button(label='reveal')