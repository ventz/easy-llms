# claude35sonnet.py
from .aws import AWS

class Claude35Sonnet(AWS):
    name = "claude_35_sonnet"
    model = "anthropic.claude-3-5-sonnet-20240620-v1:0"  # Override class variable

    def __init__(self, temperature=0.2, max_tokens=4096, **model_kwargs):
        super().__init__(**model_kwargs)

        self.model_kwargs = {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stop_sequences": ["\n\nHuman"],
            **model_kwargs
        }

        # Override AUTHENTICATION per Model
        try:
            self.auth(self.__class__.name.lower())
        except Exception as e:
            print(f"Error during authentication: {e}")


        try:
            self.updateLLM()
        except Exception as e:
            print(f"Error updating LLM in {self.__class__.__name__}: {e}")

