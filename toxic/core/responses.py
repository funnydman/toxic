import abc
import json
from typing import Any

from toxic.core import status


class BaseResponse(abc.ABC):
    def __init__(
            self,
            content: Any,
            status_code: int = status.HTTP_OK
    ) -> None:
        self.status_code = status_code
        self.content = content

    @property
    def content_length(self):
        return len(str(self.content))

    @abc.abstractmethod
    def render(self):
        ...


class Response(BaseResponse):
    content_type = 'application/json'
    charset = 'utf-8'

    def render(self) -> json:
        return json.dumps(self.content)


class HTMLResponse(BaseResponse):
    content_type = 'text/html'
    charset = 'utf-8'

    def render(self) -> str:
        return str(self.content)
