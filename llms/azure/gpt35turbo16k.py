# azure/gpt35turbo16k.py
from .azure import AzureOpenAI

class AzureGPT35Turbo16k(AzureOpenAI):
    name = "azure_gpt_35_turbo_16k"
    model = "gpt-35-turbo-16k"  # Override class variable

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
