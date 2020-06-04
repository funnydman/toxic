import json


class Response:
    media_type = 'application/json'

    def __init__(self, content):
        self.content = content

    def render(self):
        return json.dumps(self.content)
