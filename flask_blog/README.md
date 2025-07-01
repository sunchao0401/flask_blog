# Flask Markdown 博客系统

一个基于 Flask 的现代化 Markdown 博客系统，支持文章管理、评论系统、用户认证等功能。

---

## 主要特性
- 📝 **Markdown 文章支持**，代码高亮
- 💬 **嵌套评论系统**（2层）
- 👤 **用户认证与后台管理**
- 🔍 **全文搜索与分类**
- 📱 **响应式设计**
- 📊 **分页与标签系统**

---

## 技术栈与依赖

- **后端**: Flask 3.1.1, Flask-SQLAlchemy, Flask-Login, Flask-WTF, Flask-Migrate
- **数据库**: SQLite（默认），支持 PostgreSQL/MySQL
- **Markdown**: markdown, Pygments
- **前端**: Bootstrap 5, Prism.js

**依赖已极致精简，无冗余包，详见 requirements.txt。**

---

## 快速开始

1. **环境准备**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **配置环境**
   ```bash
   cp env.example .env
   # 编辑 .env 文件，设置密钥/数据库等
   ```
3. **初始化数据库**
   ```bash
   flask init-db
   flask create-admin --username admin --password your-password
   ```
4. **运行项目**
   ```bash
   python run.py
   # 或
   flask run
   ```
5. **访问**
   - 博客首页：http://localhost:5000
   - 管理后台：http://localhost:5000/admin/login

---

## 项目结构
```
flask_blog/
├── __init__.py           # 应用工厂
├── config.py             # 配置
├── models.py             # 数据模型
├── services.py           # 业务逻辑
├── forms.py              # 表单
├── commands.py           # CLI命令
├── extensions.py         # 扩展初始化
├── decorators.py         # 权限装饰器
├── utils.py              # 工具函数
├── blog_blueprint.py     # 博客蓝图
├── admin_blueprint.py    # 管理后台蓝图
├── run.py                # 启动脚本
├── requirements.txt      # 依赖列表
├── static/               # 静态资源
├── templates/            # Jinja2模板
├── posts/                # Markdown文章
└── blog.db               # SQLite数据库（可选）
```

---

## 管理命令

```bash
flask manage-user --action list|create|update|delete --username ...
flask reset-password --username ...
flask list-posts
flask init-db
```

---

## 代码与依赖清理说明
- **2024-06-XX：已彻底清理无效/冗余代码，移除所有测试文件和临时文件，run.py 启动脚本已优化。**
- **无未使用的依赖项**，requirements.txt 仅保留实际用到的包
- **无临时/测试/自动生成文件**，如有请及时删除
- **所有核心功能均有对应实现，结构清晰**
- **推荐定期用 black/flake8 检查代码风格**

---

## 开发与扩展
- 新文章：在 `posts/` 下添加 `.md` 文件，带YAML头
- 新功能：在 `services.py`/`models.py`/`blueprint` 中扩展
- 样式/主题：编辑 `static/css/main.css`、`templates/base.html`

---

## 生产部署建议
- 设置 `FLASK_ENV=production`，配置 SECRET_KEY、DATABASE_URL
- 推荐使用 Gunicorn/uwsgi + Nginx 部署
- 启用 Gzip 压缩和静态资源缓存

---

## 许可证
MIT License

---

## 更新日志
- 2024-01-01 v1.0.0 首发，功能完整，代码无冗余，依赖极简
- 2024-06-XX 代码全面清理，移除测试/临时文件，run.py 优化

---

如有问题请提交 Issue 或 PR，欢迎交流与贡献！ 