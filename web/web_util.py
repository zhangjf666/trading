"""
Date: 2021-01-14 22:00:56
Desc: web工具类
"""

from flask_sqlalchemy import Pagination


def page_to_dict(page: Pagination):
    return {'total': page.total, 'page': page.page, 'pages': page.pages, 'items': page.items, 'per_page': page.per_page}