# ollama.py
import os, sys
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOllama
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from ..llms import LLMs

class OllamaLLM(LLMs):
    name = "ollama"  # Class variable
    model = ""  # Class variable
    temperature = 0.2  # Class variable
    max_tokens = None  # Class variable

    def __init__(self, model, chat=True, model_auth=None, **model_kwargs):
        super().__init__()

        self.model = model
        self.model_kwargs = model_kwargs  # Store model kwargs

        # AUTHENTICATION
        try:
            if(model_auth):
                self.auth(model)
            else:
                self.auth()
        except Exception as e:
            print(f"Error during authentication: {e}")

        # Initialize the output parser here if it's going to be static
        self.output_parser = StrOutputParser()

        # If the prompt template is static, initialize it here
        try:
            self.prompt_template = ChatPromptTemplate.from_messages([
                SystemMessage(content="You are a helpful assistant. Answer all questions to the best of your ability."),
                MessagesPlaceholder(variable_name="messages"),
            ])
        except Exception as e:
            print(f"Error initializing prompt template: {e}")
            sys.exit(1)

        try:
            self.updateLLM(chat)
        except Exception as e:
            print(f"Error updating LLM: {e}")
            sys.exit(1)

    def updateLLM(self, chat=True):
        try:
            base_url = os.environ.get("OLLAMA_BASE_URL")
            self.llm = (ChatOllama if chat else Ollama)(
                model=self.model,
                base_url=base_url,
                temperature=self.temperature,
                num_predict=self.max_tokens,
                **self.model_kwargs
            )

            self.chain = self.prompt_template | self.llm | self.output_parser
        except Exception as e:
            print(f"Error initializing LLM or chain: {e}")
            sys.exit(1)

    @classmethod
    def auth(cls, model=None):
        # Ollama does not have auth - however it needs a "base_url" via OLLAMA_BASE_URL
        # By default it will assume "localhost", but we are going to use this as a requirement
        try:
            if(model):
                auth_status = load_dotenv(f".llms/ollama-{model}", override=True)
            else:
                auth_status = load_dotenv(".llms/ollama")
            if not auth_status:
                if not os.environ.get("OLLAMA_BASE_URL"):
                    raise EnvironmentError("`OLLAMA_BASE_URL` env variable not defined, and `.llms/ollama` not available")

        except Exception as e:
            print(f"Error loading authentication for Ollama: {e}")
            sys.exit(1)

    def run(self, prompt):
        try:
            response = self.chain.invoke({
                "messages": [
                    HumanMessage(content=prompt),
                ],
            })
            return response
        except Exception as e:
            print(f"Error invoking the chain: {e}")
            return None
