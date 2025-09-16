import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from flask import Flask, request
from langchain_community.utilities import SQLDatabase
from flask import jsonify
from write_query import write_query, State  
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool


load_dotenv()

# Initialize the model
llm = init_chat_model("gpt-4o-mini", model_provider="openai")

# Ask a question
response = llm.invoke("What is the capital of France?")

print(response.content)

app = Flask(__name__)

def connect_to_db():
    try:
        db = SQLDatabase.from_uri("sqlite:///sql.db")  
        return db
    except Exception as e:
        print(f"Failled to connect to db {e}")
        return None

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

@app.route("/query", methods= ["POST"])
def get_all_students():
    print("Request Started")

    json_response = request.json
    question = json_response.get('query')

    db = connect_to_db()

    execute_query_tool = QuerySQLDatabaseTool(db=db)
  
    query = write_query({"question": question}, db, llm)
    
    return query

@app.route("/execute", methods= ["POST"])
def ex_query_test():
    print("Request Started")

    json_response = request.json
    question = json_response.get('query')

    db = connect_to_db()

    execute_query_tool = QuerySQLDatabaseTool(db=db)
  
    query = write_query({"question": question}, db, llm)

    return {"result": execute_query_tool.invoke(query)}



if __name__ == '__main__':
	app.run(port=8000)