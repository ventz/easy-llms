# mistral7binstruct.py
from .aws import AWS

class Mistral7bInstruct(AWS):
    name = "mistral_7b_instruct"
    model = "mistral.mistral-7b-instruct-v0:2"  # Override class variable

    def __init__(self, temperature=0.2, max_tokens=8192, **model_kwargs):
        super().__init__(**model_kwargs)

        self.model_kwargs = {
            "temperature": temperature,
            "max_tokens": max_tokens,
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

