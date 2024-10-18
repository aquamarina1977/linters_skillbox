
from routes import app, api, BookResource, AuthorResource
from werkzeug.serving import WSGIRequestHandler

WSGIRequestHandler.protocol_version = "HTTP/1.1"

api.add_resource(BookResource, '/api/books/<int:book_id>')
api.add_resource(AuthorResource, '/api/authors/<int:author_id>')

if __name__ == '__main__':
    app.run(debug=True)