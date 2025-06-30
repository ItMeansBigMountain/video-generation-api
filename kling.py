import os
import time
import requests
import jwt
from dotenv import load_dotenv

load_dotenv()

# === JWT TOKEN ===
def encode_jwt_token(ak, sk):
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": ak,
        "exp": int(time.time()) + 1800,
        "nbf": int(time.time()) - 5
    }
    token = jwt.encode(payload, sk, algorithm="HS256", headers=headers)
    return token if isinstance(token, str) else token.decode("utf-8")

# === CREATE VIDEO TASK ===
def create_video_task(
    prompt: str,
    model_name: str = "kling-v2-1-master",
    negative_prompt: str = "",
    duration: int = 5,  # 5 or 10
    aspect_ratio: str = "16:9",
    cfg_scale: float = 0.5,
    mode: str = "pro",  # "std" or "pro"
    camera_type: str = None,  # or "simple", etc.
    camera_config: dict = None,
    external_task_id: str = None
):
    payload = {
        "prompt": prompt,
        "model_name": model_name,
        "negative_prompt": negative_prompt,
        "duration": int(duration),
        "aspect_ratio": aspect_ratio,
        "cfg_scale": float(cfg_scale),
        "mode": mode
    }

    if camera_type:
        payload["camera_control"] = {"type": camera_type}
        if camera_type == "simple" and camera_config:
            payload["camera_control"]["config"] = camera_config

    if external_task_id:
        payload["external_task_id"] = external_task_id

    print("📦 Sending Payload...")
    res = requests.post(BASE_URL, headers=HEADERS, json=payload)
    res.raise_for_status()
    response = res.json()

    if response["code"] != 0:
        raise Exception(f"❌ API Error: {response['message']}")

    task_id = response["data"]["task_id"]
    print(f"✅ Task Created: {task_id}")
    return task_id

# === POLL TASK ===
def poll_task_result(task_id: str, interval=10, timeout=300):
    url = f"{BASE_URL}/{task_id}"
    start = time.time()

    while time.time() - start < timeout:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        response = res.json()

        if response["code"] != 0:
            raise Exception(f"❌ Polling Error: {response['message']}")

        data = response["data"]
        status = data.get("task_status")
        print(f"⏳ Status: {status}")

        if status == "succeed":
            video_info = data["task_result"]["videos"][0]
            print("🎉 Success!")
            return {
                "video_url": video_info["url"],
                "duration": video_info["duration"],
                "created_at": data["created_at"],
                "updated_at": data["updated_at"]
            }

        elif status == "failed":
            raise Exception(f"❌ Generation Failed: {data.get('task_status_msg')}")

        time.sleep(interval)

    raise TimeoutError("⌛ Polling timed out.")

# === MAIN ===
ak = os.getenv("KLING_API_KEY")
sk = os.getenv("KLING_SECRET_KEY")

API_BEARER_TOKEN = encode_jwt_token(ak, sk)
BASE_URL = "https://api-singapore.klingai.com/v1/videos/text2video"
HEADERS = {
    "Authorization": f"Bearer {API_BEARER_TOKEN}",
    "Content-Type": "application/json"
}

if __name__ == "__main__":
    task_id = create_video_task(
        prompt="An astronaut walking through a neon-lit jungle on an alien planet, cinematic, colorful lighting",
        model_name="kling-v2-1-master",
        duration=10,
        aspect_ratio="16:9",
        cfg_scale=0.7,
        mode="pro",
        camera_type="forward_up"
    )

    result = poll_task_result(task_id)
    print("🎬 Final Video URL:", result["video_url"])
    print("🕐 Duration:", result["duration"], "seconds")
