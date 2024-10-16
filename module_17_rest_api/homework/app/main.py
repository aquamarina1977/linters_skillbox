from routes import app, api, BookResource, AuthorResource

api.add_resource(BookResource, '/api/books/<int:book_id>')
api.add_resource(AuthorResource, '/api/authors/<int:author_id>')

if __name__ == '__main__':
    app.run(debug=True)