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
        "time": duration,
    }
    try:
        res = requests.post(f"{BASE_URL}/runway/generate/text", headers=HEADERS, json=payload)
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("❌ HTTP Error:", e)
        print("🔎 Response content:", res.text)
        raise
    return res.json()["uuid"]

# ⏳ Poll job status with spinner
def poll_runway_status(uuid, interval=10, timeout=600):
    spinner = ['|', '/', '-', '\\']
    spin_idx = 0
    start_time = time.time()
    status_labels = [
        ("in queue", "🟦"),
        ("submitted", "🟦"),
        ("success", "🟩"),
        ("failed", "🟥"),
    ]
    status_order = ["in queue", "submitted", "success", "failed"]

    print("⏳ Generating video, please wait...", end='', flush=True)

    while time.time() - start_time < timeout:
        res = requests.get(f"{BASE_URL}/status", headers=HEADERS, params={"uuid": uuid})
        res.raise_for_status()
        data = res.json()
        status = data.get("status")

        # Build status display
        status_display = []
        for s, emoji in status_labels:
            if s == status:
                status_display.append(f"{emoji} [{s.upper()}] ◀️")
            else:
                status_display.append(f"{emoji} {s}")
        status_line = " | ".join(status_display)

        sys.stdout.write(f"\r{status_line} {spinner[spin_idx]} ")
        sys.stdout.flush()
        spin_idx = (spin_idx + 1) % len(spinner)

        if status == "success":
            print(f"\n\r✅ Runway video generation complete!")
            print(data)
            return data.get("url")
        elif status == "failed":
            err_code = data.get("error_code", "unknown")
            err_msg = data.get("error", "No message")
            print()  # move to next line
            raise Exception(f"❌ Generation failed. Code {err_code}: {err_msg}")

        time.sleep(interval)

    raise TimeoutError("⏰ Video generation timed out.")

# 💾 Download video file + save URL
def download_video(video_url, filename="videos/runway-output"):
    os.makedirs("videos", exist_ok=True)
    filename_txt = f"runaway-video-urls.txt"
    filename_mp4 = f"{filename}.mp4"

    with open(filename_txt, "a") as f:
        f.write(video_url )
        f.write("\n")
    print(f"🔗 Video URL saved to {filename_txt}")

    urllib.request.urlretrieve(video_url, filename_mp4)
    print(f"✅ Downloaded to: {filename_mp4}")

# 💸 Cost estimation
def estimate_cost(seconds, rate=0.02):
    cost = round(seconds * rate, 4)
    print(f"💰 Estimated cost: ${cost} for {seconds}s using Runway gen3")

# 🚀 Main entry
if __name__ == "__main__":
    prompt = "south asains realize they dont have to follow their slave culture from 400 plus years of slavery from fair skin just to translate to grind their life away for major companies. Add elements of pride in their original culture."
    duration = 10
    model = "gen3"

    print("📤 Submitting Runway job...")
    uid = start_runway_job(
        prompt=prompt,
        model=model,
        motion=5,
        width=1344,
        height=768,
        duration=duration,
    )
    print("📦 Job UUID:", uid)

    video_url = poll_runway_status(uid)
    base_filename = f"videos/runway-{model}-{uid}"
    download_video(video_url, base_filename)

    estimate_cost(seconds=duration)
    print("🎉 All done!")
