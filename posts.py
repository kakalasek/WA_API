from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Post, User

post_bp = Blueprint(
    'posts',
    __name__
)

@post_bp.post('/')
@jwt_required()
def create_post():
    data = request.get_json()
    identity = get_jwt_identity()

    new_post = Post(text=data.get('text'))
    new_post.set_user_id(identity)

    new_post.save()

    return jsonify({"message": f"Post created successfully"}), 201

@post_bp.get('/')
def get_all_posts():
    posts = Post.query.all()

    result = []

    for post in posts:
        user = User.query.filter_by(id=post.user_id).first()
        result.append({
            'user': user.username,
            'date': post.created_at,
            'text': post.text
        })

    return jsonify(result), 200

@post_bp.get('/<int:post_id>')
def get_post(post_id: int):
    post = Post.get_post_by_id(post_id)

    if post is None:
        return jsonify({"error":"Post with this ID does not exist"}), 404
    
    user = User.query.filter_by(id=post.user_id).first()

    return jsonify({
        "user": user.username,
        "date": post.created_at,
        "text": post.text
    }), 200

@post_bp.patch('/<int:post_id>')
@jwt_required()
def patch_post(post_id: int):
    data = request.get_json()
    post = Post.get_post_by_id(post_id)
    identity = get_jwt_identity()

    if post is None:
        return jsonify({"error":"Post with this ID does not exist"}), 404
    
    user = User.query.filter_by(id=post.user_id).first()

    if user.username != identity:
        return jsonify({"message": "You are not authorized to patch post with this ID", "error": "unauthorized_patch"}), 401
    
    post.patch(data.get('text'))

    return jsonify({"message": "Post patched successfully"}), 200

@post_bp.delete('/<int:post_id>')
@jwt_required()
def delete_post(post_id: int):
    post = Post.get_post_by_id(post_id)
    identity = get_jwt_identity()

    if post is None:
        return jsonify({"error":"Post with this ID does not exist"}), 404
    
    user = User.query.filter_by(id=post.user_id).first()

    if user.username != identity:
        return jsonify({"message": "You are not authorized to delete post with this ID", "error": "unauthorized_delete"}), 401
    
    Post.delete_post_by_id(post.id)

    return jsonify({"message": "Post deleted successfully"}), 200