from django.db import models
from django.utils.translation  import ugettext_lazy as _
from django.contrib.auth.models import User
import re
from django.core.exceptions import ValidationError
from catalog.isbn import isValid as isbn_validator
from django.template.defaultfilters import slugify

def validate_isbn(isbn):
    if not isbn_validator(isbn):
        raise ValidationError(u'%s is not a valid isbn number' % isbn)

class Book(models.Model):
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(unique=True)
    isbn = models.CharField(_('isbn'), max_length=13,
            unique=True, validators=[validate_isbn],
            help_text='Enter the unique 10 or 13 digit ISBN',
            blank=True, null=True)
    description = models.TextField(_('description'), blank=True)
    url = models.URLField(_('url'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    owners = models.ManyToManyField(User, through='BookOwner')

    @models.permalink
    def get_absolute_url(self):
        if self.isbn:
            return ('catalog:book_details', (self.isbn, ))
        else:
            return ('catalog:book_details', (self.slug, ))

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)

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

