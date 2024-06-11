# j2ultra.py
from .aws import AWS

class J2Ultra(AWS):
    name = "j2_ultra"
    model = "ai21.j2-ultra-v1"  # Override class variable
    chat = False # NOTE: A21 J2 does NOT support Chat

    def __init__(self, temperature=0.2, max_tokens=2048, **model_kwargs):
        super().__init__(**model_kwargs)

        self.model_kwargs = {
            "temperature": temperature,
            "maxTokens": max_tokens,
            **model_kwargs
        }

        # Override AUTHENTICATION per Model
        try:
            self.auth(self.__class__.name.lower())
        except Exception as e:
            print(f"Error during authentication: {e}")


        try:
            self.updateLLM(self.chat)
        except Exception as e:
            print(f"Error updating LLM in {self.__class__.__name__}: {e}")

