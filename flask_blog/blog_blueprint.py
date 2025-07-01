from flask import Blueprint, render_template, request, redirect, url_for, abort, flash, current_app
from .extensions import cache
from .services import PostService, CommentService
from .forms import CommentForm
from .utils import paginate_items

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
@cache.cached(timeout=300, key_prefix='blog_index')
def index():
    """首页(缓存5分钟)"""
    all_posts = PostService.get_all_posts()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('POSTS_PER_PAGE', 10)
    paginated_posts, total_pages = paginate_items(all_posts, page, per_page)
    return render_template('index.html', 
                         posts=paginated_posts, 
                         all_posts=all_posts,
                         page=page, 
                         total_pages=total_pages, 
                         blog_title=current_app.config['BLOG_TITLE'])

@blog_bp.route('/post/<slug>')
def post(slug):
    """文章详情页"""
    result = PostService.get_post_by_slug(slug)
    if not result:
        abort(404)
    
    metadata, html_content = result
    
    # 获取评论（多层嵌套结构）
    comments = CommentService.get_comments_by_post(slug, approved_only=True)
    
    # 创建评论表单
    form = CommentForm()
    
    return render_template('post.html', 
                         post=metadata, 
                         content=html_content,
                         comments=comments,
                         form=form,
                         blog_title=current_app.config['BLOG_TITLE'])

@blog_bp.route('/post/<slug>/comment', methods=['POST'])
def add_comment(slug):
    """添加评论"""
    # 检查文章是否存在
    result = PostService.get_post_by_slug(slug)
    if not result:
        abort(404)
    
    form = CommentForm()
    if form.validate_on_submit():
        try:
            parent_id = int(form.parent_id.data) if form.parent_id.data else None
            CommentService.add_comment(
                post_slug=slug,
                author=form.author.data,
                email=form.email.data,
                content=form.content.data,
                parent_id=parent_id
            )
            flash('评论提交成功！', 'success')
        except ValueError as e:
            flash(str(e), 'error')
        except Exception as e:
            current_app.logger.error(f"添加评论失败: {e}")
            flash('评论提交失败，请稍后重试', 'error')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{getattr(form, field).label.text}: {error}', 'error')
    
    return redirect(url_for('blog.post', slug=slug))

@blog_bp.route('/category/<category>')
@cache.cached(timeout=300, key_prefix=lambda: f'blog_category_{request.view_args["category"]}')
def category(category):
    """分类页面(缓存5分钟)"""
    all_posts = PostService.get_all_posts()
    posts = [post for post in all_posts if post.get('category', '').lower() == category.lower()]
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('POSTS_PER_PAGE', 10)
    paginated_posts, total_pages = paginate_items(posts, page, per_page)
    # 获取所有分类（去重）
    categories = list({post.get('category') for post in all_posts if post.get('category')})
    return render_template('category.html', 
                         posts=paginated_posts, 
                         category=category,
                         categories=categories,
                         page=page,
                         total_pages=total_pages,
                         blog_title=current_app.config['BLOG_TITLE'])

@blog_bp.route('/search')
def search():
    """搜索页面"""
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('POSTS_PER_PAGE', 10)
    
    results = PostService.search_posts(query) if query else []
    
    paginated_results, total_pages = paginate_items(results, page, per_page)
    
    return render_template('search.html', 
                         query=query, 
                         results=paginated_results, 
                         page=page, 
                         total_pages=total_pages, 
                         blog_title=current_app.config['BLOG_TITLE'])

# 文章详情、评论、分类、搜索等路由可依次迁移 