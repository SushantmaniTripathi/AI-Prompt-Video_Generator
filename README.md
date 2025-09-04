# 🎥 AI Video Generator

A prompt-to-video tool built using **Gemini API**, **Manim**, and **gTTS** that converts user prompts into short, narrated educational videos.

---

## ✨ Features

- ✅ Beautiful UI built with TailwindCSS
- ✅ Converts user topic into 8 educational sentences
- ✅ Adds natural voice-over using Google Text-to-Speech (gTTS)
- ✅ Displays each sentence using Manim with simple text transitions and timing.
- ✅ Downloadable MP4 video output
- ✅ Entirely Python + Flask-based backend
- ✅ Lightweight, fast, and beginner-friendly

---

## 🚀 How to Run Locally

Follow these exact steps:

```bash
# 1. Clone the Repository
```bash
git clone https://github.com/SushantmaniTripathi/AI-Prompt-Video_Generator.git
cd ai-video-generator

# 2. Create and activate virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# 3. Install all required dependencies
pip install -r requirements.txt

# 4. Run the Flask app
flask --app app.py run

Then open your browser and go to:
👉 http://127.0.0.1:5000

#🗂️ Project Folder Structure

ai-video-generator/
├── app.py
├── gemini_test.py
├── generated_scene.py
├── manim_generator.py
├── hello.py
├── index.html
├── requirements.txt
├── saved_videos/
│   └── final_demo_video.mp4
├── .gitignore
├── .env.example
└── README.md
            

# Demo Use Case

📌 Prompt: What are black holes?
🎬 Result: A short 8-line text-based video explaining black holes with voice-over, ready to download and share.

## 🎥 Demo Video

You can find the final demo video inside the `saved_videos` folder:
`saved_videos/final_demo_video.mp4`

To watch it:
- Click the file, then on the top right corner, click the three dots (⋯)
- Then click "View file"
- Then click `View raw` to download and view it


#📬 Contact

📧 Email: [sushantmanitripathiji@gmail.com] 

💻 GitHub: https://github.com/Sushantmanitripathi


⭐ If you found this project helpful or want to collaborate, feel free to connect!


