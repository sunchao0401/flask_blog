"""
工具函数模块
"""

def paginate_items(items, page, per_page):
    """通用分页函数"""
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_items = items[start:end]
    total_pages = (total + per_page - 1) // per_page
    return paginated_items, total_pages 