import time
from google import genai
from google.genai.types import GenerateVideosConfig

class Veo3Handler:
    def __init__(self, model: str = "veo-3.0-generate-preview"):
        self.client = genai.GenerativeModel(model)  # Initializes model directly
        self.model = model

    def generate(self, prompt: str, *,
                 aspect_ratio: str = "16:9",
                 person_generation: str = "allow_adult",
                 sample_count: int = 1,
                 seed: int = None,
                 output_gcs_uri: str = None):
        config = GenerateVideosConfig(
            aspect_ratio=aspect_ratio,
            person_generation=person_generation,
            sample_count=sample_count,
            seed=seed,
            output_gcs_uri=output_gcs_uri,
        )

        operation = self.client.generate_videos(prompt=prompt, config=config)

        # Wait until complete
        while not operation.done:
            time.sleep(15)
            operation = operation.refresh()

        return [video.video.uri for video in operation.result.generated_videos]
