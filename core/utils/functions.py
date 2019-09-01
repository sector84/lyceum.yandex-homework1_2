from functools import wraps
from core.engine import Errors


def login_required(f):
    @wraps(f)
    def login_required_wrapper(*args, **kwargs):
        # todo: каким-то образом проверить что мы авторизовались
        # Errors.error('', code=CODE_UNAUTHORIZED)
        return f(*args, **kwargs)

    return login_required_wrapper

