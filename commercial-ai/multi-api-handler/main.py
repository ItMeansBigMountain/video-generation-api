from VideoGenerator import VideoGenerator

video_api = VideoGenerator(provider="google")
videos = video_api.generate(
    prompt="A neon-lit cyberpunk city with flying cars",
    aspect_ratio="16:9",
    person_generation="allow_adult",
    seed=42,
)

print(videos)  # List of GCS video URIs
