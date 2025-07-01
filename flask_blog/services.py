import os
from datetime import datetime
from pathlib import Path
import markdown
from flask import current_app
from .models import db, User, Comment
from .extensions import cache

class PostService:
    """文章服务类"""
    
    @staticmethod
    def parse_markdown_file(file_path):
        """解析Markdown文件，提取元数据和HTML内容"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 分离元数据和内容
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                metadata_text = parts[1]
                markdown_content = parts[2]
            else:
                metadata_text = ""
                markdown_content = content
        else:
            metadata_text = ""
            markdown_content = content
        
        # 解析元数据
        metadata = {}
        if metadata_text:
            for line in metadata_text.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
        
        # 处理特殊字段
        if 'top' in metadata:
            val = str(metadata['top']).lower()
            metadata['top'] = val in ['true', '1', 'yes', 'on']
        else:
            metadata['top'] = False
        
        # 设置默认值
        if 'title' not in metadata:
            metadata['title'] = Path(file_path).stem.replace('_', ' ').title()
        if 'date' not in metadata:
            file_time = os.path.getmtime(file_path)
            metadata['date'] = datetime.fromtimestamp(file_time).strftime('%Y-%m-%d')
        
        # 转换为HTML
        html_content = markdown.markdown(
            markdown_content,
            extensions=['fenced_code', 'tables', 'toc']
        )
        
        return metadata, html_content
    
    @staticmethod
    @cache.cached(timeout=21600, key_prefix='get_all_posts')
    def get_all_posts():
        """获取所有文章（缓存6小时）"""
        posts = []
        posts_dir = current_app.config['POSTS_DIR']
        
        if not os.path.exists(posts_dir):
            return posts
            
        for filename in os.listdir(posts_dir):
            if filename.endswith('.md'):
                file_path = os.path.join(posts_dir, filename)
                try:
                    metadata, _ = PostService.parse_markdown_file(file_path)
                    metadata['filename'] = filename
                    metadata['slug'] = filename.replace('.md', '')
                    posts.append(metadata)
                except Exception as e:
                    current_app.logger.error(f"Error parsing {filename}: {e}")
                    continue
        
        # 按置顶和日期排序
        posts.sort(key=lambda x: (x.get('top', False), x.get('date', '')), reverse=True)
        return posts
    
    @staticmethod
    @cache.memoize(timeout=21600)
    def get_post_by_slug(slug):
        """根据slug获取文章（缓存6小时，基于slug参数自动生成缓存键）"""
        file_path = os.path.join(current_app.config['POSTS_DIR'], f'{slug}.md')
        if not os.path.exists(file_path):
            return None
        
        try:
            metadata, html_content = PostService.parse_markdown_file(file_path)
            metadata['slug'] = slug
            return metadata, html_content
        except Exception as e:
            current_app.logger.error(f"Error parsing post {slug}: {e}")
            return None
    
    @staticmethod
    def update_post_metadata(slug, new_metadata):
        """更新文章元数据"""
        file_path = os.path.join(current_app.config['POSTS_DIR'], f'{slug}.md')
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文章 {slug} 不存在")
        
        # 读取原文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 分离元数据和内容
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                markdown_content = parts[2]
            else:
                markdown_content = content
        else:
            markdown_content = content
        
        # 构建新的元数据
        meta_lines = []
        for key, value in new_metadata.items():
            if value is not None and value != '':
                if key == 'top':
                    meta_lines.append(f"{key}: {str(value).lower()}")
                else:
                    meta_lines.append(f"{key}: {value}")
        
        # 重新构建文件内容
        new_metadata_text = '\n'.join(meta_lines)
        new_content = f"---\n{new_metadata_text}\n---\n{markdown_content.lstrip()}"
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    @staticmethod
    def search_posts(query):
        """搜索文章"""
        if not query.strip():
            return []
        
        results = []
        posts_dir = current_app.config['POSTS_DIR']
        
        for filename in os.listdir(posts_dir):
            if filename.endswith('.md'):
                file_path = os.path.join(posts_dir, filename)
                try:
                    metadata, html_content = PostService.parse_markdown_file(file_path)
                    haystack = '\n'.join([
                        metadata.get('title', ''),
                        metadata.get('description', ''),
                        metadata.get('author', ''),
                        metadata.get('category', ''),
                        html_content
                    ]).lower()
                    
                    if query.lower() in haystack:
                        metadata['slug'] = filename.replace('.md', '')
                        results.append(metadata)
                except Exception as e:
                    current_app.logger.error(f"Error searching in {filename}: {e}")
                    continue
        
        return results

class CommentService:
    """评论服务类"""
    
    @staticmethod
    def get_comments_by_post(post_slug, approved_only=True):
        """获取文章的评论（多层嵌套结构）"""
        query = Comment.query.filter_by(post_slug=post_slug)
        if approved_only:
            query = query.filter_by(approved=True)
        
        comments = query.order_by(Comment.created_at.asc()).all()
        
        # 构建嵌套结构
        comment_dict = {comment.id: comment for comment in comments}
        top_level = []
        
        for comment in comments:
            if comment.parent_id is None:
                top_level.append(comment)
        
        return top_level
    
    @staticmethod
    def add_comment(post_slug, author, email, content, parent_id=None):
        """添加评论"""
        # 检查父评论是否存在
        level = 0
        if parent_id:
            parent_comment = Comment.query.get(parent_id)
            if not parent_comment:
                raise ValueError("父评论不存在")
            
            # 检查嵌套层级
            if parent_comment.level >= 2:
                raise ValueError("评论嵌套层级已达上限（最多2层）")
            
            level = parent_comment.level + 1
        
        comment = Comment(
            post_slug=post_slug,
            author=author,
            email=email,
            content=content,
            parent_id=parent_id,
            level=level
        )
        
        db.session.add(comment)
        db.session.commit()
        return comment
    
    @staticmethod
    def approve_comment(comment_id):
        """批准评论"""
        comment = Comment.query.get_or_404(comment_id)
        comment.approved = True
        db.session.commit()
        return comment
    
    @staticmethod
    def reject_comment(comment_id):
        """拒绝评论"""
        comment = Comment.query.get_or_404(comment_id)
        comment.approved = False
        db.session.commit()
        return comment
    
    @staticmethod
    def delete_comment(comment_id):
        """删除评论（同时删除所有子评论）"""
        comment = Comment.query.get_or_404(comment_id)
        
        # 递归删除所有子评论
        CommentService._delete_comment_tree(comment)
        
        db.session.commit()
        return comment
    
    @staticmethod
    def _delete_comment_tree(comment):
        """递归删除评论树"""
        # 先删除所有子评论
        replies = comment.get_all_child_comments()
        for reply in replies:
            db.session.delete(reply)
        
        # 删除当前评论
        db.session.delete(comment)
    


class UserService:
    """用户服务类"""
    
    @staticmethod
    def authenticate_user(username, password):
        """用户认证"""
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None
    
    @staticmethod
    def create_admin_user(username, password):
        """创建管理员用户"""
        user = User.query.filter_by(username=username).first()
        if user:
            return user
        
        user = User(username=username, is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user 