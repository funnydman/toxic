from toxic.core.responses import HTMLResponse


def render_template(path_to_file: str, params):
    # todo: mock, add proper
    start_bracket = '{'
    end_bracket = '}'
    with open(path_to_file, 'r') as file:
        content = file.read()
    content = content.replace(f'{start_bracket}username{end_bracket}', params['name'])
    return HTMLResponse(content)
