# aws.py
import os, sys, boto3
from dotenv import load_dotenv
from langchain_aws import ChatBedrock
from langchain_aws import BedrockLLM
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from ..llms import LLMs

class AWS(LLMs):
    name = "aws" # Class variable
    model = "" # Class variable
    temperature = 0.2  # Class variable

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

    def updateLLM(self, chat=True):
        try:
            ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
            SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
            REGION = os.environ.get("AWS_REGION")
            session = boto3.Session(aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
            client = session.client("bedrock-runtime", region_name=REGION)

            self.llm = (ChatBedrock if chat else BedrockLLM)(
                client=client,
                region_name=REGION,
                model_id=self.model,
                model_kwargs=self.model_kwargs
            )

            self.chain = self.prompt_template | self.llm | self.output_parser
        except Exception as e:
            print(f"Error initializing LLM or chain: {e}")
            sys.exit(1)

    @classmethod
    def auth(cls, model=None):
        # AWS Bedrock auth happens here
        try:
            if(model):
                auth_status = load_dotenv(f".llms/aws-{model}", override=True)
            else:
                auth_status = load_dotenv(".llms/aws")
            if not auth_status:
                if not (
                    os.environ.get("AWS_ACCESS_KEY_ID") and
                    os.environ.get("AWS_SECRET_ACCESS_KEY") and
                    os.environ.get("AWS_REGION")
                ):
                    raise EnvironmentError("`AWS_ACCESS_KEY_ID` or `AWS_SECRET_ACCESS_KEY` or `AWS_REGION` env variables not defined, and `.llms/aws` not available")

        except Exception as e:
            print(f"Error loading authentication for AWS: {e}")
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
