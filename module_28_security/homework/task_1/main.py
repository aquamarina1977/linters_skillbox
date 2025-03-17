from flask import Flask, jsonify, request, Response

app = Flask(__name__)

ALLOWED_ORIGIN = "https://www.google.com"


@app.route('/', methods=['GET'])
def get_handler():
    print(request.headers)
    return jsonify({"message": "Hello, User"})


@app.route('/', methods=['POST'])
def post_handler():
    data = request.json
    return jsonify({"received": data})


@app.after_request
def add_cors(response: Response):
    response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGIN
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'X-My-Fancy-Header, Content-Type, Authorization'
    response.headers['Access-Control-Max-Age'] = '3600'
    return response


if __name__ == '__main__':
    app.run(port=8080, debug=True)

