"""
Заменим сообщение "The requested URL was not found on the server" на что-то более информативное.
Например, выведем список всех доступных страниц с возможностью перехода по ним.

Создайте Flask Error Handler, который при отсутствии запрашиваемой страницы будет выводить
список всех доступных страниц на сайте с возможностью перехода на них.
"""

from flask import Flask

app = Flask(__name__)

def get_available_pages():
    return [endpoint for endpoint in app.url_map.iter_rules() if endpoint.endpoint != 'Static']

def generate_links(pages):
    links = ''
    for page in pages:
        links += f'<a href="{page.rule}">{page.rule}</a><br>'
    return links

@app.errorhandler(404)
def page_not_found(e):
    pages = get_available_pages()
    links = generate_links(pages)
    return f'Страница не найдена. Доступные страницы:<br>{links}', 404

@app.route('/dogs')
def dogs():
    return 'Страница с пёсиками'


@app.route('/cats')
def cats():
    return 'Страница с котиками'


@app.route('/cats/<int:cat_id>')
def cat_page(cat_id: int):
    return f'Страница с котиком {cat_id}'


@app.route('/index')
def index():
    return 'Главная страница'


if __name__ == '__main__':
    app.run(debug=True)
