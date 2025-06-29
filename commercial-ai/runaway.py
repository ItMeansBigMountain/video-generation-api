import requests, time
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("AIVIDEOAPI_KEY")
BASE_URL = "https://api.aivideoapi.com"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

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

def poll_runway_status(uuid, interval=10, timeout=600):
    start_time = time.time()
    while time.time() - start_time < timeout:
        res = requests.get(f"{BASE_URL}/status", headers=HEADERS, params={"uuid": uuid})
        res.raise_for_status()
        data = res.json()
        if data.get("status") == "done":
            return data.get("video_url")
        elif data.get("status") == "failed":
            raise Exception("Generation failed")
        print("⏳", data.get("status"))
        time.sleep(interval)
    raise TimeoutError("Video generation timed out")

if __name__ == "__main__":
    uid = start_runway_job("A cinematic drone shot of a forest in autumn")
    print("Job started:", uid)
    video_url = poll_runway_status(uid)
    print("🎬 Video ready:", video_url)
