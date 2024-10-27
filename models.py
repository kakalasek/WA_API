from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password= db.Column(db.Text())

    def __repr__(self):
        return f"<User {self.username}>"
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password, password)

    @classmethod 
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime(), default=datetime.now())
    text = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"<Post {self.text[:20]}...>"

    def set_user_id(self, username):
        user_id = User.get_user_by_username(username=username).id
        self.user_id = user_id

    @classmethod
    def get_post_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def delete_post_by_id(cls, id):
        cls.query.filter_by(id=id).delete()
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def patch(self, text):
        self.text = text
        db.session.commit()

class TokenBlockList(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    jti = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())

    def __repr__(self):
        return f"<Token {self.jti}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
