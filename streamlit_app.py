import streamlit as st

st.set_page_config(page_title="Optimizare CNC", layout="centered")
st.title("⚙️ Optimizare Plasmă, Bare & Bond")

tip = st.radio("Alege tipul:", ["Foi Tablă", "Bare", "Bond"])

if tip == "Foi Tablă":
    st.write("Funcționează!")
elif tip == "Bare":
    st.write("Bare în curând...")
else:
    st.write("Bond în curând...")