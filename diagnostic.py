import streamlit as st

st.set_page_config(page_title="Streamlit Diagnostic")

st.title("Streamlit is working!")
st.write("If you can see this, the page is rendering.")

if st.button("Click me"):
    st.success("Button interaction is working!")