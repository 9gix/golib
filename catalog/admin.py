from django.contrib import admin
from catalog.models import Book, BookOwner
from catalog.forms import BookModelForm

class BookAdmin(admin.ModelAdmin):
    form = BookModelForm
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('isbn','title',)
    list_display_links = ('isbn','title',)

admin.site.register(Book, BookAdmin)
admin.site.register(BookOwner)
