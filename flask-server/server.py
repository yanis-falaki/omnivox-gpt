from flask import Flask, session
import os
from dotenv import load_dotenv
from core.main import run_llm

load_dotenv('../.env')

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")


@app.route("/query")
def index():
    return "hello"


if __name__ == "__main__":
    app.run(debug=True)