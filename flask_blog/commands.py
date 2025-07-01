import click
from flask.cli import with_appcontext
from .models import db, User
from .services import UserService, PostService

@click.command('init-db')
@with_appcontext
def init_db_command():
    """初始化数据库"""
    db.create_all()
    click.echo('数据库初始化完成')

@click.command('create-admin')
@click.option('--username', default='admin', help='管理员用户名')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='管理员密码')
@with_appcontext
def create_admin_command(username, password):
    """创建管理员用户"""
    user = UserService.create_admin_user(username, password)
    click.echo(f'管理员用户 {user.username} 创建成功')

@click.command('list-posts')
@with_appcontext
def list_posts_command():
    """列出所有文章"""
    posts = PostService.get_all_posts()
    if not posts:
        click.echo('没有找到文章')
        return
    
    click.echo(f'找到 {len(posts)} 篇文章:')
    for post in posts:
        click.echo(f"- {post.get('title', '无标题')} ({post.get('slug', '无slug')})")

@click.command('reset-password')
@click.option('--username', prompt=True, help='用户名')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='新密码')
@with_appcontext
def reset_password_command(username, password):
    """重置用户密码"""
    user = User.query.filter_by(username=username).first()
    if not user:
        click.echo(f'用户 {username} 不存在')
        return
    
    user.set_password(password)
    db.session.commit()
    click.echo(f'用户 {username} 密码重置成功')

@click.command('manage-user')
@click.option('--action', type=click.Choice(['list', 'create', 'update', 'delete']), 
              prompt=True, help='操作类型')
@click.option('--username', help='用户名')
@click.option('--new-username', help='新用户名')
@click.option('--password', help='密码')
@click.option('--is-admin', is_flag=True, help='是否为管理员')
@with_appcontext
def manage_user_command(action, username, new_username, password, is_admin):
    """用户管理命令"""
    if action == 'list':
        users = User.query.all()
        if not users:
            click.echo('没有找到用户')
            return
        
        click.echo('用户列表:')
        for user in users:
            admin_status = '管理员' if user.is_admin else '普通用户'
            click.echo(f"- {user.username} ({admin_status}) - 创建时间: {user.created_at}")
    
    elif action == 'create':
        if not username:
            username = click.prompt('请输入用户名')
        if not password:
            password = click.prompt('请输入密码', hide_input=True, confirmation_prompt=True)
        
        # 检查用户是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            click.echo(f'用户 {username} 已存在')
            return
        
        user = User(username=username, is_admin=is_admin)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f'用户 {username} 创建成功')
    
    elif action == 'update':
        if not username:
            username = click.prompt('请输入要修改的用户名')
        
        user = User.query.filter_by(username=username).first()
        if not user:
            click.echo(f'用户 {username} 不存在')
            return
        
        # 修改用户名
        if new_username:
            existing_user = User.query.filter_by(username=new_username).first()
            if existing_user and existing_user.id != user.id:
                click.echo(f'用户名 {new_username} 已被使用')
                return
            user.username = new_username
            click.echo(f'用户名已修改为: {new_username}')
        
        # 修改密码
        if password:
            user.set_password(password)
            click.echo('密码已修改')
        
        # 修改管理员权限
        if is_admin is not None:
            user.is_admin = is_admin
            admin_status = '管理员' if is_admin else '普通用户'
            click.echo(f'权限已修改为: {admin_status}')
        
        db.session.commit()
        click.echo(f'用户 {user.username} 更新成功')
    
    elif action == 'delete':
        if not username:
            username = click.prompt('请输入要删除的用户名')
        
        user = User.query.filter_by(username=username).first()
        if not user:
            click.echo(f'用户 {username} 不存在')
            return
        
        if click.confirm(f'确定要删除用户 {username} 吗？'):
            db.session.delete(user)
            db.session.commit()
            click.echo(f'用户 {username} 删除成功')

def register_commands(app):
    """注册CLI命令"""
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_admin_command)
    app.cli.add_command(list_posts_command)
    app.cli.add_command(reset_password_command)
    app.cli.add_command(manage_user_command) 