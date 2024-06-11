# azure.py
import os, sys
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from ..llms import LLMs

class AzureOpenAI(LLMs):
    name = "azure"
    model = ""  # Class variable
    temperature = 0.2  # Class variable
    max_tokens = None  # Class variable

    def __init__(self, **model_kwargs):
        super().__init__()

        self.model_kwargs = model_kwargs  # Store model kwargs

        # AUTHENTICATION
        try:
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
            self.updateLLM()
        except Exception as e:
            print(f"Error updating LLM: {e}")
            sys.exit(1)

    def updateLLM(self):
        try:
            AZURE_OPENAI_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION")
            AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
            AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
            self.llm = AzureChatOpenAI(
                api_key=AZURE_OPENAI_API_KEY,
                api_version=AZURE_OPENAI_API_VERSION,
                azure_endpoint=AZURE_OPENAI_ENDPOINT,
                azure_deployment=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                model_kwargs=self.model_kwargs
            )

            self.chain = self.prompt_template | self.llm | self.output_parser
        except Exception as e:
            print(f"Error initializing LLM or chain: {e}")
            sys.exit(1)

    @classmethod
    def auth(cls, model=None):
        # Azure OpenAI auth happens here
        try:
            if(model):
                auth_status = load_dotenv(f".llms/azure-{model}", override=True)
            else:
                auth_status = load_dotenv(".llms/azure")
            if not auth_status:
                if not (
                    os.environ.get("AZURE_OPENAI_ENDPOINT") and
                    os.environ.get("AZURE_OPENAI_API_KEY") and
                    os.environ.get("AZURE_OPENAI_API_VERSION")
                ):
                    raise EnvironmentError("`AZURE_OPENAI_ENDPOINT` or `AZURE_OPENAI_API_KEY` or `AZURE_OPENAI_API_VERSION` env variables not defined, and `.llms/azure` not available")

        except Exception as e:
            print(f"Error loading authentication for Azure OpenAI: {e}")
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
