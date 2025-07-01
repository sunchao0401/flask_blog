---
title: 欢迎来到我的博客
date: 2024-01-15
author: 博主
category: 介绍
description: 这是我的第一篇博客文章，介绍这个用 Flask 构建的 Markdown 博客系统
tags: Flask, Markdown, Python, 博客
top: true
---
# 欢迎来到我的博客！

这是一个使用 **Flask** 和 **Markdown** 构建的博客系统。让我来介绍一下这个系统的特点：

## 主要功能

### 1. Markdown 支持
- 完整的 Markdown 语法支持
- 代码高亮显示
- 表格渲染
- 目录生成

### 2. 文章管理
- 自动解析文章元数据
- 支持分类和标签
- 按日期排序
- 文章预览

### 3. 现代化界面
- 响应式设计
- Bootstrap 5 框架
- Font Awesome 图标
- 优雅的动画效果

## 如何使用

### 创建新文章
1. 在 `posts` 目录下创建 `.md` 文件
2. 在文件开头添加元数据（可选）
3. 使用 Markdown 语法编写内容
4. 保存文件即可自动显示在博客中

### 元数据格式
```yaml
---
title: 文章标题
date: 2024-01-15
author: 作者名
category: 分类名
description: 文章描述
tags: 标签1, 标签2, 标签3
---
```

## 代码示例

这是一个 Python 代码示例：

```python
from flask import Flask, render_template
import markdown

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```

## 表格示例

| 功能 | 状态 | 说明 |
|------|------|------|
| Markdown 渲染 | ✅ | 完整支持 |
| 代码高亮 | ✅ | 支持多种语言 |
| 响应式设计 | ✅ | 移动端友好 |
| 分类管理 | ✅ | 自动分类 |

## 下一步计划

- [ ] 添加搜索功能
- [ ] 支持评论系统
- [ ] 添加 RSS 订阅
- [ ] 支持图片上传
- [ ] 添加访问统计

---

*感谢您阅读我的第一篇博客文章！如果您有任何建议或问题，欢迎在评论区留言。* 