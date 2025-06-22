class VideoGenerator:
    def __init__(self, provider: str):
        self.provider = provider.lower()
        self.handler = self._get_handler()

    def _get_handler(self):
        if self.provider == 'google':
            return Veo3Handler()
        elif self.provider == 'openai':
            return SoraHandler()
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def generate(self, prompt: str, **kwargs):
        return self.handler.generate(prompt, **kwargs)
