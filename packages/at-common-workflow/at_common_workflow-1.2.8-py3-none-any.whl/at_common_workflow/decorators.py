from typing import Callable, Any

def requires_context(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to mark functions that require the full context object."""
    func.__requires_context__ = True
    return func 