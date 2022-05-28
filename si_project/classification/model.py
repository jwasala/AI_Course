from dataclasses import dataclass
from datetime import date


@dataclass
class BookRaw:
    """
    Represents book data as in source file with very basic transformations:
    - article_id, freebase_id to int
    - book genres to list of strings (dict values)
    - publication_date to datetime
    """
    article_id: int | None
    freebase_id: int | None
    book_title: str | None
    author: str | None
    publication_date: date | None
    book_genres: list[str]
    plot_summary: str | None


@dataclass
class Book:
    """
    Represents transformed book data:
    - book_genres replaced with arbitrary label book_genre
    - values of other fields are non nullable
    """
    article_id: int
    freebase_id: int
    book_title: str
    author: str
    book_genre: str
    plot_summary: str
