from flask import Flask, request, Response

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    {user_input}
</body>
</html>
"""


@app.route('/')
def index():
    user_input = request.args.get('input', 'Hello, User!')
    response = Response(HTML_TEMPLATE.format(user_input=user_input))
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self';"
    return response


if __name__ == '__main__':
    app.run(port=8080, debug=True)

