import json
from typing import Any

from toxic.core import status


class Response:
    content_type = 'application/json'
    charset = 'utf-8'

    def __init__(
            self,
            content: Any,
            status_code: str = status.HTTP_OK
    ) -> None:
        self.status_code = status_code
        self.content = content

    def render(self) -> json:
        return json.dumps(self.content)

    @property
    def content_length(self):
        return len(str(self.content))
