# Import necessary libraries
import streamlit as st
import os
from together import Together

# Set your Together API key (ensure it's stored securely in Streamlit Secrets)
os.environ['TOGETHER_API_KEY'] = st.secrets["TOGETHER_API_KEY"]

# Initialize Together client
client = Together()

# Function to generate an image based on a text prompt
def generate_image_with_prompt(prompt):
    """
    Generate an image based on a natural language description.

    Parameters:
    prompt (str): A plain-text description of the desired image.

    Returns:
    str: URL or data of the generated image, or an error message.
    """
    try:
        # Call Together AI for image generation
        response = client.image_generations.create(
            model="meta-diffusion/Diffusion-2.1",  # Text-to-image model
            prompt=prompt,
            options={"size": "512x512"}  # Specify image size (optional)
        )

        # Extract image URL from the response
        image_url = response.image_url
        return image_url

    except Exception as e:
        return f"Error generating image: {e}"

# Streamlit app layout
st.title("Enhanced Text-to-Image Generator")
st.write("Enter a detailed description, and the AI will generate an image based on it!")

# Tips for writing better prompts
with st.expander("Tips for Writing Effective Prompts"):
    st.markdown("""
    - **Be Specific:** Mention the key details about the image, such as objects, environment, or style.
    - **Use Adjectives:** Describe colors, textures, and emotions (e.g., "vivid sunset over a calm ocean").
    - **Mention Artistic Style (Optional):** Specify styles like "realistic," "cartoon," or "abstract."
    - **Set the Scene:** Describe the setting, perspective, or composition (e.g., "a bird's eye view of a city at night").
    - **Include Details:** If applicable, add unique elements (e.g., "a futuristic robot holding a glowing orb").
    """)

# Input box for the user to enter a description
prompt = st.text_area(
    "Image Description", 
    placeholder="Example: A futuristic city at sunset, with flying cars and glowing skyscrapers."
)

# Button to trigger image generation
if st.button("Generate Image"):
    if prompt.strip():
        st.write("### Generated Image:")
        # Generate the image
        image_url = generate_image_with_prompt(prompt)

        # Check if the response is an error or a valid image URL
        if image_url.startswith("Error"):
            st.error(image_url)
        else:
            st.image(image_url, caption="Generated Image", use_column_width=True)
    else:
        st.error("Please provide a valid description.")
