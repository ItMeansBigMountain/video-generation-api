import handlers.Veo3Handler as veo
import handlers.sora_handler as sora

class VideoGenerator:
    def __init__(self, provider: str):
        self.provider = provider.lower()
        self.handler = self._get_handler()

    def _get_handler(self):
        if self.provider == 'google':
            return veo.Veo3Handler
        elif self.provider == 'openai':
            return sora.SoraHandler
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def generate(self, prompt: str, **kwargs):
        return self.handler.generate(self, prompt, **kwargs)