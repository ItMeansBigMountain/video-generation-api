import requests
import time
import os
from dotenv import load_dotenv


# #### API NOTE #### #### ### #### #### ### ####
    # 6/29/2025 : API COMING SOON

# KLING DOCUMENTATION:
    # https://app.klingai.com/global/dev/document-api/quickStart/productIntroduction/overview?gad_source=1&gad_campaignid=22687195893&gbraid=0AAAAA-NKDyDnxcGTokjU8PU_uIlk09442&gclid=Cj0KCQjwyIPDBhDBARIsAHJyyVht_75JkSRf8KDkrkRTSKb9a8YS-BPUmEy1lL2CFs_67GXtcos6BaQaApoBEALw_wcB

# #### ### #### #### ### #### #### ### #### #### ### #### 




load_dotenv()
API_KEY = os.getenv("KLING_API_KEY")
BASE_URL = "https://api.klingai.com/api/v1/video/t2v"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def create_kling_video(prompt, duration=5, aspect_ratio="16:9"):
    data = {
        "prompt": prompt,
        "duration": duration,
        "ratio": aspect_ratio
    }
    response = requests.post(f"{BASE_URL}/submit", headers=headers, json=data)
    response.raise_for_status()
    print(response.text)
    return response.json().get("task_id")

def poll_kling_video(task_id, interval=10, timeout=300):
    start = time.time()
    while time.time() - start < timeout:
        res = requests.get(f"{BASE_URL}/result", headers=headers, params={"task_id": task_id})
        res.raise_for_status()
        result = res.json()
        if result.get("status") == "succeeded":
            return result["video_url"]
        elif result.get("status") == "failed":
            raise Exception("Video generation failed")
        print("⏳", result.get("status"))
        time.sleep(interval)
    raise TimeoutError("Polling timed out")

if __name__ == "__main__":
    task = create_kling_video("A cat sleeping on a sunny window ledge", duration=5)
    print("Task ID:", task)
    video_url = poll_kling_video(task)
    print("🎥 Video URL:", video_url)
