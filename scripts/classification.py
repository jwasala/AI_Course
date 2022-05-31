import logging
from collections import Counter
from dataclasses import fields
from itertools import chain, islice
from pathlib import Path
from pprint import pprint

from si_project.classification import load_books, transform_books, BookRaw

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s]\t[%(asctime)s]\t(in %(funcName)s) %(message)s'
)

if __name__ == '__main__':

    books_file_path = Path(__file__).parent.parent.resolve() / 'assets' / 'booksummaries' / 'booksummaries.txt'

    with open(books_file_path, 'r', encoding='utf-8') as file:
        books_raw = load_books(file)

    missing_fields = {
        field: sum(not getattr(book, field) for book in books_raw)
        for field in (field.name for field in fields(BookRaw))
    }

    print('Missing field values:')
    pprint(missing_fields)

    books_transformed = list(transform_books(books_raw, 10))

    print('Genre counts before final transformations:')
    genre_counts = Counter(book.genre for book in books_transformed)
    pprint(genre_counts)

    # Transform genres to final format by grouping in following order:
    # - Children's literature
    # - Mystery
    # - Science Fiction
    # - Fantasy

    for genre_part in ("Children's literature", 'Mystery', 'Science Fiction', 'Fantasy'):
        books_transformed = [
            (book.replace('genre', genre_part) if genre_part in book.genre else book) for book in books_transformed
        ]

    genre_counts = Counter(book.genre for book in books_transformed)
    print('Genre counts after final transformations:')
    pprint(genre_counts)

    # Keep only top nine genres.
    top_genres = list(dict(genre_counts.most_common(9)).keys())
    books_transformed = [book for book in books_transformed if book.genre in top_genres]

    genre_counts = Counter(book.genre for book in books_transformed)
    print('Genre counts after removing less popular genres:')
    pprint(genre_counts)
    print(f'Books in total: {sum(genre_counts.values())}')

    # Count top 100-500 words in the books left out.
    words_flattened = chain(*[book.plot_summary.split(' ') for book in books_transformed])
    plot_words = list(dict(Counter(words_flattened).most_common(500)).keys())[150:]
    print(plot_words)

    # Calculate max number of occurences of each word per plot summary.
    words_max_occurences = {word: max(book.plot_summary.count(word) for book in books_transformed) for word in
                            plot_words}
    pprint(words_max_occurences)

    # Calculate feature matrix. Each row is a vector of values between 0-1, which is normalized number of occurences
    # of a given word in plot summary.
    feature_matrix = [
        [book.plot_summary.count(word) / words_max_occurences[word] for word in plot_words]
        for book in books_transformed
    ]

    print('A fragment of the feature matrix:')
    print(' '.join([' ' * 27] + [word.ljust(7)[:7] for word in plot_words[:25]]))
    for book, feature_vect in islice(zip(books_transformed, feature_matrix), 50):
        print('\t'.join([book.genre.ljust(25)] + [f'{val:.2f}' for val in feature_vect[:25]]))
