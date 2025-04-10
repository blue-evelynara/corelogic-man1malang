import streamlit as st

st.title("Portfoilo")
st.write("Welcome to this portfolio")

container = st.container()
with container:
    st.subheader("About")
    container.write("User is....")
    container.write("user also...")
