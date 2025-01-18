# Import necessary libraries
import streamlit as st
import os
import requests

# Set your Together API key (ensure it's stored securely in Streamlit Secrets)
os.environ['TOGETHER_API_KEY'] = st.secrets["TOGETHER_API_KEY"]

# Function to generate an image based on a text prompt
def generate_image_with_prompt(prompt):
    """
    Generate an image based on a natural language description.

    Parameters:
    prompt (str): A plain-text description of the desired image.

    Returns:
    str: URL of the generated image, or an error message.
    """
    api_key = os.getenv('TOGETHER_API_KEY')
    url = "https://api.together.xyz/v1/images/generate"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "stabilityai/stable-diffusion-xl-base-1.0",
        "prompt": prompt,
        "steps": 50
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["data"][0]["url"]
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
