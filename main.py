from flask import Flask, request
from dotenv import load_dotenv
from jsonschema import validate

schema = {
    "type": "object",
    "properties": {
        "author": {"type": "string"},
        "date": {"type": "string"},
        "text": {"type": "string"}
    }
}

load_dotenv()

app = Flask(__name__)

@app.route('/api/blog', methods=['POST'])
def create_blog():
    return validate(request.json, schema=schema)

@app.route('/api/blog', methods=['GET'])
def get_all_blogs():
    pass

@app.route('/api/blog/<int:blog_id>', methods=['GET'])
def get_blog():
    pass

@app.route('/api/blog/<int:blog_id>', methods=['DELETE'])
def delete_blog():
    pass

@app.route('/api/blog/<int:blog_id>', methods=['PATCH'])
def update_blog():
    pass