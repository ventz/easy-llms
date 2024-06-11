# openai.py
import os, sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from ..llms import LLMs

class OpenAI(LLMs):
    name = "openai"  # Class variable
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
            api_key = os.environ.get("OPENAI_API_KEY")
            api_base = os.environ.get("OPENAI_BASE_URL")
            self.llm = ChatOpenAI(
                openai_api_key=api_key,
                openai_api_base=api_base,
                model=self.model,
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
        # OpenAI auth happens here
        try:
            if(model):
                auth_status = load_dotenv(f".llms/openai-{model}", override=True)
            else:
                auth_status = load_dotenv(".llms/openai")
            if not auth_status:
                if not os.environ.get("OPENAI_API_KEY"):
                    raise EnvironmentError("`OPENAI_API_KEY` env variable not defined, and `.llms/openai` not available")

        except Exception as e:
            print(f"Error loading authentication for OpenAI: {e}")
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
