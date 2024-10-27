from flask import Flask, jsonify
from extensions import db, jwt
from auth import auth_bp
from users import user_bp
from posts import post_bp
from about import about_bp
from models import User, TokenBlockList

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'kdjfkshfiehkshdhfkhdfhdsh'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['JWT_SECRET_KEY'] = 'dkfh483y548dhfkly203894293kdhf2'

    # Initialize extensions
    db.init_app(app)
    with app.app_context():
        db.create_all()
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(post_bp, url_prefix='/api/blog')
    app.register_blueprint(about_bp, url_prefix='/api/about')

    # Load user
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_headers, jwt_data):
        
        identity = jwt_data['sub']

        return User.query.filter_by(username=identity).one_or_none()
    
    # Additional claims
    @jwt.additional_claims_loader
    def make_additional_claims(identity):
        
        if identity == "JohnDoe":
            return {"is_admin": True}
        return ({"is_admin": False})

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({"message": "Token has expired", "error":"token_expired"}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message":"Signature verification failed", "error":"invalid_token"}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message":"Request does not contain a valid token", "error":"authorization_required"}), 401
    
    @jwt.token_in_blocklist_loader
    def token_in_blocklist_callback(jwt_header, jwt_data):
        jti = jwt_data['jti']

        token = db.session.query(TokenBlockList).filter(TokenBlockList.jti == jti).scalar()

        return token is not None

    return app
