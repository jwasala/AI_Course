import json
import logging

from .model import BookRaw

logger = logging.getLogger(__name__)


def load_books(stream) -> list[BookRaw]:
    books: list[BookRaw] = []
    exception_count = 0

    for line_i, line in enumerate(stream):
        # Split line into columns
        try:
            article_id_raw, freebase_id, title, author, pub_date_raw, genres, plot = line.split('\t')
        except ValueError as ve:
            logger.warning(f'Couldn\'t unpack line {line_i}, values "{line}": {ve}')
            exception_count += 1
            continue
        # Parse integers
        try:
            article_id = int(article_id_raw) if article_id_raw else None
        except ValueError as ve:
            logger.warning(f'Couldn\'t parse integer value in line {line_i}, values "{line}": {ve}')
            exception_count += 1
            continue
        # Parse date
        try:
            pub_year = int(pub_date_raw.split('-')[0]) if pub_date_raw else None
        except ValueError as ve:
            logger.warning(f'Couldn\'t parse year of publication in line {line_i}, values "{line}": {ve}')
            exception_count += 1
            continue
        # Parse genres
        try:
            if genres:
                genres = list(json.loads(genres).values())
            else:
                genres = []
        except Exception as e:
            logger.warning(f'Couldn\'t parse genres in line {line_i}, values "{line}": {e}')
            exception_count += 1
            continue
        books.append(BookRaw(article_id, freebase_id, title, author, pub_year, genres, plot))

    logger.info(f'Parsed {len(books)} books, {exception_count} were ignored due to parsing errors.')
    return books
