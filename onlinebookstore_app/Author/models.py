from django.db import models

class Author(models.Model):
    author_name = models.CharField(max_length=50, primary_key=True)
    num_follower = models.IntegerField()
    about = models.TextField(max_length=1000)
    author_image = models.CharField(max_length=100)

    def __str__(self):
        return self.author_name