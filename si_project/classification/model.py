from dataclasses import dataclass


@dataclass
class BookRaw:
    """
    Represents book data as in source file with very basic transformations:
    - article_id, freebase_id to int
    - book genres to list of strings (dict values)
    - publication_date to publication_year (trunkate and parse int)
    """
    article_id: int | None
    freebase_id: int | None
    title: str | None
    author: str | None
    publication_year: int | None
    genres: list[str]
    plot_summary: str | None


@dataclass
class Book:
    """
    Represents transformed book data:
    - genres replaced with arbitrary label genre
    - values of other fields are non nullable
    """
    article_id: int
    freebase_id: int
    title: str
    author: str
    publication_year: int
    genre: str
    plot_summary: str
