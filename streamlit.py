import streamlit as st

st.title('Summariser')

text_file = st.file_uploader("Pick a file")

number = st.slider("Pick a number", 0, 100)

url = "https://api.meaningcloud.com/summarization-1.0"

if st.button('Run'):
    st.text('Success!!')


