from flask import session, redirect, url_for
from functools import wraps

# 登录限制的装饰器


def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("user_name"):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper
