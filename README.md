# Toddler Picture Story Generator
# 幼儿图画故事生成器

This Streamlit web application generates simple, engaging stories for toddlers, complete with images and audio narration. It uses OpenAI's GPT-4o-mini for story generation, DALL-E for image creation, and Edge TTS for audio narration.

这个Streamlit网络应用程序为幼儿生成简单、有趣的故事，配有图片和音频讲述。它使用OpenAI的GPT-4o-mini进行故事生成，DALL-E创建图像，以及Edge TTS进行音频讲述。

## Features
## 功能

- Generate short stories suitable for 2-3 year-old toddlers in American English
- Create matching images using DALL-E
- Produce audio narration with selectable voices
- Save generated stories, images, and audio files

- 用美式英语生成适合2-3岁幼儿的短篇故事
- 使用DALL-E创建匹配的图像
- 使用可选择的声音生成音频讲述
- 保存生成的故事、图像和音频文件

## Screenshot
## 截图

![](Screenshot.png)

## Requirements
## 要求

- Python 3.7+
- OpenAI API key
- Streamlit
- edge-tts
- requests
- python-dotenv

## Installation
## 安装

1. Clone the repository:
   克隆仓库：
   ```
   git clone https://github.com/yourusername/toddler-picture-story-generator.git
   cd toddler-picture-story-generator
   ```

2. Install the required packages:
   安装所需的包：
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your OpenAI API key:
   在根目录创建一个`.env`文件并添加你的OpenAI API密钥：
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage
## 使用方法

1. Run the Streamlit app:
   运行Streamlit应用：
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`).
   打开你的网络浏览器，访问Streamlit提供的URL（通常是`http://localhost:8501`）。

3. Enter a story idea or keywords in the text area.
   在文本区域输入故事想法或关键词。

4. Select a voice for the audio narration from the dropdown menu.
   从下拉菜单中选择音频讲述的声音。

5. Click the "Generate/Regenerate Story" button to create a new story, image, and audio.
   点击"生成/重新生成故事"按钮来创建新的故事、图像和音频。

6. Use the "Regenerate Image" and "Regenerate Audio" buttons to create new versions of these elements if desired.
   如果需要，使用"重新生成图像"和"重新生成音频"按钮来创建这些元素的新版本。

## How It Works
## 工作原理

1. Story Generation: Uses OpenAI's GPT-4 to create a short story based on the user's input.
   故事生成：使用OpenAI的GPT-4根据用户输入创建短篇故事。
2. Image Generation: Utilizes DALL-E to create an image that matches the story.
   图像生成：利用DALL-E创建与故事匹配的图像。
3. Audio Generation: Employs Edge TTS to convert the story text into spoken audio.
   音频生成：使用Edge TTS将故事文本转换为语音音频。
4. File Management: Saves generated stories, images, and audio files with unique timestamps.
   文件管理：使用唯一的时间戳保存生成的故事、图像和音频文件。

## File Structure
## 文件结构

- `app.py`: Main Streamlit application file
- `texts/`: Directory for saved story text files
- `images/`: Directory for saved image files
- `audios/`: Directory for saved audio files

- `app.py`：主Streamlit应用文件
- `texts/`：保存故事文本文件的目录
- `images/`：保存图像文件的目录
- `audios/`：保存音频文件的目录

## Contributing
## 贡献

Contributions are welcome! Please feel free to submit a Pull Request.
欢迎贡献！请随时提交Pull Request。

## License
## 许可证

This project is open source and available under the [MIT License](LICENSE).
本项目是开源的，遵循[MIT许可证](LICENSE)。
