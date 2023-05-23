from flask import Flask, request, session
from flask_session import Session
import os
from dotenv import load_dotenv
from core.main import run_llm
from langchain.memory import ConversationBufferMemory
from redis import Redis

load_dotenv('../.env')

app = Flask(__name__)
#app.secret_key = os.environ.get("FLASK_SECRET_KEY")
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis(host='localhost', port=6379)

Session(app)


@app.route("/api/query", methods=["POST"])
def query():
    if "agent_memory" not in session:
        session["agent_memory"] =  ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    payload = request.data.decode('utf-8')
    result = run_llm(question=payload, memory=session["agent_memory"])
    return result

if __name__ == "__main__":
    app.run(debug=True)