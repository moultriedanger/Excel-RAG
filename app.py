import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

# Initialize the model
llm = init_chat_model("gpt-4o-mini", model_provider="openai")

# Ask a question
response = llm.invoke("What is the capital of France?")

print(response.content)