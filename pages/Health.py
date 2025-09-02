import streamlit as st
from PIL import Image

st.set_page_config(page_title="Health Check", page_icon="✅", layout="wide")

# Minimal "I'm alive" response
image = Image.open('pages/IMG_1853.jpg')
image = image.rotate(-90)
st.write("Staus OK 200")
st.write("I am alive")
st.image(image, caption="Everything seems to be fine")
