from collections import Counter
from dataclasses import fields
from itertools import chain
import logging
from typing import Iterator

from .model import Book, BookRaw


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def _ignore_incomplete_records(books_raw: Iterator[BookRaw]) -> Iterator[BookRaw]:
    ignore_fields = []
    ignore_count, parse_count = 0, 0

    for book in books_raw:
        is_complete = True
        for field_name in (field.name for field in fields(BookRaw) if field.name not in Book.ignored_fields):
            if not getattr(book, field_name) or getattr(book, field_name) == ['']:
                is_complete = False
                ignore_fields.append(field_name)
                ignore_count += 1
                break
        if is_complete:
            parse_count += 1
            yield book

    logger.info(f'{ignore_count} books were ignored and {parse_count} books were parsed.')
    for field_name, field_count in Counter(ignore_fields).items():
        logger.info(f'Incompleteness of {field_name} field caused {field_count} books to be ignored.')
    logger.info(f'End of {_ignore_incomplete_records.__name__} statistics.')


def _skip_genres(books_raw, genres_to_skip: list[str]) -> Iterator[BookRaw]:
    count = 0
    skip_count = 0
    for book in books_raw:
        count += 1
        genres_with_skip = [genre for genre in book.genres if genre not in genres_to_skip]
        if book.genres != genres_with_skip:
            skip_count += 1
        yield BookRaw(
            book.article_id, book.freebase_id, book.title, book.author, book.publication_year,
            [genre for genre in book.genres if genre not in genres_to_skip], book.plot_summary
        )
    logger.info(f'There were {count} books, and some genres were skipped in {skip_count} of them.')


def _get_top_n_genres(books_raw: Iterator[BookRaw], n: int) -> list[str]:
    categories = chain(*(book_r.genres for book_r in books_raw))
    counter = Counter(categories)
    top_genres = list(dict(counter.most_common(n)).keys())
    logger.info(f'Calculated top genres: {top_genres}.')
    return top_genres


def _keep_n_top_genres(books_raw: Iterator[BookRaw],
                       n: int,
                       top_genres: list[str] | None = None) -> Iterator[BookRaw]:
    count = 0
    if not top_genres:
        top_genres = _get_top_n_genres(books_raw, n)
    for book in books_raw:
        count += 1
        yield BookRaw(
            book.article_id, book.freebase_id, book.title, book.author, book.publication_year,
            [genre for genre in book.genres if genre in top_genres], book.plot_summary
        )
    logger.info(f'There were {count} books yielded.')


def _sort_and_join_genres(books_raw: Iterator[BookRaw]) -> Iterator[BookRaw]:
    for book in books_raw:
        yield BookRaw(
            book.article_id, book.freebase_id, book.title, book.author, book.publication_year,
            ['-'.join(sorted(book.genres))], book.plot_summary
        )


def transform_books(books_raw: Iterator[BookRaw], output_genres_count: int) -> Iterator[Book]:
    books_with_skipped_genres = list(_skip_genres(books_raw, ['Fiction']))
    top_genres = _get_top_n_genres(books_with_skipped_genres, output_genres_count)
    count = 0

    books_after_transform: Iterator[BookRaw] = _ignore_incomplete_records(
        _sort_and_join_genres(
            _keep_n_top_genres(
                books_with_skipped_genres,
                output_genres_count,
                top_genres
            )
        )
    )

    for book_r in books_after_transform:
        count += 1
        yield Book(
            book_r.article_id, book_r.freebase_id, book_r.title, book_r.author,
            book_r.genres[0], book_r.plot_summary
        )
    logger.info(f'{count} books were transformed to final format.')
