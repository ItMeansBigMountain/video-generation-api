import time
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_VEO_API_KEY")

# 🧠 Initialize client with API key
client = genai.Client(api_key=api_key)

# 📹 Start video generation
operation = client.models.generate_videos(
    model="veo-2.0-generate-001",
    prompt="Panning wide shot of a calico kitten sleeping in the sunshine",
    config=types.GenerateVideosConfig(
        person_generation="dont_allow",  # or "allow_adult"
        aspect_ratio="16:9",             # or "9:16"
    ),
)

# ⏳ Poll for completion
while not operation.done:
    time.sleep(20)
    operation = client.operations.get(operation)

# 💾 Save each video
for n, generated_video in enumerate(operation.response.generated_videos):
    client.files.download(file=generated_video.video)
    generated_video.video.save(f"video{n}.mp4")
