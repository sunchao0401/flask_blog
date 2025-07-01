from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    post_slug = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.Boolean, default=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    level = db.Column(db.Integer, default=0)  # 评论层级，0-3层
    
    # 关系定义
    parent = db.relationship('Comment', remote_side=[id], backref='replies')
    
    def __repr__(self):
        return f'<Comment {self.id} by {self.author} (level {self.level})>'
    
    def get_replies(self):
        """获取直接回复（已批准的）"""
        return self.replies.filter_by(approved=True).order_by(Comment.created_at.asc()).all()
    
    def get_all_replies(self):
        """获取所有直接回复（包括未批准的）"""
        return self.replies.order_by(Comment.created_at.asc()).all()
    
    def get_all_child_comments(self):
        """获取所有子评论（递归）"""
        all_children = []
        for reply in self.replies:
            all_children.append(reply)
            all_children.extend(reply.get_all_child_comments())
        return all_children
    
    def can_reply(self):
        """检查是否可以回复（最多2层嵌套）"""
        return self.level < 2 