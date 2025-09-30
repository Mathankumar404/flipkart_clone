from django.db import models

# Create your models here.
class Products(models.Model):
      img=models.URLField()
      title=models.TextField()
      brand=models.CharField(max_length=100)
      offer=models.BigIntegerField(default=0)
      price=models.BigIntegerField(default=0)

      def __str__(self):
        return f"{self.title} - {self.brand} - ₹{self.price}"


class Cart(models.Model):
      product = models.ForeignKey(Products, on_delete=models.CASCADE)  # link to Products
      quantity = models.PositiveIntegerField(default=1)  # optional: track quantity
    
      def __str__(self):
          return f"{self.product.title} x {self.quantity}"


