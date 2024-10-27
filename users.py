from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models import User
from schemas import UserSchema

user_bp = Blueprint(
    'users',
    __name__
)

@user_bp.get('/all')
@jwt_required()
def get_all_users():

    claims = get_jwt()

    if claims.get('is_admin'):

        users = User.query.all()

        result = UserSchema().dump(users, many=True)

        return jsonify({
            "users": result
            }), 200
    
    return jsonify({"message":"You are not authorized to access this"}), 401