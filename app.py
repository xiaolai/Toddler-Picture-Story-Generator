from openai import OpenAI
import streamlit as st
import edge_tts
import asyncio
import os
from datetime import datetime
import requests
from dotenv import load_dotenv
from typing import Literal

ImageSize = Literal["1024x1024", "1792x1024", "1024x1792"]

load_dotenv()

# Step 1: Function to generate a 100-word story
def generate_story(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a children's story writer."},
            {"role": "user", "content": prompt + "\n\nRespond without further explanations or comments. "}
        ],
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

# Step 2: Function to generate images using DALL-E
def generate_images_with_dalle(story, image_prompt, size="1024x1024"):
    dalle_prompt = f"{image_prompt}\n\nStory:\n\n'{story}'"
    response = client.images.generate(
        model="dall-e-3",
        prompt=dalle_prompt,
        size=size,
        quality="standard",
        n=1
    )
    return response.data[0].url

# Step 3: Function to generate audio using Edge TTS
async def generate_audio(story, voice):
    communicate = edge_tts.Communicate(story, voice)
    audio_filename = f"./audios/audio-{st.session_state.timestamp}-{voice}.mp3"
    await communicate.save(audio_filename)
    return audio_filename

def generate_audio_sync(story, voice):
    return asyncio.run(generate_audio(story, voice))

# Function to save story to file
def save_story(story):
    filename = f"./texts/story-{st.session_state.timestamp}.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(story)
    return filename

# Function to save image
def save_image(image_url):
    filename = f"./images/image-{st.session_state.timestamp}-v{st.session_state.image_version}.png"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    response = requests.get(image_url)
    with open(filename, "wb") as f:
        f.write(response.content)
    return filename

# Step 4: Streamlit web app interface
st.title("Toddler Picture Story Generator")

# Function to load API key from .env file
def load_api_key_from_env():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")

# Streamlit widget for API key input
api_key_source = st.radio("Choose OpenAI API Key source:", ("Load from .env", "Enter manually"))

if api_key_source == "Load from .env":
    api_key = load_api_key_from_env()
    if not api_key:
        st.error("No API key found in .env file. Please enter it manually.")
        api_key = st.text_input("Enter your OpenAI API key:", type="password")
else:
    api_key = st.text_input("Enter your OpenAI API key:", type="password")

# Initialize OpenAI client with the API key
if api_key:
    client = OpenAI(api_key=api_key)
else:
    st.error("Please provide a valid OpenAI API key to proceed.")

# Text input for story prompt
story_idea = st.text_area("Please input the Story Idea, keywords or short sentence:", height=50)

# Text area to display and modify prompt template
default_story_prompt = f"""Create a simple story of about 100 words in American English, based on the following ideas:\n\n```\n{story_idea}\n```\n\n Make sure the story suitable for 2-3 year-old toddlers. Use plain and everyday vocabulary, short sentences, and preferably has some rhyming lines."""

story_prompt = st.text_area("Modify the story prompt if needed:", value=default_story_prompt, height=210)

# Text area to display and modify image prompt template
default_image_prompt = """Generate an image based on the following story. The style should be simple and playful, cartoonish, with soft, warm colors, and minimalistic details. The image should be suitable for a 2-year-old child, with clear, easy-to-recognize elements. Ensure that the scene evokes warmth, friendliness, and is rich in visual storytelling, but not overly complex. The composition should be balanced and visually engaging, with a focus on creating a comforting and imaginative atmosphere for storytelling."""

image_prompt = st.text_area("Modify the image prompt if needed:", value=default_image_prompt, height=150)

# Image size selection
image_sizes = {
    "Square (1024x1024)": "1024x1024",
    "Landscape (1792x1024)": "1792x1024",
    "Portrait (1024x1792)": "1024x1792"
}
selected_image_size = st.selectbox("Select image size:", list(image_sizes.keys()))

# List of voices for selection
voices = [
    "en-US-AnaNeural", 
    "en-US-AriaNeural", 
    "en-US-AvaNeural", 
    "en-US-EmmaNeural", 
    "en-US-JennyNeural", 
    "en-US-MichelleNeural", 
    "en-US-GuyNeural", 
    "en-US-AndrewNeural", 
    "en-US-BrianNeural", 
    "en-US-ChristopherNeural", 
    "en-US-EricNeural", 
    "en-US-GuyNeural", 
    "en-US-RogerNeural", 
    "en-US-SteffanNeural"
]

# Dropdown list for voice selection
selected_voice = st.selectbox("Select a voice for the audio:", voices)

# Initialize session state variables
if 'story' not in st.session_state:
    st.session_state.story = ""
if 'image_url' not in st.session_state:
    st.session_state.image_url = ""
if 'audio_file' not in st.session_state:
    st.session_state.audio_file = ""
if 'timestamp' not in st.session_state:
    st.session_state.timestamp = ""
if 'last_voice' not in st.session_state:
    st.session_state.last_voice = ""
if 'last_story' not in st.session_state:
    st.session_state.last_story = ""
if 'image_version' not in st.session_state:
    st.session_state.image_version = 1
if 'audio_version' not in st.session_state:
    st.session_state.audio_version = 1

# Function to generate story
def generate_story_content():
    st.session_state.timestamp = datetime.now().strftime("%Y%m%d.%H%M%S")
    st.session_state.story = generate_story(story_prompt)
    story_file = save_story(st.session_state.story)
    st.session_state.image_version = 1
    st.session_state.audio_version = 1

# Update the generate_images_with_dalle function call
def generate_image_content():
    if st.session_state.story:
        st.session_state.image_url = generate_images_with_dalle(
            st.session_state.story, 
            image_prompt, 
            size=image_sizes[selected_image_size]
        )
        image_file = save_image(st.session_state.image_url)
        st.session_state.image_version += 1
    else:
        st.write("Please generate a story first.")

# Function to generate audio
def generate_audio_content():
    if st.session_state.story:
        if st.session_state.audio_file:
            os.remove(st.session_state.audio_file)
        st.session_state.audio_file = generate_audio_sync(st.session_state.story, selected_voice)
        st.session_state.last_voice = selected_voice
        st.session_state.last_story = st.session_state.story
        st.session_state.audio_version += 1
    else:
        st.write("Please generate a story first.")

# Button to generate all components
if st.button('Generate Story, Image, and Audio'):
    generate_story_content()
    generate_image_content()
    generate_audio_content()

# Display story in a text area with auto-adjusting height
if st.session_state.story:
    story_lines = st.session_state.story.count('\n') + 1
    st.text_area("Story:", value=st.session_state.story, height=story_lines * 25, key="story_display", max_chars=None)

# Display image with a frame
if st.session_state.image_url:
    st.image(st.session_state.image_url, use_column_width=True)

if st.button('Regenerate Image'):
    generate_image_content()
    if st.session_state.image_url:
        st.image(st.session_state.image_url, use_column_width=True)

# Audio player
if st.session_state.audio_file:
    st.audio(st.session_state.audio_file)

if st.button('Regenerate Audio'):
    if st.session_state.story:
        if selected_voice != st.session_state.last_voice or st.session_state.audio_file == "" or st.session_state.story != st.session_state.last_story:
            generate_audio_content()
        else:
            st.write("No need to regenerate audio. Voice hasn't changed and story is the same.")
    else:
        st.write("Please generate a story first.")
