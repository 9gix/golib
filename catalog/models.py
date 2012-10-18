from django.db import models
from django.utils.translation  import ugettext_lazy as _
from django.contrib.auth.models import User

class Book(models.Model):
    name = models.CharField(_('name'), max_length=48)
    isbn = models.CharField(_('isbn'), max_length=16)
    description = models.TextField(_('description'))
    url = models.URLField(_('url'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ManyToManyField(User, through='BookOwner')

    @models.permalink
    def get_absolute_url(self):
        return ('book_detail', (self.pk))

    def __unicode__(self):
        return self.name

class BookOwner(models.Model):
    CONDITION_CHOICES = (
            ('new','New'),
            ('good','Good'),
            ('ok','Ok'),
            ('bad','Bad'),
        )

    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    availability = models.BooleanField(default=True)
    condition = models.CharField(max_length=5, choices=CONDITION_CHOICES)

    def __unicode__(self):
        return "%s (owner: %s)" %(self.book, self.user)

