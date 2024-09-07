from django.db import models
from Book.models import Book
from User.models import CustomUser
from .utils import generate_order_code, generate_str_digit

class CustomerOrder(models.Model):
    order_index = models.CharField(max_length=12, primary_key=True)
    user_email = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_code = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return f"Order {self.order_code} by {self.user_email}"
    
    def generate_order_index(self):
        # Generate a custom unique integer
        while True:
            order_index = generate_str_digit()
            if not CustomerOrder.objects.filter(order_index=order_index).exists():
                break
        return order_index
    
    def generate_order_code(self):
        # Generate a custom unique order code
        while True:
            order_code = generate_order_code()
            if not CustomerOrder.objects.filter(order_code=order_code).exists():
                break
        return order_code
    
    def save(self, *args, **kwargs):
        if not self.order_index:
            self.order_index = self.generate_order_index()
        if not self.order_code:
            self.order_code = self.generate_order_code()
        return super().save(*args, **kwargs)

class OrderDetail(models.Model):
    order_index = models.ForeignKey(CustomerOrder, on_delete=models.CASCADE)
    book_name = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('order_index', 'book_name')

    def __str__(self):
        return f"Order {self.order_index} includes {self.book_name}"