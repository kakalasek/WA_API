from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from models import db, Post, User
import os
from werkzeug.security import generate_password_hash, check_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.urandom(24)

auth = HTTPBasicAuth()

db.init_app(app)
with app.app_context():
    db.create_all()

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return username

@app.route('/api/register', methods=['POST'])
def register():
    if User.query.filter_by(username=request.json["username"]).first():
        return "User already registered", 400
    
    user = User(username=request.json["username"], password=generate_password_hash(request.json["password"]))

    db.session.add(user)
    db.session.commit()

    return "User registered successfuly", 201

@app.route('/api/exists', methods=['POST'])
def exists():
    if not User.query.filter_by(username=request.json["username"]).first():
        return "User not registered", 400

    user = User.query.filter_by(username=request.json["username"]).first()

    if not check_password_hash(user.password, request.json["password"]):
        return "Wrong password", 400
    
    return "User exists", 200


@app.route('/api/blog', methods=['POST'])
@auth.login_required
def create_post():
    try:
        user = User.query.filter_by(username=auth.current_user()).first()
        new_post = Post(user_id=user.id, text=request.json['text'])
        db.session.add(new_post)
        db.session.commit()
        return "Post created successfuly", 201
    except Exception as e:
        return "There has been a problem with creating your post", 400
    

@app.route('/api/blog', methods=['GET'])
def get_all_posts():
    posts = [] 
    for post in Post.query.all():
        author = User.query.filter_by(id=post.user_id).first()
        posts.append({
            'author': author.username,
            'date': post.create_date,
            'text': post.text
        })
    return posts, 200

@app.route('/api/blog/<int:blog_id>', methods=['GET'])
@auth.login_required
def get_post(blog_id: int):
    user = User.query.filter_by(username=auth.current_user()).first()
    post = Post.query.get(blog_id)
    if not post:
        return "No post was found with this id", 400
    if post.user_id != user.id:
        return "You can only access your posts", 401

    post_json = {
        'author': user.username,
        'date': post.create_date,
        'text': post.text
    }    

    return post_json, 200

@app.route('/api/blog/<int:blog_id>', methods=['DELETE'])
@auth.login_required
def delete_post(blog_id: int):
    user = User.query.filter_by(username=auth.current_user()).first()
    post = Post.query.get(blog_id)

    if not post:
        return "No post was found with this id", 400
    if post.user_id != user.id:
        return "You can only delete your posts", 401

    Post.query.filter_by(id=blog_id).delete()
    db.session.commit()
    return "Post successfuly deleted", 200    

@app.route('/api/blog/<int:blog_id>', methods=['PATCH'])
@auth.login_required
def update_post(blog_id: int):
    new_text = request.get_json()['text']

    user = User.query.filter_by(username=auth.current_user()).first()
    post = Post.query.filter_by(id=blog_id).first()

    if not post:
        return "No post was found with this id", 400
    if post.user_id != user.id:
        return "You can only update your posts", 401

    post.text = new_text
    db.session.commit()

    return "Post successfuly updated", 200

if __name__ == "__main__":
    app.run(port=5020, debug=True)