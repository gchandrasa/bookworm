from django.conf import settings
from django.db import models
from django.db.models import Avg


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True,
                                 null=True)
    created = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(blank=True, null=True, editable=False)

    def __unicode__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    rating = models.IntegerField(choices=[(i, i) for i in xrange(1, 6)])
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('book', 'user'),)

    def __unicode__(self):
        return unicode(self.rating)

    def calculate_book_rating(self):
        # calculate average rating for book
        rating = Review.objects.filter(book=self.book).aggregate(avg=Avg('rating'))
        if rating and 'avg' in rating:
            self.book.rating = rating['avg']
            self.book.save()
            return rating['avg']
        return None

    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)
        self.calculate_book_rating()

    def delete(self, *args, **kwargs):
        super(Review, self).delete(*args, **kwargs)
        self.calculate_book_rating()
