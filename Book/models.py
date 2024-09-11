from django.db import models
from Author.models import Author
from Category.models import Category

class Book(models.Model):
    book_name = models.CharField(max_length=50, primary_key=True)
    author_name = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    book_image = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    num_1_star = models.IntegerField()
    num_2_star = models.IntegerField()
    num_3_star = models.IntegerField()
    num_4_star = models.IntegerField()
    num_5_star = models.IntegerField()
    book_description = models.TextField(max_length=1000)
    public_date = models.DateField()
    book_language = models.CharField(max_length=50)
    book_weight = models.DecimalField(max_digits=4, decimal_places=1)
    book_page = models.IntegerField()

    def __str__(self):
        return self.book_name
    
    def average_rating(self):
        average = (self.num_1_star + self.num_2_star * 2 + self.num_3_star * 3 + self.num_4_star * 4 + self.num_5_star * 5) / (self.num_1_star + self.num_2_star + self.num_3_star + self.num_4_star + self.num_5_star)
        return round(average, 2)