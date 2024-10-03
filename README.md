# Toddler Picture Story Generator

This Streamlit web application generates simple, engaging stories for toddlers, complete with images and audio narration. It uses OpenAI's GPT-4o-mini for story generation, DALL-E for image creation, and Edge TTS for audio narration.

## Features

- Generate short stories suitable for 2-3 year-old toddlers in American English
- Create matching images using DALL-E
- Produce audio narration with selectable voices
- Save generated stories, images, and audio files

## Screenshot

![](Screenshot.png)

## Requirements

- Python 3.7+
- OpenAI API key
- Streamlit
- edge-tts
- requests
- python-dotenv

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/toddler-picture-story-generator.git
   cd toddler-picture-story-generator
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Enter a story idea or keywords in the text area.

4. Select a voice for the audio narration from the dropdown menu.

5. Click the "Generate/Regenerate Story" button to create a new story, image, and audio.

6. Use the "Regenerate Image" and "Regenerate Audio" buttons to create new versions of these elements if desired.

## How It Works

1. Story Generation: Uses OpenAI's GPT-4 to create a short story based on the user's input.
2. Image Generation: Utilizes DALL-E to create an image that matches the story.
3. Audio Generation: Employs Edge TTS to convert the story text into spoken audio.
4. File Management: Saves generated stories, images, and audio files with unique timestamps.

## File Structure

- `app.py`: Main Streamlit application file
- `texts/`: Directory for saved story text files
- `images/`: Directory for saved image files
- `audios/`: Directory for saved audio files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
