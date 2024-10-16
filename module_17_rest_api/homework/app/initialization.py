from models import init_db

initial_authors = [
    {'first_name': 'Swaroop', 'last_name': 'C. H.', 'middle_name': None},
    {'first_name': 'Herman', 'last_name': 'Melville', 'middle_name': None},
    {'first_name': 'Leo', 'last_name': 'Tolstoy', 'middle_name': None},
]

initial_books = [
    {'title': 'A Byte of Python', 'author_id': 1},
    {'title': 'Moby-Dick; or, The Whale', 'author_id': 2},
    {'title': 'War and Peace', 'author_id': 3},
]

init_db(initial_books=initial_books, initial_authors=initial_authors)
