from flask import Flask, request, jsonify
from flask_login import LoginManager
from jsonschema import validate
from models import db, Post, User
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
app.config

db.init_app(app)
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)

@app.route('/api/login')
def login():
    pass

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
def get_post(blog_id: int):
    post = Post.query.get(blog_id)
    if not post:
        return "No post was found with this id", 400

    post_json = {
        'author': post.author,
        'date': post.create_date,
        'text': post.text
    }    

    return post_json, 200

@app.route('/api/blog/<int:blog_id>', methods=['DELETE'])
def delete_post(blog_id: int):
    deleted = Post.query.filter_by(id=blog_id).delete()
    db.session.commit()
    if not deleted:
        return "No rows were deleteed", 200
    return "Post successfuly deleted", 200    

@app.route('/api/blog/<int:blog_id>', methods=['PATCH'])
def update_post(blog_id: int):
    new_text = request.get_json()['text']

    post = Post.query.filter_by(id=blog_id).first()

    if not post:
        return "No post was found with this id", 400

    post.text = new_text
    db.session.commit()

    return "Post successfuly updated", 200

if __name__ == "__main__":
    app.run(port=5020, debug=True)