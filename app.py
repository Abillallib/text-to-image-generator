# Import necessary libraries
import streamlit as st
import os
from together import Together

# Explicitly pass the API key to Together (from Streamlit Secrets)
client = Together(api_key=st.secrets["TOGETHER_API_KEY"])

# Function to generate an image based on a text prompt
def generate_image_with_flux(prompt):
    try:
        response = client.images.generate(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-schnell",
            steps=4
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        return f"Error generating image: {e}"

# Streamlit app layout
st.title("Text-to-Image Generator with Together AI")
prompt = st.text_area("Image Description", placeholder="Example: A glowing forest under a starry sky.")
if st.button("Generate Image"):
    if prompt.strip():
        image_url = generate_image_with_flux(prompt)
        if image_url.startswith("Error"):
            st.error(image_url)
        else:
            st.image(image_url, caption="Generated Image", use_column_width=True)
    else:
        st.error("Please provide a valid description.")
