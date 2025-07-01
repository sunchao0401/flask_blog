---
title: 代码高亮测试
date: 2024-01-20
author: 测试用户
category: 技术
description: 测试各种编程语言的代码高亮功能
tags: 测试, 代码高亮, 编程
top: true
---
# 代码高亮测试

这篇文章用于测试各种编程语言的代码高亮功能。

## Python 代码示例

```python
def fibonacci(n):
    """计算斐波那契数列"""
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# 使用示例
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")

# 列表推导式
squares = [x**2 for x in range(10)]
print(squares)
```

## JavaScript 代码示例

```javascript
// 箭头函数
const multiply = (a, b) => a * b;

// 异步函数
async function fetchData(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}

// 类定义
class Calculator {
    constructor() {
        this.result = 0;
    }
    
    add(value) {
        this.result += value;
        return this;
    }
    
    getResult() {
        return this.result;
    }
}
```

## HTML 代码示例

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>示例页面</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>欢迎访问</h1>
        <nav>
            <ul>
                <li><a href="#home">首页</a></li>
                <li><a href="#about">关于</a></li>
                <li><a href="#contact">联系</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <section id="content">
            <p>这是主要内容区域。</p>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2024 示例网站</p>
    </footer>
</body>
</html>
```

## CSS 代码示例

```css
/* 基础样式 */
body {
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
}

/* 导航栏样式 */
.navbar {
    background-color: #333;
    color: white;
    padding: 1rem;
}

.navbar ul {
    list-style: none;
    display: flex;
    gap: 2rem;
}

.navbar a {
    color: white;
    text-decoration: none;
    transition: color 0.3s ease;
}

.navbar a:hover {
    color: #ffd700;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .navbar ul {
        flex-direction: column;
        gap: 1rem;
    }
}
```

## SQL 代码示例

```sql
-- 创建用户表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 插入数据
INSERT INTO users (username, email, password_hash) 
VALUES ('john_doe', 'john@example.com', 'hashed_password_here');

-- 查询数据
SELECT 
    u.username,
    u.email,
    COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id
ORDER BY post_count DESC;
```

## Bash 脚本示例

```bash
#!/bin/bash

# 系统信息脚本
echo "=== 系统信息 ==="
echo "主机名: $(hostname)"
echo "操作系统: $(uname -s)"
echo "内核版本: $(uname -r)"
echo "CPU架构: $(uname -m)"

# 检查磁盘空间
echo -e "\n=== 磁盘空间 ==="
df -h | grep -E '^/dev/'

# 检查内存使用
echo -e "\n=== 内存使用 ==="
free -h

# 检查网络连接
echo -e "\n=== 网络连接 ==="
netstat -tuln | grep LISTEN
```

## JSON 数据示例

```json
{
    "name": "示例项目",
    "version": "1.0.0",
    "description": "这是一个示例项目",
    "author": {
        "name": "开发者",
        "email": "dev@example.com"
    },
    "dependencies": {
        "express": "^4.17.1",
        "mongoose": "^6.0.0",
        "bcryptjs": "^2.4.3"
    },
    "scripts": {
        "start": "node app.js",
        "dev": "nodemon app.js",
        "test": "jest"
    },
    "repository": {
        "type": "git",
        "url": "https://github.com/example/project.git"
    }
}
```

## Markdown 代码示例

```markdown
# 标题1
## 标题2
### 标题3

**粗体文本** 和 *斜体文本*

- 无序列表项1
- 无序列表项2
  - 嵌套列表项

1. 有序列表项1
2. 有序列表项2

[链接文本](https://example.com)

![图片描述](image.jpg)

`行内代码`

> 引用文本
```

## 总结

以上是各种编程语言的代码示例，用于测试代码高亮功能是否正常工作。每种语言都应该有不同的颜色主题来区分关键字、字符串、注释等不同元素。 