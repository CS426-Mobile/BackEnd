from django.db import models
from User.models import CustomUser
from Book.models import Book

class CustomerCartBook(models.Model):
    user_email = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book_name = models.ForeignKey(Book, on_delete=models.CASCADE)
    num_books = models.IntegerField(default=1)

    class Meta:
        unique_together = ('user_email', 'book_name')

    def __str__(self):
        return f"{self.book_name} in cart of {self.user_email}"