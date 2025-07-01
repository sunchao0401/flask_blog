import os
from flask import Flask
from .config import config
from .extensions import init_extensions
from .models import db

def create_app(config_name=None):
    """应用工厂函数"""
    if config_name is None:
        config_name = 'default'
    
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # 确保必要的目录存在
    os.makedirs(app.config['POSTS_DIR'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 初始化扩展
    init_extensions(app)
    
    # 注册蓝图
    from .blog_blueprint import blog_bp
    from .admin_blueprint import admin_bp
    
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # 注册错误处理器
    register_error_handlers(app)
    
    # 注册CLI命令
    from .commands import register_commands
    register_commands(app)
    
    # 初始化数据库
    with app.app_context():
        init_database(app)
    
    return app

def register_error_handlers(app):
    """注册错误处理器"""
    from flask import render_template
    
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html', blog_title=app.config['BLOG_TITLE']), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html', blog_title=app.config['BLOG_TITLE']), 500

def init_database(app):
    """初始化数据库"""
    from .models import User
    from .services import UserService
    
    # 创建所有表
    db.create_all()
    
    # 创建默认管理员用户
    admin_password = 'admin1234'
    UserService.create_admin_user('admin', admin_password) 