from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_caching import Cache
from .models import db

# 用户登录管理
login_manager = LoginManager()
login_manager.login_view = 'admin.admin_login'
login_manager.login_message = '请先登录'
login_manager.login_message_category = 'info'

# 数据库迁移
migrate = Migrate()

# 缓存
cache = Cache()

def init_extensions(app):
    """初始化所有Flask扩展"""
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    
    # 用户加载函数
    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id)) 