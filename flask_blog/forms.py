from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional

class CommentForm(FlaskForm):
    """评论表单"""
    author = StringField('作者', validators=[
        DataRequired(message='请输入作者名称'),
        Length(max=50, message='作者名称不能超过50个字符')
    ])
    email = StringField('邮箱', validators=[
        DataRequired(message='请输入邮箱地址'),
        Email(message='请输入有效的邮箱地址')
    ])
    content = TextAreaField('评论内容', validators=[
        DataRequired(message='请输入评论内容'),
        Length(max=1000, message='评论内容不能超过1000个字符')
    ])
    parent_id = StringField('父评论ID', validators=[Optional()])
    submit = SubmitField('提交评论')

class LoginForm(FlaskForm):
    """登录表单"""
    username = StringField('用户名', validators=[
        DataRequired(message='请输入用户名')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='请输入密码')
    ])
    submit = SubmitField('登录')

class PostEditForm(FlaskForm):
    """文章编辑表单"""
    title = StringField('标题', validators=[
        DataRequired(message='请输入文章标题'),
        Length(max=200, message='标题不能超过200个字符')
    ])
    date = StringField('日期', validators=[
        DataRequired(message='请输入发布日期')
    ])
    author = StringField('作者', validators=[
        DataRequired(message='请输入作者名称'),
        Length(max=100, message='作者名称不能超过100个字符')
    ])
    category = StringField('分类', validators=[
        Optional(),
        Length(max=50, message='分类名称不能超过50个字符')
    ])
    description = TextAreaField('描述', validators=[
        Optional(),
        Length(max=500, message='描述不能超过500个字符')
    ])
    tags = StringField('标签', validators=[
        Optional(),
        Length(max=200, message='标签不能超过200个字符')
    ])
    top = BooleanField('置顶')
    submit = SubmitField('保存') 