from toxic.core.responses import HTMLResponse


def render_template(path_to_file: str, params=None):
    # todo: mock, add proper
    start_bracket = '{'
    end_bracket = '}'
    with open(path_to_file, 'r') as file:
        content = file.read()
    return HTMLResponse(content)


class HTTPRedirect:
    pass
