from django.contrib.auth import get_user_model
from django.db import transaction
from django.db import IntegrityError
from django.test import TestCase

from .models import Book


User = get_user_model()


class BookTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(title='Book #1')

    def test_add_remove_review(self):
        """Add review or remove should automatically update book rating"""

        user1 = User.objects.create_user('John')
        self.book.reviews.create(
            user=user1,
            rating=5,
            notes="It's so awesome"
        )

        user2 = User.objects.create_user('Jane')
        review = self.book.reviews.create(
            user=user2,
            rating=4,
            notes="Love it"
        )

        # need to reload from database for updated rating value in book
        book = Book.objects.get(id=self.book.id)
        self.assertAlmostEqual(book.rating, 4.5)

        review.delete()

        book = Book.objects.get(id=self.book.id)
        self.assertAlmostEqual(book.rating, 5)

    def test_update_review(self):
        """Add review or remove should automatically update book rating"""

        user1 = User.objects.create_user('John')
        self.book.reviews.create(
            user=user1,
            rating=5,
            notes="It's so awesome"
        )

        user2 = User.objects.create_user('Jane')
        review = self.book.reviews.create(
            user=user2,
            rating=4,
            notes="Love it"
        )

        # update rating
        review.rating = 3
        review.save()

        # need to reload from database for updated rating value in book
        book = Book.objects.get(id=self.book.id)
        self.assertAlmostEqual(book.rating, 4)

    def test_single_review_per_user(self):
        """One user only allow to review a book once"""

        user1 = User.objects.create_user('John')
        self.book.reviews.create(
            user=user1,
            rating=5,
            notes="It's so awesome"
        )

        with transaction.atomic():
            self.assertRaises(
                IntegrityError,
                lambda: self.book.reviews.create(
                    user=user1,
                    rating=3,
                    notes="Super!"
                )
            )
