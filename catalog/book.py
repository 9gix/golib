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

        book = Book.objects.create(
                isbn=isbn,
                title=title,
                description=description)
        return book
    else:
        return None
