from django.db import models
from Author.models import Author
from User.models import CustomUser

class CustomerFollow(models.Model):
    user_email = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    author_name = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_email', 'author_name')

    def __str__(self):
        return f"{self.user_email} follows {self.author_name}"