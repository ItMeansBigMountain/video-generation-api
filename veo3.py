import time, os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GOOGLE_VEO_API_KEY")

client = genai.Client(api_key=api_key)

# 🎨 Customize your video generation
model = "veo-2.0-generate-001"
# model = "veo-3.0-generate-preview"
prompt = (
    "south asains realize they are not arabs, they are not black, they are not white, therefore instead of loving their slave culture, they should be proud of becomming the best version of themselves for the sake of their children and future generations."
)
negative_prompt = "text overlay, watermark, humans, logos"
aspect_ratio = "16:9"  # "9:16" also supported
duration = 8  # between 5–8 seconds
person_generation = "allow_all"  # or: allow_adult, allow_all (check region restrictions)
sample_count = 1
enhance_prompt = True

# 🛠️ Config object
config = types.GenerateVideosConfig(
    person_generation=person_generation,
    aspect_ratio=aspect_ratio,
    number_of_videos=sample_count,
    duration_seconds=duration,
    negative_prompt=negative_prompt,
    enhance_prompt=enhance_prompt,
    seed=None, # optional for deterministic runs
)

# Run generation
print(f"📽️ Generating video using model: {model}...")
operation = client.models.generate_videos(
    model=model,  
    prompt=prompt,
    config=config
)

# ⏳ Poll status with spinner and status message
spinner = ['|', '/', '-', '\\']
spin_idx = 0
print("⏳ Please wait...", end='', flush=True)
while not operation.done:
    sys.stdout.write(f"\r⏳ Please wait... {spinner[spin_idx]} ")
    sys.stdout.flush()
    spin_idx = (spin_idx + 1) % len(spinner)
    time.sleep(0.5)
    print(client.operations)
    operation = client.operations.get(operation)

print(f"\r✅ Video generation complete!           ")

# 💾 Save videos
for idx, vid in enumerate(operation.response.generated_videos):
    filename = f"videos/google-veo-{model}-{idx}.mp4"
    client.files.download(file=vid.video)
    vid.video.save(filename)
    print(f"✅ Saved: {filename}")


# COST ESTIMATE
COST_PER_SECOND = 0.50
total_seconds = duration * sample_count
cost_estimate = round(total_seconds * COST_PER_SECOND, 4)
print(f"💰 Estimated cost: ${cost_estimate} for {total_seconds} seconds of {model}")
