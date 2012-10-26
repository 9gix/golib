from django.contrib import admin
from catalog.models import Book, BookOwner
from catalog.forms import BookModelForm

class BookAdmin(admin.ModelAdmin):
    form = BookModelForm
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Book, BookAdmin)
admin.site.register(BookOwner)
