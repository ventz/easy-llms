# gpt35turbo.py
from .openai import OpenAI

class GPT35Turbo(OpenAI):
    name = "gpt_35_turbo"
    model = "gpt-3.5-turbo-1106"  # Override class variable

    def __init__(self, temperature=0.2, max_tokens=4096, **model_kwargs):
        super().__init__(**model_kwargs)
        self.temperature = temperature
        self.max_tokens = max_tokens

        # Override AUTHENTICATION per Model
        try:
            self.auth(self.__class__.name.lower())
        except Exception as e:
            print(f"Error during authentication: {e}")


        try:
            self.updateLLM()
        except Exception as e:
            print(f"Error updating LLM in {self.__class__.__name__}: {e}")

