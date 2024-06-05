# llama370bbinstruct.py
from .aws import AWS

class Llama370bInstruct(AWS):
    name = "llama3_70b_instruct"
    model = "meta.llama3-70b-instruct-v1:0"  # Override class variable

    def __init__(self, temperature=0.2, max_tokens=2048, **model_kwargs):
        super().__init__(**model_kwargs)

        self.model_kwargs = {
            "temperature": temperature,
            "max_gen_len": max_tokens,
            **model_kwargs
        }


        try:
            self.updateLLM()
        except Exception as e:
            print(f"Error updating LLM in {self.__class__.__name__}: {e}")

