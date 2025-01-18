# Import necessary libraries
import streamlit as st
from together import Together
import os

# Set your Together API key (stored in Streamlit Secrets)
os.environ['TOGETHER_API_KEY'] = st.secrets["TOGETHER_API_KEY"]

# Initialize the Together client
client = Together()

# Function to generate an image based on a text prompt
def generate_image_with_flux(prompt):
    """
    Generate an image based on a natural language description using FLUX.1-schnell model.

    Parameters:
    prompt (str): A plain-text description of the desired image.

    Returns:
    str: URL of the generated image, or an error message.
    """
    try:
        # Call Together API for image generation using FLUX.1-schnell
        response = client.images.generate(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-schnell",  # Text-to-image model
            steps=4  # Adjust steps based on desired quality/performance
        )

        # Extract the image URL from the response
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        return f"Error generating image: {e}"

# Streamlit app layout
st.title("Text-to-Image Generator with Together AI")
st.write("Enter a description, and the AI will generate an image based on it!")

# Input box for the user to enter a description
prompt = st.text_area(
    "Image Description", 
    placeholder="Example: A majestic dragon flying over a medieval castle at sunrise."
)

# Button to trigger image generation
if st.button("Generate Image"):
    if prompt.strip():
        st.write("### Generated Image:")
        # Generate the image using FLUX.1-schnell
        image_url = generate_image_with_flux(prompt)

        # Check if the response is an error or a valid image URL
        if image_url.startswith("Error"):
            st.error(image_url)
        else:
            st.image(image_url, caption="Generated Image", use_column_width=True)
    else:
        st.error("Please provide a valid description.")
