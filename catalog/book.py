from gdata.books.service import BookService
from catalog.models import Book

def fetch_book_detail(isbn):
    """Fetch book from Google Book Service and Return dict of book info"""
    service = BookService()
    result = service.search_by_keyword(isbn=isbn)
    try:
        book = result.entry[0]
    except IndexError:
        return {}
    book_dict = book.to_dict()
    return book_dict

def search_and_save_to_db(isbn):
    """Search and save Book details into database and return the book object"""
    book_data = fetch_book_detail(isbn)

    if book_data:
        title = book_data.get('title')
        description = book_data.get('description')
        identifier_list = book_data.get('identifiers', [])
        isbn10, isbn13 = None, None
        for identifier in identifier_list:
            """Sample Identifiers:
                [('google_id', 'dwSfGQAACAAJ'),
                ('ISBN', '0132350882'),
                ('ISBN', '9780132350884')]"""
            try:
                if identifier[0] == 'ISBN':
                    if len(identifier[1]) == 10:
                        isbn10 = identifier[1]
                    elif len(identifier[1]) == 13:
                        isbn13 = identifier[1]
            except IndexError:
                # TODO: log this error, perhaps google change its structure
                pass

        try:
            # ISBN that we sent should matched with the result from Google
            if len(isbn) == 10:
                assert isbn10 == isbn
            elif len(isbn) == 13:
                assert isbn13 == isbn
        except AssertionError:
            # TODO: log this error, investigate if this error happened
            pass

        book = Book.objects.create(
                isbn10=isbn10,
                isbn13=isbn13,
                title=title,
                description=description)
        return book
    else:
        return None
