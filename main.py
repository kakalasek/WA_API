from flask import Flask, request, jsonify
from jsonschema import validate
from models import db, Post
import os
import json

schema = {
    "type": "object",
    "properties": {
        "author": {"type": "string"},
        "text": {"type": "string"}
    }
}

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/api/blog', methods=['POST'])
def create_post():
    try:
        validate(request.json, schema=schema)
        new_post = Post(author=request.json['author'], text=request.json['text'])
        db.session.add(new_post)
        db.session.commit()
        return "Post created successfuly", 201
    except Exception as e:
        return "There has been a problem with creating your post", 400
    

@app.route('/api/blog', methods=['GET'])
def get_all_posts():
    posts = [] 
    for post in Post.query.all():
        posts.append({
            'author': post.author,
            'date': post.create_date,
            'text': post.text
        })
    return posts, 200

@app.route('/api/blog/<int:blog_id>', methods=['GET'])
def get_post():
    pass

@app.route('/api/blog/<int:blog_id>', methods=['DELETE'])
def delete_post():
    pass

@app.route('/api/blog/<int:blog_id>', methods=['PATCH'])
def update_post():
    pass

if __name__ == "__main__":
    app.run(port=5020, debug=True)