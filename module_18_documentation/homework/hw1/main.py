from routes import app, api, BookResource, BookList, AuthorResource

api.add_resource(AuthorResource, '/api/authors/<int:author_id>')
api.add_resource(BookList, '/books')
api.add_resource(BookResource, '/books/<int:book_id>')

if __name__ == '__main__':
    app.run(debug=True)