from django.db import models
from users.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    producer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="products"
    )
    photo = models.ImageField(upload_to="product_photos/", blank=True, null=True)
    quality_grade = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
