import os
from datetime import timedelta

class Config:
    """基础配置类"""
    # 基础配置
    SECRET_KEY = 'dev-secret-key-change-in-production'
    BLOG_TITLE = 'My Markdown Blog'
    POSTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'posts')
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 分页配置
    POSTS_PER_PAGE = 10
    ADMIN_POSTS_PER_PAGE = 50
    
    # 安全配置
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads')
    
    # 日志配置
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'flask_blog.log'

    # 缓存配置
    CACHE_TYPE = 'RedisCache'  # 默认使用 Redis 缓存
    CACHE_DEFAULT_TIMEOUT = 300  # 默认5分钟
    # Redis缓存配置
    CACHE_REDIS_HOST = '192.168.5.8'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    
    @classmethod
    def init_app(cls, app):
        pass


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    
    @classmethod
    def init_app(cls, app):
        # 生产环境日志配置
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.debug and not app.testing:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler(
                'logs/flask_blog.log', 
                maxBytes=10240000, 
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('Flask Blog startup')

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 