# claude1instant.py
from .aws import AWS

class Claude1Instant(AWS):
    name = "claude_1_instant"
    model = "anthropic.claude-instant-v1"  # Override class variable

    def __init__(self, temperature=0.2, max_tokens=4096, **model_kwargs):
        super().__init__(**model_kwargs)

        self.model_kwargs = {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stop_sequences": ["\n\nHuman"],
            **model_kwargs
        }


        try:
            self.updateLLM()
        except Exception as e:
            print(f"Error updating LLM in {self.__class__.__name__}: {e}")

