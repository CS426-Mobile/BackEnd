from django.db import models

class Author(models.Model):
    author_name = models.CharField(max_length=50, primary_key=True)
    num_follower = models.IntegerField()
    about = models.TextField(max_length=1000)
    author_image = models.CharField(max_length=100)

    def __str__(self):
        return self.author_name
    
    def average_rating(self):
        total_rating = sum([book.average_rating() for book in self.book_set.all()])
        return total_rating / self.book_set.count() if self.book_set.count() > 0 else 0