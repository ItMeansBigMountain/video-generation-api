from VideoGenerator import VideoGenerator

video_api = VideoGenerator(provider="google")
videos = video_api.generate(
    prompt="A neon-lit cyberpunk city with flying cars",
    aspect_ratio="16:9",
    person_generation="allow_adult",
    sample_count=1,
    seed=42,
    output_gcs_uri="gs://your-bucket/videos/"
)

print(videos)  # List of GCS video URIs
