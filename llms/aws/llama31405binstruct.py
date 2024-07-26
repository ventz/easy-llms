# llama31405bbinstruct.py
from .aws import AWS

class Llama31405bInstruct(AWS):
    name = "llama3_1_405b_instruct"
    model = "meta.llama3-1-405b-instruct-v1:0"  # Override class variable

    def __init__(self, temperature=0.2, max_tokens=2048, **model_kwargs):
        super().__init__(**model_kwargs)

        self.model_kwargs = {
            "temperature": temperature,
            "max_gen_len": max_tokens,
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

