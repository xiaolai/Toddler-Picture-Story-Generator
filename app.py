from openai import OpenAI
import streamlit as st
import edge_tts
import asyncio
import os
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()
# Set your OpenAI API key

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
def generate_images_with_dalle(story, size="1024x1024"):
    dalle_prompt = f"""Generate an image based on the following story: \n\n'{story}'\n\n The style should be simple and playful, with soft, warm colors. The image should be suitable for a 2-year-old child, with clear, easy-to-recognize elements. Ensure that the scene evokes warmth, friendliness, and is rich in visual storytelling, but not overly complex. The composition should be balanced and visually engaging, with a focus on creating a comforting and imaginative atmosphere for storytelling."""
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

# Text input for story prompt
story_idea = st.text_area("Please input the Story Idea, keywords or short sentence:", height=50)

# Text area to display prompt template
story_prompt = f"""Create a simple story of about 100 words in American English, based on the following ideas:\n\n```\n{story_idea}\n```\n\n Make sure the story suitable for 2-3 year-old toddlers. Use plain and everyday vocabulary, short sentences, and preferably has some rhyming lines."""

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

# Function to generate image
def generate_image_content():
    if st.session_state.story:
        st.session_state.image_url = generate_images_with_dalle(st.session_state.story)
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
        # st.write(f"Audio saved to: {st.session_state.audio_file}")
        st.session_state.last_voice = selected_voice
        st.session_state.last_story = st.session_state.story
        st.session_state.audio_version += 1
    else:
        st.write("Please generate a story first.")

# Buttons to generate individual components
if st.button('Generate/Regenerate Story'):
    generate_story_content()
    generate_image_content()
    generate_audio_content()

# Display story in a text area with auto-adjusting height
story_lines = st.session_state.story.count('\n') + 1
st.text_area("Generated Story:", value=st.session_state.story, height=story_lines * 25, key="story_display", max_chars=None)

# Display image with a frame
if st.session_state.image_url:
    st.image(st.session_state.image_url, use_column_width=True, caption="Generated Image")

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
