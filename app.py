import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from flask import Flask, request
from langchain_community.utilities import SQLDatabase
from flask import jsonify
from write_query import write_query

load_dotenv()

# Initialize the model
llm = init_chat_model("gpt-4o-mini", model_provider="openai")

# Ask a question
response = llm.invoke("What is the capital of France?")

print(response.content)


app = Flask(__name__)

@app.route('/')
def home():
	print('\033[1;34m' + 'I can talk!' + '\033[0m')

	return 'Hello. I\'m flask'

@app.route("/ai", methods = ["POST"])
def call_ai():
    print("ai called")
    json_response = request.json
    query = json_response.get('query')
    
    llm_response = llm.invoke(query)
    print(llm_response.content)

    return llm_response.content

@app.route("/students", methods= ["GET"])
def get_all_students():
	
    db = SQLDatabase.from_uri("sqlite:///sql.db")
    
    query = write_query("Make the students in aplhabetical order", db, llm)

    return query

if __name__ == '__main__':
	app.run(port=8000)