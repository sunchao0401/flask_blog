from flask import Blueprint, render_template, request, redirect, url_for, abort, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .services import PostService, CommentService, UserService
from .models import Comment
from .forms import LoginForm, PostEditForm
from .decorators import admin_required
from .utils import paginate_items

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    """管理员登录"""
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin_comments'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = UserService.authenticate_user(form.username.data, form.password.data)
        if user and user.is_admin:
            login_user(user)
            flash('登录成功', 'success')
            next_url = request.args.get('next') or url_for('admin.admin_comments')
            return redirect(next_url)
        else:
            flash('用户名或密码错误', 'error')
    
    return render_template('login.html', 
                         form=form,
                         blog_title=current_app.config['BLOG_TITLE'])

@admin_bp.route('/logout')
@login_required
def admin_logout():
    """管理员登出"""
    logout_user()
    flash('已退出登录', 'success')
    return redirect(url_for('admin.admin_login'))

@admin_bp.route('/comments')
@admin_required
def admin_comments():
    """评论管理"""
    comments = Comment.query.order_by(Comment.created_at.desc()).all()
    return render_template('admin_comments.html', 
                         comments=comments, 
                         blog_title=current_app.config['BLOG_TITLE'])

@admin_bp.route('/comments/<int:comment_id>/<action>')
@admin_required
def manage_comment(comment_id, action):
    """管理评论（批准/拒绝）"""
    if action not in ['approve', 'reject']:
        abort(400)
    
    try:
        if action == 'approve':
            CommentService.approve_comment(comment_id)
            flash('评论已批准', 'success')
        else:
            CommentService.reject_comment(comment_id)
            flash('评论已拒绝', 'success')
    except Exception as e:
        current_app.logger.error(f"管理评论失败: {e}")
        flash('操作失败', 'error')
    
    return redirect(url_for('admin.admin_comments'))

@admin_bp.route('/comments/<int:comment_id>/delete')
@admin_required
def delete_comment(comment_id):
    """删除评论"""
    try:
        CommentService.delete_comment(comment_id)
        flash('评论已删除', 'success')
    except Exception as e:
        current_app.logger.error(f"删除评论失败: {e}")
        flash('删除失败', 'error')
    
    return redirect(url_for('admin.admin_comments'))

@admin_bp.route('/posts')
@admin_required
def admin_posts():
    """文章管理"""
    posts = PostService.get_all_posts()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('ADMIN_POSTS_PER_PAGE', 50)
    
    paginated_posts, total_pages = paginate_items(posts, page, per_page)
    
    return render_template('admin_posts.html', 
                         posts=paginated_posts, 
                         page=page, 
                         total_pages=total_pages, 
                         blog_title=current_app.config['BLOG_TITLE'])

@admin_bp.route('/posts/<slug>/edit', methods=['GET', 'POST'])
@admin_required
def edit_post(slug):
    """编辑文章元数据"""
    result = PostService.get_post_by_slug(slug)
    if not result:
        abort(404)
    
    metadata, _ = result
    form = PostEditForm()
    
    if request.method == 'GET':
        # 填充表单数据
        form.title.data = metadata.get('title', '')
        form.date.data = metadata.get('date', '')
        form.author.data = metadata.get('author', '')
        form.category.data = metadata.get('category', '')
        form.description.data = metadata.get('description', '')
        form.tags.data = metadata.get('tags', '')
        form.top.data = metadata.get('top', False)
    
    if form.validate_on_submit():
        try:
            # 更新文章元数据
            PostService.update_post_metadata(slug, {
                'title': form.title.data,
                'date': form.date.data,
                'author': form.author.data,
                'category': form.category.data,
                'description': form.description.data,
                'tags': form.tags.data,
                'top': form.top.data
            })
            flash('文章元数据已保存', 'success')
            return redirect(url_for('admin.admin_posts'))
        except Exception as e:
            current_app.logger.error(f"更新文章元数据失败: {e}")
            flash('保存失败', 'error')
    
    return render_template('edit_post.html', 
                         slug=slug, 
                         form=form,
                         blog_title=current_app.config['BLOG_TITLE'])

# 后台相关路由可依次迁移 