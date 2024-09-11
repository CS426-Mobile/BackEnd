from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.category_name