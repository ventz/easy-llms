# gemini.py
import os, sys, json
from google.oauth2 import service_account
from dotenv import load_dotenv

# https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-attributes
from langchain_google_vertexai import ChatVertexAI, HarmBlockThreshold, HarmCategory
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from ..llms import LLMs

class Google(LLMs):
    name = "google" # Class variable
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
            GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
            GCP_REGION = os.environ.get("GCP_REGION")
            GCP_CREDENTIALS_JSON = os.environ.get("GCP_CREDENTIALS_JSON")
            credentials = service_account.Credentials.from_service_account_info(json.loads(GCP_CREDENTIALS_JSON))
            scoped_creds = credentials.with_scopes(["https://www.googleapis.com/auth/cloud-platform"])

            self.llm = ChatVertexAI(
                model_name=self.model,
                convert_system_message_to_human=False,
                project=GCP_PROJECT_ID,
                location=GCP_REGION,
                credentials=scoped_creds,
                max_output_tokens=self.max_tokens,
                temperature=self.temperature,
                model_kwargs=self.model_kwargs
            )

            self.chain = self.prompt_template | self.llm | self.output_parser

        except Exception as e:
            print(f"Error initializing LLM or chain: {e}")
            sys.exit(1)

    @classmethod
    def auth(cls, model=None):
        # Google auth happens here
        try:
            if(model):
                auth_status = load_dotenv(f".llms/google-{model}", override=True)
            else:
                auth_status = load_dotenv(".llms/google")
            if not auth_status:
                if not (
                    os.environ.get("GCP_PROJECT_ID") and
                    os.environ.get("GCP_REGION") and
                    os.environ.get("GCP_CREDENTIALS_JSON")
                ):
                    raise EnvironmentError("`GCP_PROJECT_ID` or `GCP_REGION` or `GCP_CREDENTIALS_JSON` env variables not defined, and `.llms/google` not available")

        except Exception as e:
            print(f"Error loading authentication for Google: {e}")
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
