from django.db import models
from django.utils.translation  import ugettext_lazy as _
from django.contrib.auth.models import User
import re
from django.core.exceptions import ValidationError
from catalog.isbn import isValid as isbn_validator
from catalog.isbn import checkI10, checkI13
from django.template.defaultfilters import slugify
from django.db.models.query import QuerySet


def isbn10_validator(isbn):
    if not checkI10(isbn):
        raise ValidationError(u'%s is not a valid ISBN-10' % isbn)

def isbn13_validator(isbn):
    if not checkI13(isbn):
        raise ValidationError(u'%s is not a valid ISBN-13' % isbn)

def validate_isbn(isbn):
    if len(isbn) == 10:
        isbn10_validator(isbn)
    elif len(isbn) == 13:
        isbn13_validator(isbn)
    else:
        raise ValidationError("Invalid ISBN")

def switch_isbn(**kwargs):
    isbn = kwargs.pop('isbn', '')
    if len(isbn) == 10:
        kwargs['isbn10'] = isbn
    elif len(isbn) == 13:
        kwargs['isbn13'] = isbn
    return kwargs

class BookQuerySet(QuerySet):
    def get(self, *args, **kwargs):
        kwargs = switch_isbn(**kwargs)
        return super(BookQuerySet, self).get(*args, **kwargs)

class BookManager(models.Manager):
    def get_query_set(self):
        return BookQuerySet(self.model, using=self._db)

    def get(self, *args, **kwargs):
        kwargs = switch_isbn(**kwargs)
        return super(BookManager, self).get(*args, **kwargs)

class Book(models.Model):
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(unique=True)
    isbn10 = models.CharField(_('isbn10'), max_length=10,
            unique=True, validators=[isbn10_validator],
            help_text='Enter the unique ISBN-10',
            blank=True, null=True)
    isbn13 = models.CharField(_('isbn13'), max_length=13,
            unique=True, validators=[isbn13_validator],
            help_text='Enter the unique ISBN-13',
            blank=True, null=True)
    description = models.TextField(_('description'), blank=True)
    url = models.URLField(_('url'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    owners = models.ManyToManyField(User, through='BookOwner')

    objects = BookManager()

    class Meta:
        unique_together = ('isbn10', 'isbn13')

    @models.permalink
    def get_absolute_url(self):
        if self.isbn13:
            return ('catalog:book_details', (self.isbn13, ))
        elif self.isbn10:
            return ('catalog:book_details', (self.isbn10, ))
        else:
            return ('catalog:book_details', (self.slug, ))

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            if self.isbn10:
                self.slug = slugify(self.isbn10)
            elif self.isbn13:
                self.slug = slugify(self.isbn13)
            else:
                self.slug = ''
            self.slug = "%s-%s" % (self.slug, slugify(self.title))
        super(Book, self).save(*args, **kwargs)

    @property
    def isbn(self):
        return self.isbn13 or self.isbn10

class BookOwner(models.Model):
    CONDITION_CHOICES = (
            ('good','Good'),
            ('ok','Ok'),
            ('bad','Bad'),
        )

    owner = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    availability = models.BooleanField(default=True)
    condition = models.CharField(max_length=5, choices=CONDITION_CHOICES)

    def __unicode__(self):
        return "%s" % self.book

