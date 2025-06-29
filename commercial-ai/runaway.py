import requests, time, os, sys, urllib.request
from dotenv import load_dotenv

# 📦 Load environment variables
load_dotenv()
API_KEY = os.getenv("RUNAWAY_API_KEY")

# 📡 API setup
BASE_URL = "https://api.aivideoapi.com"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 🎬 Start generation job
def start_runway_job(prompt, model="gen3", width=1344, height=768, motion=5, duration=5):
    payload = {
        "text_prompt": prompt,
        "model": model,
        "width": width,
        "height": height,
        "motion": motion,
        "time": duration
    }
    res = requests.post(f"{BASE_URL}/runway/generate/text", headers=HEADERS, json=payload)
    res.raise_for_status()
    return res.json()["uuid"]

# ⏳ Poll job status with spinner
def poll_runway_status(uuid, interval=10, timeout=600):
    spinner = ['|', '/', '-', '\\']
    spin_idx = 0
    start_time = time.time()
    print("⏳ Generating video, please wait...", end='', flush=True)

    while time.time() - start_time < timeout:
        res = requests.get(f"{BASE_URL}/status", headers=HEADERS, params={"uuid": uuid})
        res.raise_for_status()
        data = res.json()
        status = data.get("status")

        if status == "done":
            print("\r✅ Runway video generation complete!        ")
            return data.get("video_url")
        elif status == "failed":
            raise Exception("❌ Runway generation failed.")

        sys.stdout.write(f"\r⏳ Runway status: {status} {spinner[spin_idx]} ")
        sys.stdout.flush()
        spin_idx = (spin_idx + 1) % len(spinner)
        time.sleep(interval)

    raise TimeoutError("⏰ Video generation timed out.")

# 💾 Download video file
def download_video(video_url, filename="videos/runway-output.mp4"):
    os.makedirs("videos", exist_ok=True)
    urllib.request.urlretrieve(video_url, filename)
    print(f"✅ Downloaded to: {filename}")

# 💸 Cost estimation
def estimate_cost(seconds, rate=0.02):
    cost = round(seconds * rate, 4)
    print(f"💰 Estimated cost: ${cost} for {seconds}s using Runway gen3")

# 🚀 Main entry
if __name__ == "__main__":
    prompt = "A cinematic drone shot of a forest in autumn, golden leaves falling, sweeping motion"
    duration = 5

    print("📤 Submitting Runway job...")
    uid = start_runway_job(
        prompt=prompt,
        model="gen3",
        motion=5,
        width=1344,
        height=768,
        duration=duration
    )
    print("📦 Job UUID:", uid)

    video_url = poll_runway_status(uid)
    download_video(video_url, f"videos/runway-{uid}.mp4")

    estimate_cost(seconds=duration)
    print("🎉 All done!")
