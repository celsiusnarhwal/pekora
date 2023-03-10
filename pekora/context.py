import typer
from decorator import decorator

_CONTEXT: typer.Context = None


@decorator
def set_context(func, *args, **kwargs):
    global _CONTEXT
    _CONTEXT = args[0]
    return func(*args, **kwargs)


def get_context():
    return _CONTEXT
