import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHORS_TABLE_NAME = 'authors'

@dataclass
class Author:
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    id: Optional[int] = None

@dataclass
class Book:
    title: str
    author_id: int
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


def init_db(initial_books: List[Dict], initial_authors: List[Dict]) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {BOOKS_TABLE_NAME};")
        cursor.execute(f"DROP TABLE IF EXISTS {AUTHORS_TABLE_NAME};")

        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {AUTHORS_TABLE_NAME}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                middle_name TEXT
            );
            """
        )

        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {BOOKS_TABLE_NAME}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author_id INTEGER,
                FOREIGN KEY (author_id) REFERENCES {AUTHORS_TABLE_NAME}(id) ON DELETE CASCADE
            );
            """
        )

        cursor.executemany(
            f"""
            INSERT INTO {AUTHORS_TABLE_NAME}(first_name, last_name, middle_name) 
            VALUES (?, ?, ?)
            """,
            [(author['first_name'], author['last_name'], author.get('middle_name')) for author in initial_authors]
        )

        cursor.executemany(
            f"""
            INSERT INTO {BOOKS_TABLE_NAME}(title, author_id) 
            VALUES (?, ?)
            """,
            [(book['title'], book['author_id']) for book in initial_books]
        )


def _get_book_obj_from_row(row: tuple) -> Book:
    return Book(id=row[0], title=row[1], author_id=row[2])

def get_all_books() -> List[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{BOOKS_TABLE_NAME}`')
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]

def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO `{BOOKS_TABLE_NAME}` 
            (title, author_id) VALUES (?, ?)
            """,
            (book.title, book.author_id)
        )
        book.id = cursor.lastrowid
        return book

def _get_author_obj_from_row(row: tuple) -> Author:
    return Author(id=row[0], first_name=row[1], last_name=row[2], middle_name=row[3])

def get_author_by_id(author_id: int) -> Optional[Author]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM `{AUTHORS_TABLE_NAME}` WHERE id = ?', (author_id,))
        author = cursor.fetchone()
        if author:
            return _get_author_obj_from_row(author)

def get_book_by_title(book_title: str) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM {BOOKS_TABLE_NAME} WHERE title = ?
            """,
            (book_title,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)

def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {BOOKS_TABLE_NAME} WHERE id = ?", (book_id,))
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)
    return None

def update_book(book_id: int, updated_data: dict) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE {BOOKS_TABLE_NAME}
            SET title = ?, author_id = ?
            WHERE id = ?
            """,
            (updated_data['title'], updated_data['author_id'], book_id)
        )
        if cursor.rowcount > 0:
            return get_book_by_id(book_id)
    return None

def delete_book(book_id: int) -> bool:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {BOOKS_TABLE_NAME} WHERE id = ?", (book_id,))
        return cursor.rowcount > 0

def add_author(author_data: dict) -> Author:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO {AUTHORS_TABLE_NAME}(first_name, last_name, middle_name) VALUES (?, ?, ?)",
            (author_data['first_name'], author_data['last_name'], author_data.get('middle_name'))
        )
        author_id = cursor.lastrowid
        return get_author_by_id(author_id)

def get_books_by_author_id(author_id: int) -> List[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {BOOKS_TABLE_NAME} WHERE author_id = ?", (author_id,))
        books = cursor.fetchall()
        return [_get_book_obj_from_row(book) for book in books]

def delete_author_and_books(author_id: int) -> bool:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {AUTHORS_TABLE_NAME} WHERE id = ?", (author_id,))
        cursor.execute(f"DELETE FROM {BOOKS_TABLE_NAME} WHERE author_id = ?", (author_id,))
        return cursor.rowcount > 0
