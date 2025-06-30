import os
import time
import requests
from dotenv import load_dotenv
import time
import jwt


load_dotenv()


def encode_jwt_token(ak, sk):
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": ak,
        "exp": int(time.time()) + 1800, # The valid time, in this example, represents the current time+1800s(30min)
        "nbf": int(time.time()) - 5 # The time when it starts to take effect, in this example, represents the current time minus 5s
    }
    token = jwt.encode(payload, sk, algorithm="HS256", headers=headers)
    return token if isinstance(token, str) else token.decode("utf-8")

def create_video_task(
    prompt: str,
    model_name: str = "kling-v2-1-master",
    negative_prompt: str = "",
    duration: str = "5",  # "5" or "10"
    aspect_ratio: str = "16:9",
    cfg_scale: float = 0.5,
    mode: str = "pro",  # "std" or "pro"
    camera_type: str = "forward_up",  # use "simple" to use camera_config
    camera_config: dict = None,
    external_task_id: str = None
):
    payload = {
        "prompt": prompt,
        "model_name": model_name,
        "negative_prompt": negative_prompt,
        "duration": duration,
        "aspect_ratio": aspect_ratio,
        "cfg_scale": cfg_scale,
        "mode": mode,
    }

    if external_task_id:
        payload["external_task_id"] = external_task_id

    # Handle camera
    if camera_type:
        payload["camera_control"] = {
            "type": camera_type
        }
        if camera_type == "simple" and camera_config:
            payload["camera_control"]["config"] = camera_config

    res = requests.post(BASE_URL, headers=HEADERS, json=payload)
    res.raise_for_status()
    response = res.json()
    
    if response["code"] != 0:
        raise Exception(f"❌ API Error: {response['message']}")
    
    task_id = response["data"]["task_id"]
    print(f"✅ Task Created: {task_id}")
    return task_id

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


ak = os.getenv("KLING_API_KEY")
sk = os.getenv("KLING_SECRET_KEY")

API_BEARER_TOKEN = encode_jwt_token(ak, sk)
BASE_URL = "https://api-singapore.klingai.com/v1/videos/text2video"
# print("🔐 JWT:", API_BEARER_TOKEN[:10], "...", API_BEARER_TOKEN[-10:])
HEADERS = {
    "Authorization": f"Bearer {API_BEARER_TOKEN}",
    "Content-Type": "application/json"
}

if __name__ == "__main__":
    task_id = create_video_task(
        prompt="An astronaut walking through a neon-lit jungle on an alien planet, cinematic, colorful lighting",
        model_name="kling-v2-1-master",
        duration="10",
        aspect_ratio="16:9",
        cfg_scale=0.7,
        mode="pro",
        camera_type="forward_up"
    )

    result = poll_task_result(task_id)
    print("🎬 Final Video URL:", result["video_url"])
    print("🕐 Duration:", result["duration"], "seconds")