
from contextvars import ContextVar
from typing import Optional

__all__ = ['x_request_content']

x_request_content: ContextVar[Optional[str]] = ContextVar('_x_request_id', default="-")
x_request_content.set("-")
