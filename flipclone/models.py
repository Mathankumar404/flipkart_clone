from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings

# Create your models here.
class Products(models.Model):
      img=models.URLField()
      title=models.TextField()
      brand=models.CharField(max_length=100)
      offer=models.BigIntegerField(default=0)
      price=models.BigIntegerField(default=0)

      def __str__(self):
        return f"{self.title} - {self.brand} - ₹{self.price}"

class User(models.Model):
      username = models.CharField(max_length=150, unique=True, blank=False)  # Required
      phone_no = models.CharField(
            max_length=10,
            validators=[RegexValidator(r'^\d{10}$', message="Enter a valid 10-digit phone number.")],
            unique=True,
            blank=False  # Required
      )
      password = models.CharField(max_length=128, blank=False)  # Required
      

class Cart(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      product = models.ForeignKey(Products, on_delete=models.CASCADE)  # link to Products
      quantity = models.PositiveIntegerField(default=1)  # optional: track quantity

      def __str__(self):
          return f"{self.product.title} x {self.quantity}"




