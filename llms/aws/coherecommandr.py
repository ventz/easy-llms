# coherecommandr.py
from .aws import AWS

class CohereCommandR(AWS):
    name = "cohere_command_r"
    model = "cohere.command-r-v1:0"  # Override class variable
    chat = False # NOTE: Cohere Command does NOT support Chat

    def __init__(self, temperature=0.2, max_tokens=4096, **model_kwargs):
        super().__init__(**model_kwargs)

        self.model_kwargs = {
            "temperature": temperature,
            "max_tokens": max_tokens,
            **model_kwargs
        }


        try:
            self.updateLLM(self.chat)
        except Exception as e:
            print(f"Error updating LLM in {self.__class__.__name__}: {e}")

