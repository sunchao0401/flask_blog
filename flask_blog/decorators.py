from functools import wraps
from flask import redirect, url_for, flash, request
from flask_login import current_user

def admin_required(f):
    """管理员权限装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('admin.admin_login', next=request.url))
        if not current_user.is_admin:
            flash('需要管理员权限', 'error')
            return redirect(url_for('blog.index'))
        return f(*args, **kwargs)
    return decorated_function 