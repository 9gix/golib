from gdata.books.service import BookService
from catalog.models import Book

def fetch_book_detail_from_google(isbn):
    """Fetch book from Google Book Service and Return dict of book info"""
    service = BookService()
    result = service.search(isbn)
    book_dict = {}
    matched_book = None
    for book in result.entry:
        for identifier in book.identifier:
            if isbn in identifier.text:
                matched_book = book
                break


    book_dict = matched_book.to_dict()

    if matched_book:
        for identifier in matched_book.identifier:
            """
            Book Identifiers:
                [('google_id', 'dwSfGQAACAAJ'),
                ('ISBN', '0132350882'),
                ('ISBN', '9780132350884')]
            """
            if 'ISBN' in identifier.text:
                isbn = identifier.text.split(':',1)[1]
                if len(isbn) == 10:
                    book_dict['isbn10'] = isbn
                elif len(isbn) == 13:
                    book_dict['isbn13'] = isbn
    return book_dict

def search_and_save_to_db(isbn):
    """Search and save Book details into database and return the book object"""
    book_data = fetch_book_detail_from_google(isbn)

    if book_data:
        title = book_data.get('title')
        description = book_data.get('description','')
        identifier_list = book_data.get('identifiers', [])
        isbn10, isbn13 = book_data.get('isbn10', None), book_data.get('isbn13',None)
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
